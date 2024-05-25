import text_input
import result_serialization


# Call the main functions
def main(mode):
    if mode == 1:
        text_input.order_text()
    else:
        result_serialization.serialize(result_serialization.process_data('base_text.txt'), 'base_result.pkl')


main(1)
