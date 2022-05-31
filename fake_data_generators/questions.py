import json
import random
from exams.models import Subject, Question, Option

f = open('CompilerDesign.json')
data = json.load(f)

subject = Subject.objects.create(title='Compiler Design', description='Compiler design principles provide an in-depth view of translation and optimization process. Compiler design covers basic translation mechanism and error detection & recovery. It includes lexical, syntax, and semantic analysis as front end, and code generation and optimization as back-end.')

for idx, x in enumerate(data):
    question = Question.objects.create(question_text=x['question'], order=idx+1, subject=subject, score=5)
    option_1 = Option.objects.create(question=question, option_text=x['option_1'])
    option_2 = Option.objects.create(question=question, option_text=x['option_2'])
    option_3 = Option.objects.create(question=question, option_text=x['option_3'])
    option_4 = Option.objects.create(question=question, option_text=x['option_4'])

    random_option = random.choice([option_1, option_2, option_3, option_4])
    random_option.is_correct = True
    random_option.save()


f.close