import pymorphy3  # https://github.com/no-plagiarism/pymorphy3
import emot  # https://github.com/NeelShah18/emot
import re

morph = pymorphy3.MorphAnalyzer()


# Производится токенизация текста
def tokenize_text(text):
    tokens = re.findall(r'(\b\w+\b|\S)', text)

    # Возвращается список с токенами
    return tokens


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


# находим глаголы в повелительном наклонении

def find_imperative_verbs(text):
    def is_imperative_verb(word):
        # находим все возможные интерпретации слова
        parsed_words = morph.parse(word)
        for parsed_word in parsed_words:
            # определяем, что слово является глаголом в форме повелительного наклонения
            if parsed_word.tag.POS == 'VERB' and 'impr' in parsed_word.tag:
                return True
        return False

    # ищем слова в тексте
    words = tokenize_text(text)

    # находим все побудительные глаголы
    imperative_verbs = [word for word in words if is_imperative_verb(word)]

    return {'imperative_verbs': imperative_verbs}



# Поиск чрезмерных знаков восклицания
def find_excessive_exclamations(text):
    excessive_exclamations = []
    words = text.split()
    for word in words:
        exclamation_count = 0
        for char in word:
            if char == '!':
                exclamation_count += 1
                if exclamation_count > 1:
                    excessive_exclamations.append(word)
                    break
    return {"excessive_exclamations": excessive_exclamations}


# Поиск чрезмерных вопросительных знаков
def find_excessive_questions(text):
    excessive_questions = []
    words = text.split()
    for word in words:
        questions_count = 0
        for char in word:
            if char == '?':
                questions_count += 1
                if questions_count > 1:
                    excessive_questions.append(word)
                    break
    return {"excessive_questions": excessive_questions}


# Поиск знаков восклицания с вопросительными знаками
def find_question_and_exclamation(text):
    question_and_exclamation = []
    words = text.split()
    for word in words:
        found_alternation = False
        current_punctuation = []
        for char in word:
            if char == '!' or '?':
                if current_punctuation and current_punctuation[-1] != char:
                    current_punctuation.append(char)
                    found_alternation = True
                elif not current_punctuation:
                    current_punctuation.append(char)
                else:
                    current_punctuation = [char]
            else:
                if found_alternation:
                    question_and_exclamation.append(word)
                    break
                current_punctuation = []
        if found_alternation and "".join(current_punctuation) in word:
            question_and_exclamation.append(word)
    return {"question_and_exclamation": question_and_exclamation}


# Поиск ссылок
def find_links(text):
    link_pattern = re.compile(r'([a-zA-Z0-9\-_]+\.[a-zA-Z]{2,}([a-zA-Z0-9\-\._~:/?#\[\]@!\$&\'\(\)\*\+,;=]'
                              r'*)|www\.[a-zA-Z0-9\-_]+\.[a-zA-Z]{2,}([a-zA-Z0-9\-\._~:/?#\[\]@!\$&\'\(\)\*\+,;=]*))')
    links = link_pattern.findall(text)
    links = [link[0] for link in links]
    return {"links": links}


# Поиск электронных почт
def find_emails(text):
    email_pattern = r"[a-zA-Z0-9.+_-]+@[a -zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    return {"emails": emails}


# Поиск капитализированных слов
def find_capitalized_text(word_list):
    capitalized_text = []
    for word in word_list:
        if word.isalpha() and word.isupper() and len(word) > 1:
            capitalized_text.append(word)
    return {"capitalized_text": capitalized_text}
=======
def find_personal_info(text):
    # поиск номеров карт в тексте
    def find_card_numbers(text):
        # шаблоны номеров карт
        cards = [
            # карты Visa
            r'\b4\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            # карты Mastercard
            r'\b5[1-5]\d{2}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            r'\b2[2-7]\d{2}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            # карты Мир
            r'\b220[0-4][-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # 16 цифр
            r'\b220[0-4][-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{5}\b',  # 17 цифр
            r'\b220[0-4]\d{4}[-\s]?\d{10}\b',  # 18 цифр
            r'\b220[0-4]\d{3}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b'
        ]
        card_numbers = set()  # Создаем пустое множество, для дальнейшего добавления в него найденных номеров

        for numbers in cards:
            matches_ = re.findall(numbers, text)
            card_numbers.update(matches_)

        return {'card_list': list(card_numbers)}

    # поиск номеров телефона в тексте
    def find_phone_numbers(text):
        # шаблоны номеров телефона
        phone_patterns = [
            # +7/8 (000) 000-00-00 и +7/8 000 000-00-00(как с пробелами, так и без них)
            r'(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}-\d{2}-\d{2}\b',
            # +7/8-000-000-00-00
            r'(?:\+7|8)-\d{3}-\d{3}-\d{2}-\d{2}\b',
            # +7/8 000 000 0000 и +7/8 (000) 000 0000 (как с пробелами, так и без них)
            r'(?:\+7|8)\s?\(?\d{3}\)?\s?\d{3}\s?\d{4}\b'
        ]
        phone_numbers = []
        for pattern in phone_patterns:
            matches = re.findall(pattern, text)
            phone_numbers.extend(matches)

        return {'phone_numbers_list': phone_numbers}

    found_card_numbers = find_card_numbers(text)
    found_phone_numbers = find_phone_numbers(text)

    result_dict = {}
    result_dict.update(found_card_numbers)
    result_dict.update(found_phone_numbers)

    return result_dict


def find_expressive(text):
    # Производится обработка текста, приводящая к нахождению эмотиконов
    def emoticon_find(text):
        emot_obj = emot.core.emot()
        emot_dict = emot_obj.emoji(text)

        # Возвращается словарь, состоящий из ключей-названий списков и значений-списков, которые соответствуют своему
        # названию
        return {"emoticon_list": emot_dict['value']}

    found_emoticon = emoticon_find(text)

    result_dict = {}
    result_dict.update(found_emoticon)

    return result_dict


def check(text):
    # Вызываются функции, необходимые для обработки текста, и сохраняются их возвращённые значения в соответствующие
    # переменные
    found_expressive = find_expressive(text)
    counted_token = token_check(tokenize_text(text), found_expressive["emoticon_list"])
    checked_word = word_check(counted_token["cyrillic_word_list"], counted_token["latin_word_list"])
    found_personal_info = find_personal_info(text)
    found_imperative_verbs = find_imperative_verbs(text)

    # Возвращается словарь, состоящий из ключей-названий словарей и значений-словарей, которые соответствуют своему
    # названию
    return {"counted_token": counted_token,
            "checked_word": checked_word,
            "found_personal_info": found_personal_info,
            "found_imperative_verbs": found_imperative_verbs}


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
