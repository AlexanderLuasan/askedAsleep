
import json
class trivia:
    def __init__(self,question_text,choices = [], correct_answer = 0, meta = {}) -> None:
        self.question_text = question_text
        self.choices = choices
        self.correct_answer = correct_answer
        self.meta = meta

    def __str__(self):
        return f"{self.question_text} : \n\t {self.correct_answer} ({','.join(self.choices)})"

    def toDict(self):
        return dict({
            "question_text":self.question_text,
            "choices":self.choices,
            "answer": self.correct_answer,
            "meta": self.meta
        })
    def fromDict(dict_obj):
        try:
            return trivia(
                dict_obj["question_text"],
                dict_obj["choices"],
                dict_obj["answer"],
                dict_obj["meta"])
        except Exception as e:
            print(dict_obj)
            raise e

        