




from text_cleaning import clean, question_frame,get_json_data
import pandas as pd
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

from sklearn.metrics.pairwise import linear_kernel

def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col,coo_matrix.data)
    return sorted(tuples,key=lambda x:(x[1],x[0]),reverse=True)



class text_minner():
    def __init__(self,question_table=pd.DataFrame()):

        self.question_table = question_table
        self.question_table["clean"] = list(map(lambda x:clean(x) , question_table["raw"].to_list()))

        self.all_text = self.question_table["clean"]

        #setup word counter

        stop = stopwords.words('english')

        self.count_vectorizer_transformer = CountVectorizer(max_df=0.85,stop_words = stop)
        self.word_count_vector = self.count_vectorizer_transformer.fit_transform(self.all_text)

        #get the tf_idf
        self.tf_idf_transformer = TfidfTransformer(smooth_idf=True,use_idf=True)
        self.tf_idf_quesiton_text_vectors = self.tf_idf_transformer.fit_transform(self.word_count_vector)

    

    def tf_idf_keywords(self,question_text,topn = 5):
        question_text = clean(question_text)

        tf_idf_vector = self.tf_idf_transformer.transform(self.count_vectorizer_transformer.transform([question_text]))
        best_word_index = sort_coo(tf_idf_vector.tocoo())[:topn]


        results = {}
        for idx,score in best_word_index:
            results[self.count_vectorizer_transformer.get_feature_names()[idx]] = round(score,3)
        return results
    
    def tf_idf_search(self,search_text,topn = 5):
        search_text =clean(search_text)

        tf_idf_vector = self.tf_idf_transformer.transform(self.count_vectorizer_transformer.transform([search_text]))


        similarity_scores = linear_kernel(tf_idf_vector,self.tf_idf_quesiton_text_vectors).flatten()

        results = {}
        for k,v in sorted([x for x in zip(similarity_scores,self.all_text)],reverse=True)[:topn]:
            results[v] = k
        return results
        
        


if __name__ == "__main__":
    question_frame = question_frame(get_json_data())
    
    t = text_minner(question_frame)


    question = 16
    print(question_frame["raw"][question])
    print(t.tf_idf_keywords(question_frame["raw"][question]))

    print(f"search: '{question_frame['raw'][question]}'")
    print(t.tf_idf_search(question_frame['raw'][question]))

    print(f"search: '{' '.join(question_frame['raw'][question].split(' ')[::2])}'")
    print(t.tf_idf_search(' '.join(question_frame['raw'][question].split(' ')[::2])))