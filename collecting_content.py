import os 
import re


def get_content():
    path = 'quiz-questions'
    for file in os.listdir(path):
        file_path = f'{path}/{file}'
        quiz_content = {}
        with open(file_path, 'r', encoding='KOI8-R') as file:
            text_parts = file.read().split('\n\n')
            for text_part in text_parts:
                if 'Вопрос' in text_part:
                    question = re.split(':', text_part, maxsplit=1)[1].replace('\n', ' ')
                if 'Ответ' in text_part:
                    answer = re.split(':', text_part, maxsplit=1)[1].replace('\n', ' ')
                    quiz_content[question] = answer
        return quiz_content
