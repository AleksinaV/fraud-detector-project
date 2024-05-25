import pickle
import text_checker


def collect_data(file_name):
    unpickled_result = pickle.load(open(file_name, 'rb'))

    base_result = text_checker.form_result(unpickled_result)

    return base_result


def compare_parameters(input_result, base_result):
    base_words_amount = len(base_result["word_list"])
    input_words_amount = len(input_result["word_list"])

    base_parameters_amount = count_parameters(base_result)
    input_parameters_amount = count_parameters(input_result)

    base_coefficient = round((base_parameters_amount / base_words_amount), 2)
    input_coefficient = round((input_parameters_amount / input_words_amount), 2)

    if input_coefficient >= base_coefficient:
        return [True, input_coefficient, base_coefficient]
    else:
        return [False, input_coefficient, base_coefficient]


def count_parameters(dictio):
    parameters_amount = 0
    for key in list(dictio.keys())[1::]:
        parameters_amount += len(dictio[key])

    return parameters_amount
