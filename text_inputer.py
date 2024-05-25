import text_checker


# Display containment of all the lists
def contain_result(result):
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


def display_result(result):
    contain_result(result)
    count_result(result)


# Order text from the console
def process_text():
    input_text = input("Please, input a text: ")

    result = text_checker.check(input_text)
    result_dict = text_checker.form_result(result)

    return result_dict
