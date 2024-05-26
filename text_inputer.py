import text_checker


def contain_result(result):
    print("\nContainment of the lists:")
    # Каждая пара ключ-значение в словаре проходит данный цикл
    for k, v in result.items():
        if len(v) > 0:
            # Если длина значения больше 0, то производится следующий вывод на экран
            print(f"===> {k}:", v)


# Count and display length of all the lists
def count_result(result):
    print("\nLength of the lists:")
    # Каждая пара ключ-значение в словаре проходит данный цикл
    for k, v in result.items():
        len_lst = len(v)    # Данная переменная содержит длину значения словаря
        if len_lst > 0:
            # Если длина значения больше 0, то производится следующий вывод на экран
            print(f"===> {k}:", len_lst)


def display_result(result):
    # Вызываются функции, выводящие на экран нужные показатели
    contain_result(result)
    count_result(result)


# Order text from the console
def input_text():
    inputted_text = input("Please, input a text: ")

    return inputted_text


def process_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        read_text = file.read()

    return read_text


def process_text(text):
    result = text_checker.check(text)
    result_dict = text_checker.form_result(result)

    return result_dict
