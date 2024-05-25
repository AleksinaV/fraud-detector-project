import pymorphy3
import emot
import re


morph = pymorphy3.MorphAnalyzer()


# Tokenize the text into words and symbols
def tokenize_text(text):
    tokens = re.findall(r'(\b\w+\b|\S)', text)
    # tokens = word_tokenize(text)
    return tokens


# Append list with emoticons from the text
def emoticon_find(text):
    emot_obj = emot.core.emot()
    emot_dict = emot_obj.emoji(text)

    return {"emoticon_list": emot_dict['value']}


# Append lists with words: cyrillic, latin and mixed, digits and symbols from the tokenized_text
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
            if re.search(r"^[а-яА-ЯёЁ]+$", token):
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


# Append lists with correct and incorrect words in both languages, russian ban words from the word_list
def word_check(word_list):
    correct_word_list = []
    en_correct_word_list = []
    ban_word_list = []

    questionable_list = []
    incorrect_word_list = []

    file_dict = {"russian_words.txt": correct_word_list,
                 "english_words.txt": en_correct_word_list,
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
                        file_dict[file_name].append(word)

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

        if not in_lst and word not in incorrect_word_list:
            incorrect_word_list.append(word)

    return {"correct_word_list": correct_word_list,
            "en_correct_word_list": en_correct_word_list,
            "incorrect_word_list": incorrect_word_list,
            "ban_word_list": ban_word_list}


# Call the functions below to analyze the text
def check(text):
    found_emoticon = emoticon_find(text)
    counted_token = token_count(text, found_emoticon["emoticon_list"])
    checked_word = word_check(counted_token["word_list"])

    return {"counted_token": counted_token, "checked_word": checked_word, "found_emoticon": found_emoticon}


# Form result by creating dictionary with all the lists and their names
def form_result(result):
    list_dict = {}

    for function_result in result.values():
        for k, v in function_result.items():
            list_dict.update({k: v})

    return list_dict
