from selenium import webdriver
from time import sleep

from json_scraper import question_indexed_answer_tags,question_answers_marked

import json

if __name__ == '__main__':
    #driver = webdriver.Chrome("trivia_scraper/chromedriver")


    #driver.get("https://www.google.com/")
    #sleep(5)

    #driver.quit()
    print("hello world")

    all_trivia = []

    #from json_files
    json_files = []
    json_files = json_files + [question_indexed_answer_tags("data/arts_and_literature.json",{"source": "open_trivia_database","catagory":"arts,literature"})]
    json_files = json_files + [question_answers_marked("data/DB.json",{"source":"kaggel"})]

    for json_file in json_files:
        for i in json_file.get_trivia():
            all_trivia.append(i)
    


    #web scraping
        #skiped
    #saving raw_data to file

    with open('data/all.json','w') as f:
        json.dump(list(map(lambda x:x.toDict(),all_trivia)),f)

