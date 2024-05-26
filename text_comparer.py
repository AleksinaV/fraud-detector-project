import text_checker
import text_serializer


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
    for key in list(dictio.keys()):
        parameters_amount += len(dictio[key])

    return parameters_amount


def fraud_detect(result_dict):
    fraud_detection = compare_parameters(result_dict,
                                         text_checker.form_result(text_serializer.deserialize_file('base_result.pkl')))

    if fraud_detection[0]:
        print("\nMaybe text was written by a scammer.")
    else:
        print("\nMaybe text was not written by a scammer.")

    print(f"input_coefficient = {fraud_detection[1]}, base_coefficient = {fraud_detection[2]}")
