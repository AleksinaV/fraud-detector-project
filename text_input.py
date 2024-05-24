from fraud_detector import main


# Display containment of all the lists
def display_result(result):
    print("\033[1;30;46mContainment of the lists:\033[0m")
    for couple in result:
        name_lst = couple[0]
        lst = couple[1]

        if len(lst) > 0:
            print(f"===> \033[1m{name_lst}\033[0m:", lst)


# Count and display length of all the lists
def count_result(result):
    print("\033[1;30;45mLength of the lists:\033[0m")
    for couple in result:
        name_lst = couple[0]
        lst = couple[1]

        len_lst = len(lst)
        if len_lst > 0:
            print(f"===> \033[1m{name_lst}\033[0m:", len_lst)


# Order text from the console
def order_text():
    input_text = input("Please, input a text: ")
    result_dict = main(input_text)
    display_result(result_dict)
    count_result(result_dict)
