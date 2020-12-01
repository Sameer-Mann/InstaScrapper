from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import requests
import os

from pickle import load,dump

class selenium_driver(object):
    """
    Provides saving session info support.
    Stores the seesion in binary format so it cannot be
    misused
    """
    def __init__(self,cookies_path,allowed_domains=[".instagram.com"]):
        self.options = webdriver.ChromeOptions()
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.maximize_window()
        self.domains = allowed_domains
        self.cookies_path = cookies_path
        self.cookies = []
        try:
            if "cookies" in os.listdir(cookies_path):
                cookie_path = os.path.join(cookies_path,"cookies")
                for cookie in load(open(cookie_path,"rb")):
                    self.cookies.append(cookie)
        except Exception as e:
            print(e)

    def go_to_site(self,url):
        domain = url.split("www")[1].split("/")[0]
        self.driver.get(url)
        flag=False
        for cookie in self.cookies:
            if cookie["domain"] == domain:
                self.driver.add_cookie(cookie)
                flag=True
        if flag:
            self.driver.get(url)

    def save_cookies(self):
        cookies = self.driver.get_cookies()
        for cookie in cookies:
            if cookie not in self.cookies:
                self.cookies.append(cookie)
        dump(self.cookies,open("cookies","wb"))

    def close_all(self):    
        if len(self.driver.window_handles) < 1:
            return
        for window_handle in self.driver.window_handles[:]:
            self.driver.switch_to.window(window_handle)
            self.driver.close()

    def quit(self):
        self.save_cookies()
        self.close_all()
        self.driver.quit()

def is_logged_in(driver):
    logged_in = True
    try:
        driver.find_element_by_css_selector(
            "input[aria-label='Phone number, username, or email']")
    except NoSuchElementException:
        logged_in=False
        pass
    return logged_in

def login_to_instagram(driver):
    user = WebDriverWait(driver,3).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR,
                "input[aria-label='Phone number, username, or email']")
        ))
    password = driver.find_element_by_css_selector(
        "input[aria-label='Password']")
    login_btn = driver.find_element_by_css_selector("button")
    ActionChains(driver).move_to_element(user)\
        .click().send_keys(os.getenv("USERNAME_INSTA")).perform()
    ActionChains(driver).move_to_element(password)\
        .click().send_keys(os.getenv("PASSWORD_INSTA")).perform()
    login_btn.click()
    try:
        save_info_selector = "main>div>div>div>section>div>button"
        WebDriverWait(driver,3).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                "main>div>div>div>div:nth-child(1)")
        )).click()
        sleep(2)
        noNotificationSelector = "div[role='dialog']>div>div>div:nth-child(3)>button:last-child"
        try:
            driver.find_element_by_css_selector(noNotificationSelector).click()
        except NoSuchElementException:
            driver.find_element_by_css_selector(
                "div[role='dialog']>div>div>div:nth-child(3)>button\
                    :nth-child(2)").click()
    except NoSuchElementException:
        pass


def get_image_and_comments(driver):
    # url,[comments]
    # comments : username,text
    return_url = ""
    comments = []
    tp = "img"
    likes = ""
    try:
        image_area = driver.find_element_by_css_selector(
            "div[role='dialog']>article>:nth-child(3)")
        comment_area = driver.find_element_by_css_selector(
            "div[role='dialog']>article>:nth-child(4)")
        try:
            img = image_area.find_element_by_css_selector("div>img")
            url = img.get_property("src")
            likes = comment_area.find_element_by_css_selector(
                "div[class]>button>span").text
            return_url = url
        except NoSuchElementException:
            return return_url, comments, likes, tp
            # image_area = self.driver.find_element_by_css_selector(
            # "div[role='dialog']>article>:nth-child(3)")
            # url = image_area.find_element_by_css_selector("div>video")\
            # .get_property("url")
            # return_url = url
            # tp="video"
            # likes = comment_area.find_elements_by_css_selector(
            # "div[class]>span>span")[2].text
        comments_list = comment_area.find_elements_by_css_selector(
            "div[class]>ul>ul")
        for comment in comments_list[1:]:
            username = comment.find_element_by_css_selector(
                "div>a").get_property("href")
            username = username.split("/")[-2]
            message = comment.find_element_by_css_selector(
                "div>li>div>div:first-child>div:nth-child(2)>span").text
            message.replace(",", " ").replace("\n", " ")
            comments.append((username, message))
    except NoSuchElementException:
        pass
    return return_url, comments, likes, tp


def finite_scroll(driver, to_download):
    SCROLL_PAUSE_TIME = 4.5
    total = 1000
    f1 = open("likes.csv", "a+")
    f1.write("id,likes\n")
    f2 = open("comments.csv", "a+")
    f2.write("id,username,comment\n")
    for times in range(total):
        sleep(1.2)
        url, comments, likes, tp = get_image_and_comments(driver)
        if url != "":
            likes = int("".join(likes.split(",")))
            if to_download:
                if tp == "img":
                    data = requests.get(url)
                    if data.status_code == 200:
                        with open(f"{times}.jpg", 'wb') as f:
                            f.write(data.content)

                else:
                    r = requests.get(url, stream=True)
                    with open(f"{times}.mp4", 'wb') as f:
                        for chunk in r.iter_content(chunk_size=1024*1024):
                            if chunk:
                                f.write(chunk)
            f1.write(f"{times},{likes}\n")
            for comment in comments:
                f2.write(f"{times},{comment[0]},{comment[1]}\n")
            print(f"Iteration {times}")
            print(*comments)
        next_btn = driver.find_element_by_css_selector(
            "div[role='dialog']>div>div>div>a:last-child")
        if next_btn is None:
            break
        next_btn.click()
        sleep(SCROLL_PAUSE_TIME)
    f1.close()
    f2.close()


if __name__ == '__main__':
    driver = selenium_driver()
    driver.go_to_site("https://www.instagram.com")
    if not logged_in():
        login_to_instagram(driver.driver)
    try:
        username = input("Enter a Username\n").strip()
        to_download = input(
            "Do you want to download the images:\n(y/n):\n").lower() == "y"
        driver.driver.get(f"https://www.instagram.com/{username}")
        sleep(2.5)
        driver.driver.find_element_by_css_selector(
            "main>div>div:last-child>article>div>div>div>div>a").click()
        sleep(1)
        driver.finite_scroll(to_download)
    except Exception as e:
        print(e)
    driver.quit()
