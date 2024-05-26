import json


def open_json(file_name):
    current_file = open(file_name, 'r', encoding="utf-8")
    json_file = json.load(current_file)
    parse(json_file)
    current_file.close()


def parse(json_file):
    result_str = ""
    for message in json_file['messages']:
        try:
            message_text = message['text_entities']
            text_pos = message_text[0]
            text = text_pos['text']
            result_str += text + '\n'
        except Exception:
            continue
    save(result_str)


def save(text):
    with open("balance.txt", 'a', encoding="utf-8") as saving_file:
        saving_file.write(text)


open_json("result.json")
