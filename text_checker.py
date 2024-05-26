import pymorphy3  # https://github.com/no-plagiarism/pymorphy3
import emot  # https://github.com/NeelShah18/emot
import re

morph = pymorphy3.MorphAnalyzer()


# Производится токенизация текста
def tokenize_text(text):
    tokens = re.findall(r'(\b\w+\b|\S)', text)

    # Возвращается список с токенами
    return tokens


# Производится обработка текста, приводящая к нахождению эмотиконов
def emoticon_find(text):
    emot_obj = emot.core.emot()
    emot_dict = emot_obj.emoji(text)

    # Возвращается словарь, состоящий из ключей-названий списков и значений-списков, которые соответствуют своему
    # названию
    return {"emoticon_list": emot_dict['value']}


def token_check(tokenized_text, emoticon_list):
    # Инициализируются все списки, в которые в дальнейшем будут добавляться соответствующие им токены
    word_list = []
    cyrillic_word_list = []
    latin_word_list = []
    mixed_word_list = []
    digit_list = []
    symbol_list = []
    express_list = []
    currency_list = []
    trash_list = []

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

        elif token in "[~@#№%^&*+-=/.,\\{}[]();:<>\"'_]«»":
            symbol_list.append(token)  # Каждый токен, содержащий в себе что-либо из вышеперечисленных символов,
            # должен быть добавлен в symbol_list

        elif token in "!?":
            express_list.append(token)  # Каждый токен, содержащий в себе что-либо из вышеперечисленных символов,
            # должен быть добавлен в express_list

        elif token in "$€£₽₸₴₮₱֏₩¥₦₲₫₭₡₾₼₹₵৳ƒ₪฿":
            currency_list.append(token)  # Каждый токен, содержащий в себе что-либо из вышеперечисленных символов,
            # должен быть добавлен в currency_list

        else:
            if token not in emoticon_list:
                trash_list.append(token)  # Каждый токен, не соответствующий ни одному условию выше и не
                # являющийся эмотиконом, должен быть добавлен в trash_list

    # Возвращается словарь, состоящий из ключей-названий списков и значений-списков, которые соответствуют своему
    # названию
    return {"word_list": word_list,
            "cyrillic_word_list": cyrillic_word_list,
            "latin_word_list": latin_word_list,
            "mixed_word_list": mixed_word_list,
            "digit_list": digit_list,
            "symbol_list": symbol_list,
            "express_list": express_list,
            "currency_list": currency_list,
            "trash_list": trash_list}


def word_check(cyrillic_word_list, latin_word_list):
    # Инициализируются все списки, в которые в дальнейшем будут добавляться соответствующие им слова
    correct_word_list = []
    en_correct_word_list = []
    ban_word_list = []
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

    # Каждое значение словаря ru_en_dict (список со словарём соответствующего языка и списком со словами
    # соответствующей раскладки) проходит данный цикл
    for language_requirement in ru_en_dict.values():
        questionable_list = []

        file_dict = language_requirement[0]  # В данной переменной находится соответствующий языку словарь со
        # списками параметров
        layout_list = language_requirement[1]  # В данной переменной находится список с соответствующей языку раскладкой

        # Каждый файл из ключей словаря (названий файлов) проходит данный цикл
        for file_name in file_dict.keys():
            # Открывается (и закрывается по исполнении) файл, который требует проверки
            with open(file_name, encoding="utf-8") as current_file:
                current_file = current_file.read().lower().split()  # В данной переменной находится прочтённый файл
                # в виде списка слов, приведённых к низкому регистру и разделённых разделителем по умолчанию - пробелом

                parameter_list = file_dict[file_name]  # В данной переменной находится список параметров,
                # соответствующий названию открытого в данный момент файла

                # Каждое слово из списка со словами соответствующей языку раскладки проверяется на соответствие условиям
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

                        else:  # Если даже после приведения к начальной форме слово всё равно не было найдено,
                            # то оно должно быть добавлено в questionable_list, если до этого оно не находилось хотя
                            # бы в одном списке

                            # Инициализируется индикатор того, находится ли проверяемое слово в каком-либо списке.
                            # По умолчанию False
                            in_lst = False
                            # Каждый список в значениях словаря с ключами-названиями списков и значениями-списками
                            # проходит данный цикл
                            for lst in file_dict.values():
                                if word in lst:
                                    in_lst = True  # Если слово находится в проверяемом списке, то индикатор должен быть
                                    # сменен на True
                                    break  # Цикл прерывается, если слово было найдено хотя бы в одном списке,
                                    # т.к. дальнейшая проверка по остальным спискам не имеет значения

                            if not in_lst and word not in questionable_list:
                                questionable_list.append(word)  # Каждое слово, которое не было обнаружено ни в одном
                                # списке и до сих пор не находится в incorrect_word_list, должно быть добавлено в оный

        # Каждое слово, находящееся в questionable_list, должно быть проверено на то, есть ли оно хотя бы в одном списке
        for word in questionable_list:
            # Инициализируется индикатор того, находится ли проверяемое слово в каком-либо списке. По умолчанию False
            in_lst = False
            # Каждый список в значениях словаря с ключами-названиями списков и значениями-списками проходит данный цикл
            for lst in file_dict.values():
                if word in lst:
                    in_lst = True  # Если слово находится в проверяемом списке, то индикатор должен быть сменен на True
                    break  # Цикл прерывается, если слово было найдено хотя бы в одном списке, т.к. дальнейшая
                    # проверка по остальным спискам не имеет значения

            if not in_lst and word not in incorrect_word_list:
                incorrect_word_list.append(word)  # Каждое слово, которое не было обнаружено ни в одном списке и до
                # сих пор не находится в incorrect_word_list, должно быть добавлено в оный

    # Возвращается словарь, состоящий из ключей-названий списков и значений-списков, которые соответствуют своему
    # названию
    return {"correct_word_list": correct_word_list,
            "en_correct_word_list": en_correct_word_list,
            "incorrect_word_list": incorrect_word_list,
            "ban_word_list": ban_word_list}


