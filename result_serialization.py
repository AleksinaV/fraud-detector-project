from fraud_detector import main
import pickle


# Step #1. Open and read the base_text.txt
with open('base_text.txt', 'r', encoding='utf-8') as file:
    base_text = file.read()

# Step #2. Call the main() function
result_dict = main(base_text)
print(result_dict)

# pickle.dump(result_dict, open('base_result.pkl', 'w'))
# unpickled_resilt = pickle.load('base_result.pkl')
# print(unpickled_resilt)
