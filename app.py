from flask import Flask, jsonify, request
from scrapper import go_to_instagram
from flask_cors import CORS
from comments import load_comments, webdriver,\
    load_dict_contractions, load_dict_smileys

global chrome_driver, contractions,\
        smileys, comments, page_id

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "hello there"})


@app.route("/<string:post_id>", methods=["GET"])
def analyse_comments(post_id):
    global chrome_driver, contractions,\
        smileys, comments, page_id
    if request.method == "GET":
        try:
            page_id = int(request.args.get("pageId", 0))
            if post_id not in comments:
                chrome_driver.get(f"https://instagram.com/p/{post_id}")
                comments[post_id] = []
            if page_id == len(comments[post_id]):
                comments[post_id].append(
                    load_comments(chrome_driver, contractions, smileys, 12))
            response = comments[post_id][page_id]
        except Exception as e:
            print(e)
            response = {"Error Message": "some error"}
        return jsonify(response)

if __name__ == "__main__":
    chrome_driver = webdriver.Chrome()
    go_to_instagram(chrome_driver)
    contractions = load_dict_contractions()
    comments = {}
    smileys = load_dict_smileys()
    app.run(debug=False)