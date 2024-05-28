# fraud-detector-project
This repository is designed to help determine if the text was written for the purpose of fraud. 

We have collected a corpus of texts based on written messages from russian-speaking scammers from various messengers, as well as a corpus based on the personal messages of the average russian-speaking user (encrypted to save personal data). 

The repository is focused on texts written primarily in Russian with few assumptions (there is a check for correctly written English words and English trigger words; the pymorphy library, used to determine some parameters, in addition to the Russian language, also supports Ukrainian).

Next, we searched for those parameters that could indicate whether the author of the text is a fraud. For example, the following turned out to be explicit markers: motivational verbs, trigger words, overly expressive symbols (!!!, ???, ?!?!), emoticons, etc.

After that, each corpus was programmatically analyzed. The optimal coefficients were calculated by the method of differential evolution (don't ask...).

Each list of parameters from the text to be checked is multiplied by the corresponding coefficient. The sum of these coefficients is divided by the total number of words. This compares the coefficient of the text being checked and the corpus of scammers. If the first coefficient is greater than or equal to the coefficient of the second, then most likely the text being checked was written for the purpose of fraud.

This repository can be improved by adding new parameters. For example, by checking names and surnames in both Latin and Cyrillic (the corresponding files are already on the git).

The corpus with the texts of scammers (base_text.txt) is freely available. If you decide to further refine this project, you need to create a corpus with user texts yourself (for example, download the required number of dialogues from messengers, parse them and translate them into human-readable form (json_parser.py to help you)).

======

Этот репозиторий предназначен для того, чтобы помочь определить, был ли текст написан с целью мошенничества. 

Репозиторий ориентирован на тексты, написанные преимущественно на русском языке с небольшими допущениями (идёт проверка на правильно написанные английские слова и на английские слова-триггеры; библиотека pymorphy, используемая при определении некоторых параметров, помимо русского языка, также поддерживает и украинский).

Мы собрали корпус текстов, основанных на письменных сообщениях мошенников из различных мессенджеров, а также корпус, основанный на личных сообщениях среднестатического юзера (зашифрован для сохранения личных данных). 

Далее мы искали те параметры, которые могли бы свидетельствовать о том, является ли автор текста мошенником. Например, явными маркерами оказались следующие: побудительные глаголы, слова-триггеры, чрезмерные экспрессивные символы (!!!, ???, ?!?!), эмотиконы и т.д.

После этого каждый корпус был программно проанализирован. Оптимальные коэффициенты были высчитаны методом дифференциальной эволюции (не спрашивайте...).

Каждый список параметров из текста, который нужно проверить, умножается на соответствующий коэффициент. Сумма этих коэффициентов делится на общее количество слов. Таким образом сравнивается коэффициент проверяемого текста и корпуса мошенников. Если первый коэфициент больше либо равен коэффициенту второго, то скорее всего проверяемый текст был написан с целью мошенничества.

Данный репозиторий может быть усовершенствован добавлением новых параметров. Например, проверкой имён и фамилий как на латиннице, так и на кириллице (соотвутствующие файлы уже лежат на гите).

Корпус с текстами мошенников (base_text.txt) находится в свободном доступе. Корпус с текстами юзера, если вы решите дальше дорабатывать данный проект, необходимо составить самостоятельно (например, скачать необходимое количество диалогов из мессенджеров, запарсить их и перевести в человекочитаемый вид (json_parser.py вам в помощь)).

======

Necessary files for work:
---
If you only need to check the text:

Pip install modules in requirements.txt

fraud_detector.py
text_inputer.py
text_checker.py
text_comparer.py

russian_words.txt
russian_ban_words.txt
russian_trigger_words.txt
english_words.txt
english_trigger_words.txt

fraud_coef.pkl
coef.txt

---
If you want to work with your own corpus:

Add previous files

coef_calc.py

---
Optional:

text_serializer.py
json_parser.py
file_cryptor.py
