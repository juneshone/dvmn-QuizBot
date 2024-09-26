import os 
import re


def get_content(content_folder):
    quiz_content = {}
    for file in os.listdir(content_folder):
        file_path = os.path.join(content_folder, file)
        with open(file_path, 'r', encoding='KOI8-R') as content_file:
            text = content_file.read()
            text_parts = text.split('\n\n')
            for text_part in text_parts:
                if 'Вопрос' in text_part:
                    question = re.split(':', text_part, maxsplit=1)[1].replace('\n', ' ')
                if 'Ответ' in text_part:
                    answer = re.split(':', text_part, maxsplit=1)[1].replace('\n', ' ')
                    quiz_content[question] = answer
    return quiz_content
