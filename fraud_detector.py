import text_inputer
import text_serializer
import text_comparer


# Call the main functions
def main(mode):
    if mode == 1:
        result_dict = text_inputer.process_text()

        text_inputer.display_result(result_dict)
        text_comparer.fraud_detect(result_dict)
    else:
        text_serializer.serialize(text_serializer.process_data('base_text.txt'), 'base_result.pkl')


main(1)
