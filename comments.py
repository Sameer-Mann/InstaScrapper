from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from scrapper import go_to_instagram
from emoji import demojize

from json import load
from re import sub
from time import sleep
from random import randint
import sys

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# git branch -M main
# git push -u origin main
def cleaning_comment(comment,CONTRACTIONS,SMILEY):
    comment = sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", "", comment)
    comment = ' '.join(sub("(\w+:\/\/\S+)", " ", comment).split())
    comment = sub("[\.\,\!\?\:\;\-\=]", "", comment)
    # comment = comment.lower()
    comment = comment.replace("’","'")
    words = comment.split()
    reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
    comment = " ".join(reformed)
    words = comment.split()
    reformed = [SMILEY[word] if word in SMILEY else word for word in words]
    comment = " ".join(reformed)
    comment = demojize(comment)
    comment = comment.replace(":"," ").replace("_"," ")
    comment = sub("[^A-Za-z0-9\s]","",comment)
    comment = ' '.join(comment.split())
    return comment


def scroll(driver):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div>ul>li>div>button"))
        )
        element.click()
        sleep(randint(1,6))
    except:
        pass


def load_comments(driver,CONTRACTIONS,SMILEY,no_of_comments=500):
    comments = []
    no_of_iterations = no_of_comments//12 + int(no_of_comments%12 > 0)
    try:
        for _ in range(no_of_iterations):
            comments_list = driver.find_elements_by_css_selector("div>ul>ul")
            for comment in comments_list:
                text = comment.find_element_by_css_selector("div>span:nth-child(2)").text
                cleaned = cleaning_comment(text,CONTRACTIONS,SMILEY)
                if len(cleaned):
                    comments.append(cleaned)
            driver.execute_script("document.querySelectorAll('div>ul>ul').forEach(obj=>obj.remove());")
            scroll(driver)
    except NoSuchElementException:
        pass
    return comments


def load_dict_smileys():
    
    return load(open("emoticon.json","r"))


def load_dict_contractions():
    
    return load(open("contractions.json","r"))


def write_data(comments,fname):
    analyser = SentimentIntensityAnalyzer()
    with open(f"{fname}.csv","w") as f:
        f.write("comment,negative,neutral,positive,compound\n")
        for i,comment in enumerate(comments):
            f.write(",".join([comment]+[*map(str,analyser.polarity_scores(comment).values())])+"\n")



if __name__ == "__main__":
    post_url = sys.argv[2]
    CONTRACTIONS = load_dict_contractions()
    SMILEY = load_dict_smileys()
    driver = webdriver.Chrome()

    go_to_instagram(driver)
    driver.get(post_url)

    comments = load_comments(driver,CONTRACTIONS,SMILEY)
    fname = post_url.split("/")[-2]
    
    write_data(comments,fname)