import text_inputer
import text_serializer
import text_comparer


# Call the main functions
def main(mode):
    if mode == 0:
        result_dict = text_inputer.process_text(text_inputer.input_text())
        # text_comparer.fraud_detect(result_dict)

    else:
        file_name = "test_text.txt"
        result_name = "test_result.pkl"

        if mode == 1:
            file_name = 'base_text.txt'
            result_name = 'base_result.pkl'

        elif mode == 2:
            file_name = 'balance_text.txt'
            result_name = 'balance_result.pkl'

        read_text = text_inputer.process_file(file_name)
        text_serializer.serialize_file(text_inputer.process_text(read_text), result_name)
        result_dict = text_serializer.deserialize_file(result_name)

    text_inputer.display_result(result_dict)


main(0)
