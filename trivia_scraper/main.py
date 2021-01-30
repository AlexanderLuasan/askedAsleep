from selenium import webdriver
from time import sleep




if __name__ == '__main__':
    driver = webdriver.Chrome("/home/alexander/hackathons/askedAsleep/trivia_scraper/chromedriver")


    driver.get("https://www.google.com/")
    sleep(5)

    driver.quit
    print("hello world")