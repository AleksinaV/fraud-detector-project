# Step 0.
# Import libraries
import re
# pip install emot
import emot
# pip install nltk
# from nltk.tokenize import word_tokenize
# pip install pymorphy2
import pymorphy3

morph = pymorphy3.MorphAnalyzer()


# Tokenize the text into words and symbols
def tokenize_text(text):
    tokens = re.findall(r'(\b\w+\b|\S)', text)
    # tokens = word_tokenize(text)
    return tokens


# Step 3.1.1.
# Append list with emoticons from the text
def emoticon_find(text):
    emot_obj = emot.core.emot()
    emot_dict = emot_obj.emoji(text)

    return {"emoticon_list": emot_dict['value']}


# Step 3.1.2.
# Append lists with words, latin words, digits and symbols from the tokenized_text
def token_count(text, emoticon_list):
    word_list = []
    cyrillic_word_list = []
    latin_word_list = []
    mixed_word_list = []
    digit_list = []
    symbol_list = []

    tokenized_text = tokenize_text(text)
    for token in tokenized_text:
        if token.isalpha():
            word_list.append(token)
            if re.search(r"^[а-яА-Я]+$", token):
                cyrillic_word_list.append(token)
            elif re.search(r"^[a-zA-Z]+$", token):
                latin_word_list.append(token)
            else:
                mixed_word_list.append(token)
        elif token.isdigit():
            digit_list.append(token)
        else:
            if token not in emoticon_list:
                symbol_list.append(token)

    return {"word_list": word_list,
            "cyrillic_word_list": cyrillic_word_list,
            "latin_word_list": latin_word_list,
            "mixed_word_list": mixed_word_list,
            "digit_list": digit_list,
            "symbol_list": symbol_list}


# Step 3.1.3.
# Append lists with correct and incorrect words, names and surnames, ban words from the word_list
def word_check(word_list):
    correct_word_list = []
    en_correct_word_list = []
    surnames_list = []
    names_list = []
    ban_word_list = []

    questionable_list = []
    incorrect_word_list = []

    file_dict = {"russian_words.txt": correct_word_list,
                 "english_words.txt": en_correct_word_list,
                 "surnames.txt": surnames_list,
                 "names.txt": names_list,
                 "russian_ban_words.txt": ban_word_list}

    for file_name in file_dict.keys():
        with (open(file_name, encoding="utf-8") as current_file):
            current_file = current_file.read().lower().split()
            for word in word_list:
                if word.lower() in current_file:
                    file_dict[file_name].append(word)
                else:
                    normal_word = morph.parse(word)[0].normal_form
                    if normal_word.lower() in current_file:
                        file_dict[file_name].append(normal_word)

                in_lst = False
                for lst in file_dict.values():
                    if word in lst:
                        in_lst = True

                if not in_lst:
                    questionable_list.append(word)

    for word in questionable_list:
        in_lst = False
        for lst in file_dict.values():
            if word in lst:
                in_lst = True

        if not in_lst:
            incorrect_word_list.append(word)

    return {"correct_word_list": correct_word_list,
            "en_correct_word_list": en_correct_word_list,
            "incorrect_word_list": incorrect_word_list,
            "surnames_list": surnames_list,
            "names_list": names_list,
            "ban_word_list": ban_word_list}


# Step 3.1. Call the functions below to analyze the text
def text_check(text):
    found_emoticon = emoticon_find(text)
    counted_token = token_count(text, found_emoticon["emoticon_list"])
    checked_word = word_check(counted_token["word_list"])

    return {"counted_token": counted_token, "checked_word": checked_word, "found_emoticon": found_emoticon}


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
    check_result = text_check(text)
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
