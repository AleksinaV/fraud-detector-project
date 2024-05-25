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

    # Инициализируется словарь, состоящий из ключей-языков, к которым относятся их значения-списки. Оные содержат
    # словарь соответствующего языка и список со словами соответствующей раскладки
    ru_en_dict = {"russian_requirements": [russian_file_dict, cyrillic_word_list],
                  "english_requirements": [english_file_dict, latin_word_list]}

    # Каждое значение словаря ru_en_dict проходит данный цикл
    for language_requirement in ru_en_dict.values():
        file_dict = language_requirement[0]  # В данной переменной находится соответствующий языку словарь со
        # списками параметров
        layout_list = language_requirement[1]  # В данной переменной находится список с соответствующей языку раскладкой

        # Каждый файл из ключей словаря проходит данный цикл
        for file_name in file_dict.keys():
            # Открывается (и закрывается по исполнении) файл, который требует проверки
            with open(file_name, encoding="utf-8") as current_file:
                current_file = current_file.read().lower().split()  # В данной переменной находится прочтённый файл,
                # приведённый к низкому регистру и разделённый разделителем по умолчанию - пробелом

                parameter_list = file_dict[file_name]  # В данной переменной находится список параметров,
                # соответствующий названию открытого в данный момент файла

                # Каждое слово из word_list проверяется на соответствие условиям
                for word in layout_list:
                    if word.lower() in current_file:
                        parameter_list.append(word)  # Если данное слово находится в данном файле, то оно должно
                        # быть добавлено в соответствующий файлу список

                    # Если данное слово не находится в данном файле, то оно должно быть приведено к начальной форме
                    else:
                        normal_word = morph.parse(word)[0].normal_form
                        if normal_word.lower() in current_file:
                            parameter_list.append(word)  # Если данное слово, приведённое к начальной форме,
                            # находится в данном файле, то оно должно быть добавлено в соответствующий файлу список
                        else:
                            # Если даже после приведения к начальной форме слово всё равно не было найдено,
                            # то оно должно быть добавлено в questionable_list, если до этого оно не находилось хотя
                            # бы в одном списке
                            in_lst = False
                            for lst in file_dict.values():
                                if word in lst:
                                    in_lst = True
                                    break

                            if not in_lst and word not in questionable_list:
                                questionable_list.append(word)

        # Каждое слово, находящееся в questionable_list, должно быть проверено на то, есть ли оно хотя бы в одном списке
        for word in questionable_list:
            in_lst = False
            for lst in file_dict.values():
                if word in lst:
                    in_lst = True

            if not in_lst and word not in incorrect_word_list:
                incorrect_word_list.append(word)  # Каждое слово, которое не было обнаружено ни в одном списке и до
                # сих пор не находится в incorrect_word_list, должно быть добавлено в оный

    # Возвращается словарь, состоящий из ключей-названий списков и значений-списков, которые соответствуют своему
    # названию
    return {"correct_word_list": correct_word_list,
            "en_correct_word_list": en_correct_word_list,
            "incorrect_word_list": incorrect_word_list,
            "ban_word_list": ban_word_list}


def check(text):
    # Вызываются функции, необходимые для обработки текста, и сохраняются возвращённые значения в переменные
    found_emoticon = emoticon_find(text)
    counted_token = token_check(tokenize_text(text))
    checked_word = word_check(counted_token["cyrillic_word_list"], counted_token["latin_word_list"])

    # Возвращается словарь, состоящий из ключей-названий словарей и значений-словарей, которые соответствуют своему
    # названию
    return {"counted_token": counted_token,
            "checked_word": checked_word,
            "found_emoticon": found_emoticon}


def form_result(result_dict):
    list_dict = {}

    for function_result in result_dict.values():
        for k, v in function_result.items():
            list_dict.update({k: v})

    return list_dict
