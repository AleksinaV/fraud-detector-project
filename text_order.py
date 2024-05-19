# Step 0.
# Import libraries
import re
# pip install emot
import emot
# pip install nltk
from nltk.tokenize import word_tokenize
# pip install pymorphy2
import pymorphy3

morph = pymorphy3.MorphAnalyzer()

# Step 1.
# Order text from the console
input_text = input("Please, input a text: ")


# Step 2.1.
# Tokenize the text into words and symbols
def tokenize_text(text):
    # tokens = re.findall(r'(\b\w+\b|\S)', text)
    tokens = word_tokenize(text)
    return tokens


# Step 2.
# Initialization tokenized_text by tokenize_text from the input_text
tokenized_text = tokenize_text(input_text)


# Step 3.
# Initialization lists below
correct_word_list = []
incorrect_word_list = []
surnames_list = []
names_list = []
ban_word_list = []

emoticon_list = []

word_list = []
latin_word_list = []
digit_list = []
symbol_list = []


# 5.1.1.
# Append lists above with words, latin words, digits and symbols from the tokenized_text
def token_count():
    for token in tokenized_text:
        if token.isalpha():
            word_list.append(token)
            if re.search(r"^[a-zA-Z]+$", token):
                latin_word_list.append(token)
        elif token.isdigit():
            digit_list.append(token)
        else:
            symbol_list.append(token)


# Step 5.1.2.
# Append lists above with correct and incorrect words, names and surnames, ban words from the word_list
def word_check():
    file_dict = {"russian_words.txt": correct_word_list,
                 "russian_surnames.txt": surnames_list,
                 "russian_names.txt": names_list,
                 "russian_ban_words.txt": ban_word_list}

    for file_name in file_dict.keys():
        with open(file_name, encoding="utf-8") as current_file:
            current_file = current_file.read().lower().split()
            for word in word_list:
                if word.lower() in current_file:
                    file_dict[file_name].append(word)
                else:
                    normal_word = morph.parse(word)[0].normal_form
                    if normal_word.lower() in current_file:
                        file_dict[file_name].append(normal_word)

                if word not in correct_word_list and word not in incorrect_word_list:
                    incorrect_word_list.append(word)


# Step 5.1.3.
# Append list above with emoticons from the input_text
def emoticon_search():
    emot_obj = emot.core.emot()
    emot_dict = emot_obj.emoji(input_text)
    if emot_dict['flag']:
        emoticon_list.append(emot_dict['value'])


# Step 5.1. Call the functions below to analyze the text
def text_check():
    token_count()
    word_check()
    emoticon_search()


# Step 5.2. Print the length of each list
def print_check():
    print("Amount of the words:", len(word_list))
    print("Amount of the latin words:", len(latin_word_list))
    print("Amount of the digits:", len(digit_list))
    print("Amount of the spell errors:", len(incorrect_word_list))
    print("Amount of the banned words:", len(ban_word_list))
    print("Amount of the surnames:", len(surnames_list))
    print("Amount of the names:", len(names_list))
    print("Amount of the emoticons:", len(emoticon_list))


# Step 5. Call the main functions and print the main information
def main():
    text_check()
    print("Tokenized text:", tokenized_text)
    print_check()


# Step 4. Call the main() function
main()
