# fraud-detector-project
This repository is designed to help determine if the text was written for the purpose of fraud. 

We have collected a corpus of texts based on written messages from scammers from various messengers, as well as a corpus based on the personal messages of the average user (encrypted to save personal data). 

Next, we searched for those parameters that could indicate whether the author of the text is a fraud. For example, the following turned out to be explicit markers: motivational verbs, trigger words, overly expressive symbols (!!!, ???, ?!?!), emoticons, etc.

After that, each corpus was programmatically analyzed. The optimal coefficients were calculated by the method of differential evolution (don't ask...).

Each list of parameters from the text to be checked is multiplied by the corresponding coefficient. The sum of these coefficients is divided by the total number of words. This compares the coefficient of the text being checked and the corpus of scammers. If the first coefficient is greater than or equal to the coefficient of the second, then most likely the text being checked was written for the purpose of fraud.

======

Этот репозиторий предназначен для того, чтобы помочь определить, был ли текст написан с целью мошенничества. 

Мы собрали корпус текстов, основанных на письменных сообщениях мошенников из различных мессенджеров, а также корпус, основанный на личных сообщениях среднестатического юзера (зашифрован для сохранения личных данных). 

Далее мы искали те параметры, которые могли бы свидетельствовать о том, является ли автор текста мошенником. Например, явными маркерами оказались следующие: побудительные глаголы, слова-триггеры, чрезмерные экспрессивные символы (!!!, ???, ?!?!), эмотиконы и т.д.

После этого каждый корпус был программно проанализирован. Оптимальные коэффициенты были высчитаны методом дифференциальной эволюции (не спрашивайте...).

Каждый список параметров из текста, который нужно проверить, умножается на соответствующий коэффициент. Сумма этих коэффициентов делится на общее количество слов. Таким образом сравнивается коэффициент проверяемого текста и корпуса мошенников. Если первый коэфициент больше либо равен коэффициенту второго, то скорее всего проверяемый текст был написан с целью мошенничества.

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
