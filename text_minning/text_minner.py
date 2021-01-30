




from text_cleaning import clean




class text_minner():
    def __init__(self,all_text=[]):

        self.all_text = list(map(lambda x:clean(x) , all_text))


    
