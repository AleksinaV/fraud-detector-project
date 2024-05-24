import text_input
import result_serialization


# Call the main functions
def main(mode):
    if mode == 1:
        text_input.order_text()
    else:
        result_serialization.serialize()


main(1)
