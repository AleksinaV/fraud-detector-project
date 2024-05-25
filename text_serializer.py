import text_checker
import pickle


def process_data(file_name):
    # Open and read the base_text.txt
    with open(file_name, 'r', encoding='utf-8') as file:
        base_text = file.read()

    checked_text = text_checker.check(base_text)

    return checked_text


def serialize(text, file_name):
    pickle.dump(text, open(file_name, 'wb'))


def deserialize(file_name):
    result = pickle.load(open(file_name, 'rb'))

    return result
