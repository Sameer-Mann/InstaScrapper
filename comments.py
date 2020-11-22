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

# git branch -M main
# git push -u origin main
def cleaning_comment(comment,CONTRACTIONS,SMILEY):
    comment = sub("(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)", "", comment)
    comment = ' '.join(sub("(\w+:\/\/\S+)", " ", comment).split())
    comment = sub("[\.\,\!\?\:\;\-\=]", "", comment)
    comment = comment.lower()
    comment = comment.replace("’","'")
    words = comment.split()
    reformed = [CONTRACTIONS[word] if word in CONTRACTIONS else word for word in words]
    comment = " ".join(reformed)
    words = comment.split()
    reformed = [SMILEY[word] if word in SMILEY else word for word in words]
    comment = " ".join(reformed)
    comment = demojize(comment)
    comment = comment.replace(":"," ").replace("_"," ")
    comment = sub("[^A-Za-z\s]","",comment)
    comment = ' '.join(comment.split())
    return comment


def scroll(driver,no_of_times):
    for _ in range(no_of_times):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div>ul>li>div>button"))
            )
            element.click()
            sleep(randint(1,5))
        except:
            break


def load_comments(driver,CONTRACTIONS,SMILEY):
    comments = []
    scroll(driver,80)
    try:
        comments_list = driver.find_elements_by_css_selector("div>ul>ul")
        for comment in comments_list[1:]:
            text = comment.find_element_by_css_selector("div>span:nth-child(2)").text
            comments.append(cleaning_comment(text,CONTRACTIONS,SMILEY))
    except NoSuchElementException:
        pass
    return comments


def load_dict_smileys():
    
    return load(open("emoticon.json","r"))


def load_dict_contractions():
    
    return load(open("contractions.json","r"))


if __name__ == "__main__":
    post_url = sys.argv[2]
    CONTRACTIONS = load_dict_contractions()
    SMILEY = load_dict_smileys()
    driver = webdriver.Chrome()

    go_to_instagram(driver)
    driver.get(post_url)

    comments = load_comments(driver,CONTRACTIONS,SMILEY)
    fname = post_url.split("/")[-1]

    with open(f"{fname}.txt","w") as f:
        for i,comment in enumerate(comments):
            f.write(comment+"\n")
