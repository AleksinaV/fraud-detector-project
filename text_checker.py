import pymorphy3
import emot
import re

morph = pymorphy3.MorphAnalyzer()


# Tokenize the text into words and symbols
def tokenize_text(text):
    tokens = re.findall(r'(\b\w+\b|\S)', text)

    return tokens


def emoticon_find(text):
    emot_obj = emot.core.emot()
    emot_dict = emot_obj.emoji(text)

    return {"emoticon_list": emot_dict['value']}


def token_check(tokenized_text):
    # Инициализируются все списки, в которые в дальнейшем будут добавляться соответствующие им токены
    word_list = []
    cyrillic_word_list = []
    latin_word_list = []
    mixed_word_list = []
    digit_list = []
    symbol_list = []

    # Каждый токен в токенизированном тексте проверяется на соответствие условиям
    for token in tokenized_text:
        if token.isalpha():
            word_list.append(token)  # Каждый токен, состоящий из букв, должен быть добавлен в word_list
            if re.search(r"^[а-яА-ЯёЁ]+$", token):
                cyrillic_word_list.append(token)  # Каждый токен, состоящий из букв кириллицы, должен быть добавлен в
                # cyrillic_word_list
            elif re.search(r"^[a-zA-Z]+$", token):
                latin_word_list.append(token)  # Каждый токен, состоящий из букв латиницы, должен быть добавлен в
                # latin_word_list
            else:
                mixed_word_list.append(token)  # Каждый токен, состоящий из букв и латиницы, и кириллицы, должен
                # быть добавлен в mixed_word_list

        elif token.isdigit():
            digit_list.append(token)  # Каждый токен, состоящий из цифр, должен быть добавлен в digit_list

        elif token in "[~!@#$%^&*+-/.,\\{}[]();:?<>\"'_]":
            symbol_list.append(token)  # Каждый токен, состоящий из вышеперечисленных символов, должен быть добавлен
            # в symbol_list

    # Возвращается словарь, состоящий из ключей-названий списков и значений-списков, которые соответствуют своему
    # названию
    return {"word_list": word_list,
            "cyrillic_word_list": cyrillic_word_list,
            "latin_word_list": latin_word_list,
            "mixed_word_list": mixed_word_list,
            "digit_list": digit_list,
            "symbol_list": symbol_list}


def word_check(cyrillic_word_list, latin_word_list):
    # Инициализируются все списки, в которые в дальнейшем будут добавляться соответствующие им слова
    correct_word_list = []
    en_correct_word_list = []
    ban_word_list = []

    questionable_list = []
    incorrect_word_list = []

    # Инициализируются словари, относящиеся к русскому и английскому языкам и состоящие из ключей-названий файлов и
    # значений-списков, в которые в дальнейшем будут добавляться обнаруженные в соответствующем файле слова
    russian_file_dict = {"russian_words.txt": correct_word_list,
                         "russian_ban_words.txt": ban_word_list}

    english_file_dict = {"english_words.txt": en_correct_word_list}

    ru_en_dict = {"russian_file_dict": cyrillic_word_list,
                  "english_file_dict": latin_word_list}

    for language_file_dict, layout_list in ru_en_dict.items():
        # Каждый файл из ключей словаря открывается (и закрывается по исполнении)
        for file_name in language_file_dict.keys():
            with open(file_name, encoding="utf-8") as current_file:
                current_file = current_file.read().lower().split()

                # Каждое слово из word_list проверяется на соответствие условиям
                for word in cyrrilic_word_list:
                    if word.lower() in current_file:
                        russian_file_dict[file_name].append(word)  # Если данное слово находится в данном файле, то оно должно
                        # быть добавлено в соответствующий файлу список

                    # Если данное слово не находится в данном файле, то оно должно быть приведено к начальной форме
                    else:
                        normal_word = morph.parse(word)[0].normal_form
                        if normal_word.lower() in current_file:
                            file_dict[file_name].append(word)  # Если данное слово, приведённое к начальной форме,
                            # находится в данном файле, то оно должно быть добавлено в соответствующий файлу список
                        else:
                            # Если после приведения к начальной форме слово всё равно не было найдено, то оно должно быть
                            # добавлено в questionable_list
                            questionable_list.append(word)

    # Каждое слово, находящееся в questionable_list, должно быть проверено на то, есть ли она хотя бы в одном списке
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
    counted_token = token_check(tokenize_text(text))
    checked_word = word_check(counted_token["word_list"])

    return {"counted_token": counted_token,
            "checked_word": checked_word,
            "found_emoticon": found_emoticon}


# Form result by creating dictionary with all the lists and their names
def form_result(result_dict):
    list_dict = {}

    for function_result in result_dict.values():
        for k, v in function_result.items():
            list_dict.update({k: v})

    return list_dict
