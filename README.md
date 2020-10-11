# AU-Announcement

Pulls announcements from comp.eng.ankara.edu.tr/category/duyuru and mails the new ones.

## Password and emails

Create a file named "secrets.py" at the same location with main.py and add following lines:

* secrets.py
```py
sender_email = "yourSender@gmail.com" #you need to use a gmail account as sender email
receiver_email = "yourReceiverMail"
password = "passOfSenderMail"
```
## Less secure apps & your Google Account

Open the [allow less secure apps page](https://myaccount.google.com/lesssecureapps) and turn it on.

## Warning!

Please don't make any changes on last_url.txt
