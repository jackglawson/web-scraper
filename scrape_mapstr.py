import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from load_mapstr import load_most_recent
from place import Place

URL = 'https://web.mapstr.com/'
USERNAME_INPUT_XPATH = '/html/body/div[1]/div/div/div/div[2]/form/div[2]/input'
PASSWORD_INPUT_XPATH = '/html/body/div[1]/div/div/div/div[2]/form/div[3]/input'
USERNAME = 'jackglawson@gmail.com'
PASSWORD = input('Password: ')
LIST_BUTTON_XPATH = '/html/body/div[1]/div[1]/div[1]/div[2]/div[3]/map-switch/div/div[2]/div/button[2]'
BACKGROUND_XPATH = '/html/body/div[1]/div[1]/div[2]/div/div[1]'
ADDRESS_CLASS_NAME = 'place-heading'
TAG_CLASS_NAME = 'tags'

# load page
driver = webdriver.Chrome()
driver.get(URL)
driver.implicitly_wait(3)
print('Page loaded')

# log in
u = driver.find_element_by_xpath(USERNAME_INPUT_XPATH)
u.send_keys(USERNAME)
p = driver.find_element_by_xpath(PASSWORD_INPUT_XPATH)
p.send_keys(PASSWORD)
p.send_keys(Keys.RETURN)
print('Logged in')

# change to list view
list_button = driver.find_element_by_xpath(LIST_BUTTON_XPATH)
list_button.click()


def find_addresses(driver):
    address_drivers = driver.find_elements_by_class_name(ADDRESS_CLASS_NAME)
    return [ad.text for ad in address_drivers]


def find_tags(driver):
    tag_drivers = driver.find_elements_by_class_name(TAG_CLASS_NAME)
    return [td.text for td in tag_drivers]


# click on background to allow scrolling
background = driver.find_element_by_xpath(BACKGROUND_XPATH)
background.click()

# scroll down to load all items
old_count = 0
new_count = len(find_addresses(driver))
while old_count != new_count:
    old_count = new_count
    body = driver.find_element_by_tag_name('html')
    for _ in range(100):
        body.send_keys(Keys.PAGE_DOWN)
    new_count = len(find_addresses(driver))

print('Done scrolling')

# get info
addresses = find_addresses(driver)
tags = find_tags(driver)
driver.quit()
print('Found {} addresses and {} tags'.format(len(addresses), len(tags)))


places = [Place(address, tag) for address, tag in zip(addresses, tags)]

# compare to last web scrape
old_places = load_most_recent()
print('Since last scrape, {} new places have been added:'.format(len(places) - len(old_places)))
for p in places:
    if p not in old_places:
        print('    {}'.format(p))

for p in old_places:
    if p not in places:
        print('WARNING: {} has been removed since last scrape'.format(p))


# save file
timestamp = '_'.join(time.ctime().split()).replace(':', '-')
filename = 'places_' + timestamp + '.pkl'
outfile = open(filename, 'wb')
pickle.dump(places, outfile)
outfile.close()

most_recent_file = open('most_recent.txt', 'w')
most_recent_file.write(filename)
most_recent_file.close()

print('Places saved')
