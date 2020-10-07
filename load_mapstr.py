import pickle


def load_most_recent():
    most_recent_file = open('most_recent.txt', 'r')
    filename = most_recent_file.read()
    most_recent_file.close()

    infile = open(filename, 'rb')
    places = pickle.load(infile)
    infile.close()

    return places


def print_most_recent():
    places = load_most_recent()
    print(places)