import coef_calc
import text_serializer


def count_parameters(dictio):
    params_list = []
    for lst in list(dictio.values())[1::]:
        params_list.append(len(lst))

    return params_list


def form_fraud_coef():
    base_result = text_serializer.deserialize_file('base_result.pkl')
    balance_result = text_serializer.deserialize_file('balance_result.pkl')

    text1_params = count_parameters(base_result)
    text2_params = count_parameters(balance_result)

    text1_word_count = len(base_result['word_list'])
    text2_word_count = len(balance_result['word_list'])

    fraud_coefficient = coef_calc.calculate_weight(text1_params, text1_word_count,
                                                   text2_params, text2_word_count)

    text_serializer.serialize_file(fraud_coefficient, 'fraud_coef.pkl')


def count_coef(result_dict):
    fraud_coef = text_serializer.deserialize_file('fraud_coef.pkl')

    len_list = count_parameters(result_dict)

    result_coef = 0
    for i in fraud_coef:
        for j in len_list:
            result_coef += (i * j)

    len_result_dict = len(result_dict['word_list'])
    if len_result_dict > 0:
        result = result_coef / len_result_dict

        return result

    else:
        print("\nword_list are empty.")
        return False


def compare_coef(user_coef):
    with open('coef.txt') as file:
        fraud_coef = file.readline()

    if float(user_coef) >= float(fraud_coef):
        print("\nMaybe this text was written by a scammer.")
    else:
        print("\nMaybe this text was not written by a scammer.")

    print(f"fraud_coef: {fraud_coef}user_coef: {user_coef}")


def update_coef():
    form_fraud_coef()

    base_coef = count_coef(text_serializer.deserialize_file('base_result.pkl'))
    balance_coef = count_coef(text_serializer.deserialize_file('balance_result.pkl'))

    with open('coef.txt', 'a') as file:
        file.truncate(0)
        file.write(str(base_coef) + '\n' + str(balance_coef))


# update_coef()
