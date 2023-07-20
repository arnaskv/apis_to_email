import sys
import requests
import smtplib
import creds
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python apis_to_email.py EMAIL API")
 
    sender_email = "legarnas@gmail.com"

    receiver_email = check_email(sys.argv[1])

    apis = ["guardian", "accuweather"]    
    api = check_api(apis, sys.argv[2])
    
    data = []
    subject = ""
    if api == 0:
        tag = "ukraine"
        subject = f"Guardian articles about {tag}:\n\n"
        data = extract_guardian_data(get_guardian_data(creds.guardian_api_key))
    elif api == 1:
        subject = "Accuweather forecast:\n\n"
    else:
        sys.exit("Invalid API.")

    text = format_guardian_data(data)

    message = create_message(sender_email, receiver_email, subject, text)
    send_email(sender_email, creds.app_password, receiver_email, message)


def check_email(email):
    if "@" not in email or "." not in email:
        sys.exit("Invalid email address.")
    return email


def check_api(apis, api):
    for idx, i in enumerate(apis):
       if api == i:
           return idx 


def get_guardian_data(api_key):
    response = requests.get(f"https://content.guardianapis.com/search?q=ukraine&api-key={api_key}")
    return response.json()


def extract_guardian_data(data):
    articles = []
    for article in data["response"]["results"]:
        n = [] 
        n.append(article["webPublicationDate"]) 
        n.append(article["webTitle"])
        n.append(article["webUrl"])
        articles.append(n)
    return articles


def format_guardian_data(data):
    text = ""
    for idx, article in enumerate(data):
        text += f"{idx+1}. "
        for item in article:
            text += f"{item}\n"
        text += "\n"
    return text


def get_accuweather_data(api_key):
    pass


def extract_accuweather_data(data):
    pass


def create_message(sender_email, receiver_email, subject, text):
    message = MIMEMultipart("alternative")
    message.attach(MIMEText(text, "plain"))
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email
    return message


def send_email(sender_email, app_password, receiver_email, message):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_email, app_password)
    s.sendmail(sender_email, receiver_email, message.as_string())
    s.quit()


if __name__ == "__main__":
    main()


# my vscode shortcuts:
# ctrl + x 
# ctrl + ` 
# ctrl + \ 
# ctrl + p 
# ctrl + /  