import sys
import requests
import smtplib
import creds
from datetime import datetime


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python apis_to_email.py EMAIL API")

    recipient_email = check_email(sys.argv[1])

    apis = ["guardian", "accuweather"]    
    api = check_api(apis, sys.argv[2])
    
    email_message = ""
    if api == 0:
        email_message = get_guardian_message()
    else:
        email_message = get_accuweather_message()

    send_email(creds.sender_email, creds.app_password, recipient_email, email_message)


def check_email(email):
    if "@" not in email or "." not in email:
        sys.exit("Invalid email address.")
    return email


def check_api(apis, api):
    for idx, i in enumerate(apis):
       if api == i:
           return idx 
    sys.exit("Invalid API.")


def get_guardian_response(api_key, tag):
    try:
        response = requests.get(f"https://content.guardianapis.com/search?q={tag}&api-key={api_key}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
            sys.exit(f"Failed to fetch data: {e}") 
        


def filter_guardian_data(data):
    articles = []
    for article in data["response"]["results"]:
        n = [] 
        n.append("    ".join(extract_datetime(article["webPublicationDate"])))
        n.append(article["webTitle"])
        n.append(article["webUrl"])
        articles.append(n)
    return articles


def format_guardian_message(data):
    text = ""
    for idx, article in enumerate(data):
        text += f"{idx+1}. "
        for item in article:
            text += f"{item}\n"
        text += "\n"
    return text


def get_accuweather_response(api_key, location_key):
    try:
        response = requests.get(f"http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/{location_key}?apikey={api_key}&metric=true")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        sys.exit(f"Failed to fetch data: {e}")


def filter_accuweather_data(response):
    hours = []
    for hour in response:
        n = []
        # [1] element gets only hours and minutes
        n.append(extract_datetime(hour["DateTime"])[1])
        n.append(f"{round(hour['Temperature']['Value'])} °C")

        hours.append(n)
    return hours


def format_accuweather_message(data):
    message = ""
    for i in data:
        message += f"{i[0]}\n       Temperature: {i[1]}\n\n"
    return message


def get_guardian_message():
    tag = "Ukraine"
    subject = f"Newest Guardian articles about {tag}"
    response = get_guardian_response(creds.guardian_api_key, tag)
    data = filter_guardian_data(response)
    message = format_guardian_message(data)
    return f"Subject: {subject}\n\n{message}"

        
def get_accuweather_message():
    city = "Kaunas"
    subject = f"Accuweather weather forecast for the upcoming 12 hours in {city}"
    response = get_accuweather_response(creds.accuweather_api_key, creds.kaunas_location_key)
    data = filter_accuweather_data(response)
    message = format_accuweather_message(data)
    return f"Subject: {subject}\n\n{message}" 


# extracts and separates date into first: yearly, and second: daytime
def extract_datetime(iso_datetime):
    dt_object = datetime.fromisoformat(iso_datetime.replace("Z", "+00:00"))
    date = dt_object.strftime("%Y-%m-%d")
    hours_minutes = dt_object.strftime("%H:%M")
    return date, hours_minutes


# def create_message(sender_email, receiver_email, subject, text):
#     message = MIMEMultipart("alternative")
#     message.attach(MIMEText(text, "plain"))
#     message["Subject"] = subject
#     message["From"] = sender_email
#     message["To"] = receiver_email
#     return message


def send_email(sender_email, app_password, recipient_email, email_message):
    try:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(sender_email, app_password)
        s.sendmail(sender_email, recipient_email, email_message.encode('utf-8'))
        s.quit()
        print("Email sent succesfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    main()


# my vscode shortcuts:
# ctrl + x 
# ctrl + ` 
# ctrl + \ 
# ctrl + p 
# ctrl + /  
