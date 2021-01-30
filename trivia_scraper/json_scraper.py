

from utils import meta_dict_combo
from trivia import trivia
import json

class json_style:
    def __init__(self,file_name,meta_dict = {}):
        self.file_name = file_name
        self.meta_dict = meta_dict
    def get_trivia(self):
        raise NotImplemented


open_trivia_database = "https://github.com/el-cms/Open-trivia-database"
class question_indexed_answer_tags(json_style):

    def get_trivia(self):
        data = None
        with open(self.file_name,'r') as f:
            data = json.load(f)
        
        end = []
        for question in data:
            quesiton_text = question['question']
            choices = question['answers']
            answer = choices[question['answer']]
            other_tags = question['tags'] 
            end.append(trivia(quesiton_text,choices,answer,meta_dict_combo(self.meta_dict.copy(),{"catagory":",".join(other_tags)})))
        return end
kaggle = "https://www.kaggle.com/theriley106/hq-trivia-question-database"    
class question_answers_marked(json_style):

    def get_trivia(self):
        data = None
        with open(self.file_name,'r') as f:
            data = json.load(f)
        
        end = []
        for question in data:
            
            quesiton_text = question['question']
            choices = list(map(lambda x: x["text"], question['answers']))
            try:
                answer = list(filter(lambda x: x["correct"]==True, question['answers']))[0]["text"]
            except IndexError:
                continue
            end.append(trivia(quesiton_text,choices,answer,meta_dict_combo(self.meta_dict.copy(),{})))
        return end




if __name__ == '__main__':
    a = question_indexed_answer_tags("data/arts_and_literature.json",{"source": "open_trivia_database","catagory":"arts,literature"})
    b = question_answers_marked("data/DB.json",{"source":"kaggel"})
    for i in b.get_trivia():
        print(i)