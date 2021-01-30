

from selenium import webdriver
from time import sleep
from trivia import trivia
from tqdm import tqdm
from utils import meta_dict_combo
bar_size = 100

class searchable_page:
    searched_links = []
    unsearched_links = []
    bar = tqdm(total = bar_size, desc="scraping")
    def __init__(self,url,meta_dict={}):
        self.url = url
        self.meta_dict = meta_dict
    def __str__(self):
        return f"{self.__class__.__name__} url:{self.url} "
    
    def get_unsearched_page():
        try:
            return searchable_page.unsearched_links.pop()
        except IndexError:
            return None


    def add_searchable_pages(new_pages):
        #check duplicates within the list
        index = 0
        while(index < len(new_pages)):
            second_index = index+1
            while(second_index<len(new_pages)):
                if(new_pages[index].url == new_pages[second_index].url):
                    del new_pages[index]
                    index + index-1
                    break
                second_index = second_index + 1
            index = index + 1
        ture_new_pages = filter(
            lambda page: page.url not in [i.url for i in searchable_page.searched_links],
            filter(
                lambda page: page.url not in [i.url for i in searchable_page.unsearched_links],
                new_pages
        ))
        

        searchable_page.unsearched_links.extend(list(ture_new_pages))
        searchable_page.refresh_bar()
    def refresh_bar():
        value = 0
        if(len(searchable_page.unsearched_links)+len(searchable_page.searched_links)>0):
            value = len(searchable_page.searched_links)/(len(searchable_page.unsearched_links)+len(searchable_page.searched_links))
        value = value * bar_size

        searchable_page.bar.n = int(value)
        searchable_page.bar.refresh()
    
    def get_questions_from_web_site(self,driver):
        driver.get(self.url)
        searchable_page.bar.set_description(f"searching: {self.url}")
        #add sub pages
        searchable_page.add_searchable_pages(self.sub_links(driver))

        new_trivia = [
            trivia(question,choices,answer,self.meta_dict.copy()) 
            for question,answer,choices in zip(self.questions(driver),self.correct_answers(driver),self.answers(driver))
        ]
        searchable_page.searched_links.append(self)
        return new_trivia

    #to make
    #ignore
    def sub_links(self,driver):
        raise NotImplemented()
    def questions(_,driver):
        raise NotImplemented()
    def answers(_,driver):
        raise NotImplemented()
    def correct_answers(_,driver):
        raise NotImplemented


class usefulltrivia_page(searchable_page):
    pass
    def sub_links(self,driver):#return a list of searchable pages and links
        subcats = driver.find_elements_by_css_selector("a.subcat")
        new_pages1 = list(map(lambda item: 
            usefulltrivia_page(item.get_attribute("href"),meta_dict_combo(self.meta_dict,{"catagory":item.text})),
            subcats
        ))

        other_pages = driver.find_elements_by_css_selector("ul.pagination li a")
        new_pages2 = list(map(lambda item: 
            usefulltrivia_page(item.get_attribute("href"),meta_dict_combo(self.meta_dict,{})),
            other_pages
        ))

        return new_pages1+new_pages2

    def questions(_,driver):#return text of questions on the page
        items = driver.find_elements_by_css_selector("div.mbr-article h2")

        return list(map(lambda x: x.text, items))
    def answers(_,driver):
        items = driver.find_elements_by_css_selector("div.mbr-buttons")

        answer_list = []
        for item in items:
            sub_buttons = item.find_elements_by_css_selector("a")
            answer_list.append((list(map(lambda x:x.text,sub_buttons))))
        return answer_list

    def correct_answers(_,driver):
        items = driver.find_elements_by_css_selector("div.mbr-buttons")

        answer_list = []
        for item in items:
            sub_buttons = item.find_elements_by_css_selector("a")
            for answer in sub_buttons:
                if(answer.get_attribute("onmousedown") == "ding.play()"):
                    answer_list.append(answer.text)
                    break
        return answer_list
        
    
        











if __name__ == '__main__':
    driver = webdriver.Chrome('/home/alexander/hackathons/askedAsleep/trivia_scraper/chromedriver')
    a = usefulltrivia_page('https://www.usefultrivia.com/sports_trivia/football_trivia_index.html',{"source":"usefultrivia","catagory":"football_trivia"})

    searchable_page.add_searchable_pages([a])

    questions = [] 
    full_search_path = []

    while( True ):
        next_page = searchable_page.get_unsearched_page()
        if(next_page == None):
            break
        #print(f"searching {next_page.url}")
        full_search_path.append(next_page.url)
        questions.extend(next_page.get_questions_from_web_site(driver))

    driver.quit()

    for i in questions:
        print(i)

    if(len(list(set(full_search_path)))!= len(full_search_path)):
        print("double searching")


