import pickle


def serialize_file(text, file_name):
    pickle.dump(text, open(file_name, 'wb'))


def deserialize_file(file_name):
    result = pickle.load(open(file_name, 'rb'))

    return result
