from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client
import smtplib
from secrets import sender_email, receiver_email, password

def tr2ascii(raw_string):
    string = raw_string
    tr_chars = {'ç':'c', 'Ç':'C', 'ğ':'g', 'Ğ':'G', 'ı':'i', 'İ':'I', 'ö':'o', 'Ö':'O', 'ş':'s', 'Ş':'S', 'ü':'u', 'Ü':'U'}
    for src, target in tr_chars.items():
        string = string.replace(src, target)
    return string

def send_email(msg):
    sent_from = sender_email
    to = [receiver_email]
    subject = 'New Announcement | Yeni Duyuru'
    body_raw = tr2ascii(msg)
    body = body_raw.encode('ascii', 'ignore').decode('ascii')
    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(sender_email, password)
        server.sendmail(sent_from, to, email_text)
        server.close()

        print("Email sent!")
    except Exception as e:
        print('Failed to send email: '+ str(e))

def list2str(str_list):
    string = ""   
    for elem in str_list:  
        string += elem + "----------------------------------------------------------\n"
    return string
        


url_file = open("last_url.txt", "r")
file_urls = []
for file_url in url_file:
    print("The last url: " + file_url)
    file_urls.append(file_url)
url_file.close()

i = 1
post_urls = []
next = True
while next:
    page_url = "http://comp.eng.ankara.edu.tr/category/duyuru/page/" + str(i)
    uClient = uReq(page_url)
    page_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    containers = page_soup.findAll("div", {"class": "fusion-image-wrapper fusion-image-size-fixed"})
    pagination_containers = page_soup.findAll("div", {"class": "pagination clearfix"})
    next = "Sonraki" in pagination_containers[0].text
    i = i + 1
    for container in containers:
        container_url = container.a["href"]
        if len(file_urls) == 0:
            print(container_url)
            post_urls.append(container_url)
        elif not(container_url in file_urls[0]):
            print(container_url)
            post_urls.append(container_url)
        else:
            next = False
            break


if len(post_urls) != 0:
    url_file = open("last_url.txt", "w")
    url_file.write(post_urls[0])
    url_file.close()

post_contents = []
for post_url in post_urls:
    print(post_url)
    uClient = uReq(post_url)
    post_soup = soup(uClient.read(), "html.parser")
    uClient.close()
    title = post_soup.title.text
    post_containers = post_soup.findAll("div", {"class": "post-content"})
    print(title + "\n\n" + post_containers[0].text)
    post_contents.append(title + "\n\n" + post_containers[0].text)

if len(post_contents) > 0:
    msg = list2str(post_contents)
    send_email(msg)
else:
    print("Nothing new!")