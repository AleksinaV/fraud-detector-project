import pickle


def serialize(text, file_name):
    pickle.dump(text, open(file_name, 'wb'))


def deserialize(file_name):
    result = pickle.load(open(file_name, 'rb'))

    return result