# поиск номеров карт в тексте
def find_card_numbers(text):
    # шаблоны номеров карт
    cards = [
        # карты Visa
        r'\b4\d{15}\b',
        r'\b4\d{3} \d{4} \d{4} \d{4}\b',
        r'\b4\d{3}-\d{4}-\d{4}-\d{4}\b',
        # карты Mastercard
        r'\b5[1-5]\d{14}\b',
        r'\b5[1-5]\d{2}-\d{4}-\d{4}-\d{4}\b'
        r'\b5[1-5]\d{2} \d{4} \d{4} \d{4}\b'
        r'\b2[2-7]\d{14}\b',
        r'\b2[2-7]\d{2}-\d{4}-\d{4}-\d{4}\b',
        r'\b2[2-7]\d{2} \d{4} \d{4} \d{4}\b',
        # карты Мир
        r'\b220[0-4][0-9]{12,15}\b',
        r'\b220[0-4] \d{4} \d{4} \d{4}\b',  # 16 цифр с разделителями
        r'\b220[0-4]-\d{4}-\d{4}-\d{4}\b',
        r'\b220[0-4] \d{4} \d{4} \d{5}\b',  # 17 цифр с разделителями
        r'\b220[0-4]-\d{4}-\d{4}-\d{5}\b',
        r'\b220[0-4]\d{4} \d{10}\b',  # 18 цифр с разделителями
        r'\b220[0-4]\d{4}-\d{10}\b',
        r'\b220[0-4]\d{3} \d{4} \d{4} \d{4}\b',  # 19 цифр с разделителями
        r'\b220[0-4]\d{3}-\d{4}-\d{4}-\d{4}\b'
    ]
    card_numbers = set()  # Создаем пустое множество, для дальнейшего добавления в него найденных номеров

    for numbers in cards:
        matches = re.findall(numbers, text)
        card_numbers.update(matches)

    return {'card_list': list(card_numbers)}
# поиск номеров телефона в тексте
def find_phone_numbers(text):
    # шаблоны номеров телефона
    phone_patterns = [
        # +7 (000) 000-00-00 (как с пробелами, так и без них)
        r'\b\+7\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}\b',
        # +7 000 000-00-00 (как с пробелами, так и без них)
        r'\b\+7\s?\d{3}\s?\d{3}-\d{2}-\d{2}\b',
        # +7-000-000-00-00
        r'\b\+7-\d{3}-\d{3}-\d{2}-\d{2}\b',
        # 8 (000) 000-00-00 (как с пробелами, так и без них)
        r'\b8\s?\(\d{3}\)\s?\d{3}-\d{2}-\d{2}\b',
        # 8 000 000-00-00 (как с пробелами, так и без них)
        r'\b8\s?\d{3}\s?\d{3}-\d{2}-\d{2}\b',
        # 8-000-000-00-00
        r'\b8-\d{3}-\d{3}-\d{2}-\d{2}\b',
        # +7 000 000 0000 (как с пробелами, так и без них)
        r'\b\+7\s?\d{3}\s?\d{3}\s?\d{4}\b',
        # 8 000 000 0000 (как с пробелами, так и без них)
        r'\b8\s?\d{3}\s?\d{3}\s?\d{4}\b',
        # +7 (000) 000 0000 (как с пробелами, так и без них)
        r'\b\+7\s?\(\d{3}\)\s?\d{3}\s?\d{4}\b',
        # 8 (000) 000 0000 (как с пробелами, так и без них)
        r'\b8\s?\(\d{3}\)\s?\d{3}\s?\d{4}\b'
    ]
    phone_numbers = []
    for pattern in phone_patterns:
        matches = re.findall(pattern, text)
        phone_numbers.extend(matches)

    return {'phone_numbers': phone_numbers}

def check(text):
    # Вызываются функции, необходимые для обработки текста, и сохраняются их возвращённые значения в соответствующие
    # переменные
    found_emoticon = emoticon_find(text)
    counted_token = token_check(tokenize_text(text), found_emoticon["emoticon_list"])
    checked_word = word_check(counted_token["cyrillic_word_list"], counted_token["latin_word_list"])
    found_card_numbers = find_card_numbers(text)
    found_phone_numbers = find_phone_numbers(text)

    # Возвращается словарь, состоящий из ключей-названий словарей и значений-словарей, которые соответствуют своему
    # названию
    return {"counted_token": counted_token,
            "checked_word": checked_word,
            "found_emoticon": found_emoticon,
            "found_card_numbers": found_card_numbers,
            "found_phone_numbers": found_phone_numbers}


def form_result(result_dict):
    # Инициализируется словарь, который в дальнейшем будет состоять из ключей-названий списков и значений-списков,
    # соответствующих своему названию
    list_dict = {}

    # Каждый словарь-результат функции, который находится в значениях передаваемого словаря, проходит данный цикл
    for function_result in result_dict.values():
        # Каждая пара ключ-значение в словаре-результате функции проходит данный цикл
        for k, v in function_result.items():
            list_dict.update({k: v})  # Инициализированный словарь обновляется ключом-названием списка и значением-
            # списком, который соответствует своему названию

    # Возвращается инициализированный словарь
    return list_dict
