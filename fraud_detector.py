import file_cryptor
import text_comparer
import text_inputer
import text_serializer


# Call the main functions
def main(mode):
    # Режим, при котором необходимо ввести проверяемый текст в консоль
    if mode == 0:
        print("Disclaimer: The corpus of texts written by the scammers was compiled from their written speech from "
              "various messengers.\nIt is possible that if you use texts taken from other sources (letters, "
              "oral speech, posts) to verify, the result may be unreliable.\nPlease do not base your decisions "
              "on the results of this program.\n")

        result_dict = text_inputer.process_text(text_inputer.input_text())  # Введённый текст обрабатывается
        text_inputer.display_result(result_dict)  # Результат обработки выводится на экран

        coef = text_comparer.count_coef(result_dict)
        if coef:
            text_comparer.compare_coef(coef)

    # Режим с тестовым текстом потенциального мошенника
    if mode == 1:
        file_name = "test_text.txt"
        result_dict = text_inputer.process_text(text_inputer.process_file(file_name))  # Текст из файла
        # обрабатывается
        text_inputer.display_result(result_dict)  # Результат обработки выводится на экран

        coef = text_comparer.count_coef(result_dict)
        if coef:
            text_comparer.compare_coef(coef)

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

        read_text = text_inputer.process_file(file_name)  # Происходит открытие файла
        result_dict = text_inputer.process_text(read_text)  # Текст из файла обрабатывается
        text_serializer.serialize_file(result_dict, result_name)  # Результат обработки сериализуется для оптимизации
        # обращения к данным результатам


main(0)


def update_corpus():
    main(2)
    main(3)


def update_all():
    update_corpus()
    text_comparer.update_coef()


# update_all()
