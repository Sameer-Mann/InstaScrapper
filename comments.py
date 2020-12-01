from selenium import webdriver
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


def cleaning_comment(comment, CONTRACTIONS, SMILEY):
    comment = sub(r"(@[A-Za-z0-9]+)|(#[A-Za-z0-9]+)|(\w+:\/\/\S+)",
                  " ", comment)
    comment = demojize(comment)
    mapping = {"’": "'", "!": "!"}
    def check(s):
        if s in CONTRACTIONS:
            return CONTRACTIONS[s]
        if s in SMILEY:
            return SMILEY[s]
        ns = ""
        for char in s:
            if char in mapping:
                ns += mapping[char]
            else:
                ns += char if char.isalnum() else " "
        return ns
    reformed = [check(word) for word in comment.split()]
    comment = " ".join(reformed)
    comment = sub(r"([^A-Za-z0-9\s]+)", "", comment)
    comment = " ".join(comment.split())
    return comment


def scroll(driver):
    try:
        WebDriverWait(driver, 4).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,"div>ul>li>div>button"))
        ).click()
    except (TimeoutError, NoSuchElementException):
        pass


def load_comments(driver, CONTRACTIONS, SMILEY, no_of_comments=500):
    comments = []
    no_of_iterations = no_of_comments//12 + int(no_of_comments % 12 > 0)
    try:
        WebDriverWait(driver, 3).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,"div>ul>ul"))
        )
        analyser = SentimentIntensityAnalyzer()
        for _ in range(no_of_iterations):
            comments_list = driver.find_elements_by_css_selector("div>ul>ul")
            for comment in comments_list:
                text = comment.find_element_by_css_selector(
                    "div>span:nth-child(2)").text
                cleaned = cleaning_comment(text, CONTRACTIONS, SMILEY)
                if len(cleaned):
                    d={"comment": cleaned}
                    d.update(analyser.polarity_scores(cleaned))
                    comments.append(d)
            driver.execute_script("document.querySelectorAll('div>ul>ul')\
                                .forEach(obj=>obj.remove());")
            scroll(driver)
    except (NoSuchElementException, TimeoutError):
        pass
    return comments


def load_dict_smileys():
    return load(open("emoticon.json", "r"))


def load_dict_contractions():
    return load(open("contractions.json", "r"))


def write_data_to_csv(comments, fname):
    with open(f"{fname}.csv", "w") as f:
        f.write(",".join(map(str, comments[0].keys())) + "\n")
        for obj in comments:
            f.write(",".join(map(str, obj.values())) + "\n")


if __name__ == "__main__":
    post_url = sys.argv[2]
    CONTRACTIONS = load_dict_contractions()
    SMILEY = load_dict_smileys()
    driver = webdriver.Chrome()

    go_to_instagram(driver)
    driver.get(post_url)

    comments = load_comments(driver, CONTRACTIONS, SMILEY)
    fname = post_url.split("/")[-2]

    write_data_to_csv(comments, fname)
