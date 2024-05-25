import text_inputer
import text_serializer
import text_comparer
import text_checker


# Call the main functions
def main(mode):
    if mode == 0:
        result_dict = text_inputer.process_text()

        text_inputer.display_result(result_dict)
        text_comparer.fraud_detect(result_dict)
    elif mode == 1:
        text_serializer.serialize(text_serializer.process_data('base_text.txt'), 'base_result.pkl')
    elif mode == 2:
        text_serializer.serialize(text_serializer.process_data('balance_text.txt'), 'balance_result.pkl')


main(0)

# result = text_serializer.deserialize('balance_result.pkl')
# result = text_checker.form_result(result)
# text_inputer.display_result(result)
#
# text_comparer.fraud_detect(result)
