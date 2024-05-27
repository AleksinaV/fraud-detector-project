import os

import file_cryptor
import text_comparer
import text_inputer
import text_serializer


# Call the main functions
def main(mode):
    # Режим, при котором необходимо ввести проверяемый текст в консоль
    if mode == 0:
        result_dict = text_inputer.process_text(text_inputer.input_text())  # Введённый текст обрабатывается
        # text_comparer.fraud_detect(result_dict)
        text_inputer.display_result(result_dict)  # Результат обработки выводится на экран

        text_comparer.compare_coef(text_comparer.count_coef(result_dict))

    # Режим с тестовым текстом потенциального мошенника
    if mode == 1:
        file_name = "test_text.txt"
        result_dict = text_inputer.process_text(text_inputer.process_file(file_name))  # Текст из файла
        # обрабатывается
        # text_comparer.fraud_detect(result_dict)
        text_inputer.display_result(result_dict)  # Результат обработки выводится на экран

        text_comparer.compare_coef(text_comparer.count_coef(result_dict))

    # Режим, который обращается к корпусу мошенников
    if mode == 2:
        file_name = 'base_text.txt'
        result_name = 'base_result.pkl'

        read_text = text_inputer.process_file(file_name)  # Происходит открытие файла
        result_dict = text_inputer.process_text(read_text)  # Текст из файла обрабатывается
        text_serializer.serialize_file(result_dict, result_name)  # Результат обработки сериализуется для оптимизации
        # обращения к данным результатам

    # Режим, который обращается к корпусу, призванному сбалансировать коэффициенты определения мошенников
    if mode == 3:
        file_name = 'balance_text.txt'
        result_name = 'balance_result.pkl'

        file_cryptor.decrypt_file('crypt_' + file_name, file_name)  # Корпус необходимо расшифровать по паролю
        # (опционально)

        read_text = text_inputer.process_file(file_name)  # Происходит открытие файла
        result_dict = text_inputer.process_text(read_text)  # Текст из файла обрабатывается
        text_serializer.serialize_file(result_dict, result_name)  # Результат обработки сериализуется для оптимизации
        # обращения к данным результатам

        file_cryptor.encrypt_file(file_name, 'crypt_' + file_name)  # Корпус балансировки шифруется (опционально)
        file_cryptor.encrypt_file(result_name, 'crypt_' + result_name)  # Результат обработки шифруется (опционально)
        # Исходные файлы (незашифрованные) должны быть удалены из ОС (опционально)
        os.remove(file_name)
        os.remove(result_name)


main(0)


def update_corpus():
    main(2)
    main(3)
