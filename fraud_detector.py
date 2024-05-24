# Step 0.
# Import libraries
import text_checker


# Step 3.2. Form result by creating dictionary with all the lists
def form_result(result):
    list_dict = []

    for function_result in result.values():
        for k, v in function_result.items():
            list_dict.append((k, v))

    return list_dict


# Step 3.3. Display containment of all the lists
def display_result(result):
    print("\033[1;30;46mContainment of the lists:\033[0m")
    for couple in result:
        name_lst = couple[0]
        lst = couple[1]

        if len(lst) > 0:
            print(f"===> \033[1m{name_lst}\033[0m:", lst)


# Step 3.4. Count and display length of all the lists
def count_result(result):
    print("\033[1;30;45mLength of the lists:\033[0m")
    for couple in result:
        name_lst = couple[0]
        lst = couple[1]

        len_lst = len(lst)
        if len_lst > 0:
            print(f"===> \033[1m{name_lst}\033[0m:", len_lst)


# Step 3. Call the main functions and print the main information
def main(text):
    check_result = text_checker.check(text)
    result_dict = form_result(check_result)
    display_result(result_dict)
    count_result(result_dict)

    return result_dict
