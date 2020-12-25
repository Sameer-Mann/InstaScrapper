# InstaScrapper
Uses Selenium to Automate The Chrome Browser<br>
To Install Requirements Use<br>
```
pip install -r requirements.txt
```
# Scrapper.py
It contains functions that are used to extract images and the selenium driver class that provides saving of cookies.

# Comments.py
This file contains the functions for extracting the no. of comments you want(load_comments).

# How To Use
```
python app.py
```
This runs the flask api and logins to instaram (username and password should be set as environment variables with names: USERNAME_INSTA and PASSWORD_INSTA) and also saves the cookies.<br>

After the api is running navigate to the angular directory and run
```
ng serve
```
This will run the angular frontend(may take some seconds).In the input dialog box provide a post_id and click on load comments and it will load the comments below as a unordered list
