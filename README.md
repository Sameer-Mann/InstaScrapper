# InstaScrapper
Uses Selenium to Automate The Chrome Browser<br>
Requirements<br>
<ul>
<li>Python >= 3.7</li>
<li>Selenium</li>
</ul>

```
python scrapper.py
```

It Downloads the images in the same directory as the script. To turn off the download comment the lines 87-90.
Expects there to be 2 csv files<br>
comments.csv : image_id,username,comment_text<br>
likes.csv : image_id,no_of_likes

# Currently Cannot Video Files

# Requires An Instagram Account to run

username and password should be set as environment variables with names: USERNAME_INSTA and PASSWORD_INSTA
