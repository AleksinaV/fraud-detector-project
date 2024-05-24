# Step 0.
# Import libraries
import re
# pip install emot
import emot
# pip install nltk
# from nltk.tokenize import word_tokenize
# pip install pymorphy2
import pymorphy3
# import pickle
# import text_check

morph = pymorphy3.MorphAnalyzer()


# Tokenize the text into words and symbols
def tokenize_text(text):
    tokens = re.findall(r'(\b\w+\b|\S)', text)
    # tokens = word_tokenize(text)
    return tokens


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
    # check_result = text_check.text_check(text)
    result_dict = form_result(check_result)
    display_result(result_dict)
    count_result(result_dict)


# Step #1. Open and read the base_text.txt
# with open('base_text.txt', 'r', encoding='utf-8') as file:
#     base_text = file.read()
# Step #2. Call the main() function
# main(base_text)

# Step 1.
# Order text from the console
input_text = input("Please, input a text: ")

# Step 2. Call the main() function
main(input_text)
