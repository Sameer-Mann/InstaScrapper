# InstaScrapper
Uses Selenium to Automate The Chrome Browser<br>
To Install Requirements Use<br>
```
pip install -r requirements.txt
```
```
python scrapper.py
```
Writes the output in 2 csv files<br>
comments.csv : image_id,username,comment_text<br>
likes.csv : image_id,no_of_likes

# Currently Cannot Handle Video Files

# Requires An Instagram Account to run

# Comments
This file extracts the no. of comments you want from a post and writes them to a file after cleaning them and also analyses the comments sentiments<br>
Outputs: post_id.csv : comment,negative,neutral,positive,compound <br>
username and password should be set as environment variables with names: USERNAME_INSTA and PASSWORD_INSTA
