import text_checker
import pickle


def serialize():
    # Open and read the base_text.txt
    with open('base_text.txt', 'r', encoding='utf-8') as file:
        base_text = file.read()

    checked_text = text_checker.check(base_text)

    pickle.dump(checked_text, open('base_result.pkl', 'wb'))
