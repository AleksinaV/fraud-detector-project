import text_checker
import compare_texts


# Display containment of all the lists
def display_result(result):
    print("\nContainment of the lists:")
    for k, v in result.items():
        if len(v) > 0:
            print(f"===> {k}:", v)


# Count and display length of all the lists
def count_result(result):
    print("\nLength of the lists:")
    for k, v in result.items():
        len_lst = len(v)
        if len_lst > 0:
            print(f"===> {k}:", len_lst)


# Order text from the console
def order_text():
    input_text = input("Please, input a text: ")

    result = text_checker.check(input_text)
    result_dict = text_checker.form_result(result)

    display_result(result_dict)
    count_result(result_dict)

    if_scammer = compare_texts.compare_parameters(result_dict, compare_texts.collect_data())

    if if_scammer[0]:
        print("\nMaybe text was written by a scammer.")
    else:
        print("\nMaybe text was not written by a scammer.")

    print(f"input_coefficient = {if_scammer[1]}, base_coefficient = {if_scammer[2]}")
