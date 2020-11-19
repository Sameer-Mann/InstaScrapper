from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
import requests
import os

global driver
driver = webdriver.Chrome()


def go_to_instagram():
    global driver
    driver.get('https://www.instagram.com/')
    driver.maximize_window()
    sleep(5)
    user = driver.find_element_by_css_selector("input[aria-label='Phone number, username, or email']")
    password = driver.find_element_by_css_selector("input[aria-label='Password']")
    login_btn = driver.find_element_by_css_selector("button")
    ActionChains(driver).move_to_element(user).click().send_keys(os.getenv("USERNAME_INSTA")).perform()
    sleep(2)
    ActionChains(driver).move_to_element(password).click().send_keys(os.getenv("PASSWORD_INSTA")).perform()
    sleep(2)
    login_btn.click()
    try:
        sleep(3)
        driver.find_element_by_css_selector("main>div>div>div>div:nth-child(2)").click()
        sleep(3)
        driver.find_element_by_css_selector("div[role='dialog']>div>div>div:nth-child(3)>button:nth-child(2)").click()
    except NoSuchElementException:
        pass


def get_image_and_comments():
    # url,[comments]
    # comments : username,text
    return_url = ""
    comments = []
    tp="img"
    likes = ""
    try:
        image_area = driver.find_element_by_css_selector("div[role='dialog']>article>:nth-child(3)")
        comment_area = driver.find_element_by_css_selector("div[role='dialog']>article>:nth-child(4)")
        

        try:    
            img = image_area.find_element_by_css_selector("div>img")
            url = img.get_property("src")
            likes = comment_area.find_element_by_css_selector("div[class]>button>span").text
            return_url = url
        except NoSuchElementException:
            return return_url,comments,likes,tp
            # image_area = driver.find_element_by_css_selector("div[role='dialog']>article>:nth-child(3)")
            # url = image_area.find_element_by_css_selector("div>video").get_property("url")
            # return_url = url
            # tp="video"
            # likes = comment_area.find_elements_by_css_selector("div[class]>span>span")[2].text

        comments_list = comment_area.find_elements_by_css_selector("div[class]>ul>ul")
        for comment in comments_list[1:]:
            username  = comment.find_element_by_css_selector("div>a").get_property("href")
            username = username.split("/")[-2]
            message = comment.find_element_by_css_selector("div>li>div>div:first-child>div:nth-child(2)>span").text
            message.replace(","," ")
            comments.append((username,message))

    except NoSuchElementException:
        pass

    return return_url,comments,likes,tp


def finite_scroll():
    SCROLL_PAUSE_TIME = 4.5
    times = 1
    total = 1000
    f1 = open("likes.csv","a+")
    f2 = open("comments.csv","a+")
    while True:
        sleep(1.2)
        url,comments,likes,tp = get_image_and_comments()
        if url != "":
            likes = int("".join(likes.split(",")))
            if tp == "img":
                data = requests.get(url)
                if data.status_code == 200:
                    with open(f"{times}.jpg",'wb') as f:
                        f.write(data.content)

            else:
                r = requests.get(url,stream=True)
                with open(f"{times}.mp4",'wb') as f:
                    for chunk in r.iter_content(chunk_size = 1024*1024): 
                        if chunk: 
                            f.write(chunk)
            f1.write(f"{times},{likes}\n")
            for comment in comments:
                f2.write(f"{times},{comment[0]},{comment[1]}\n")

        if times==total:
            break

        times += 1
        next_btn = driver.find_element_by_css_selector("div[role='dialog']>div>div>div>a:last-child")
        if next_btn is None:
            break
        next_btn.click()
        sleep(SCROLL_PAUSE_TIME)
    f1.close()
    f2.close()


go_to_instagram()

driver.get("https://www.instagram.com/upgrad_edu")
sleep(2.5)

# clicking the first image
driver.find_element_by_css_selector("main>div>div:last-child>article>div>div>div>div>a").click()
sleep(1)

finite_scroll()

# driver.close()