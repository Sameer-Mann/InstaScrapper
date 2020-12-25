from flask import Flask, jsonify, request
from scrapper import selenium_driver
from flask_cors import CORS
from comments import load_comments, webdriver,\
    load_dict_contractions, load_dict_smileys,\
    get_image_url
import atexit
import os

global chrome_driver, contractions,\
        smileys, comments, page_id
chrome_driver = selenium_driver()
def OnExitApp(user):
    chrome_driver.quit()

atexit.register(OnExitApp,user="sameer")

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "hello there"})


@app.route("/<string:post_id>", methods=["GET"])
def analyse_comments(post_id):
    global chrome_driver, contractions,\
        smileys, comments, page_id
    try:
        page_id = int(request.args.get("pageId", 0))
        if post_id not in comments:
            chrome_driver.driver.get(f"https://instagram.com/p/{post_id}")
            comments[post_id] = []
        if page_id == len(comments[post_id]):
            comments[post_id].append(
                load_comments(chrome_driver.driver, contractions, smileys, 12))
        response = comments[post_id][page_id]
    except:
        response = {"Error Message": "some error"}
        return jsonify(response),404
    return jsonify(response)

@app.route("/image/<string:post_id>",methods=["GET"])
def image_url(post_id):
    global chrome_driver
    response = get_image_url(chrome_driver.driver)
    if response == "":
        return jsonify({"Error Message": "some error"}),404
    return jsonify(response)

if __name__ == "__main__":
    chrome_driver.go_to_site()
    contractions = load_dict_contractions()
    comments = {}
    smileys = load_dict_smileys()
    app.run(debug=False)