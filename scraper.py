import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.message import EmailMessage
import logging
from apscheduler.schedulers.blocking import BlockingScheduler

logging.basicConfig(level=logging.INFO)

def send_email(subject, body, target_emails=["desmondboateng@u.boisestate.edu", "alessiobarboni@u.boisestate.edu"]):
    logging.info(f"Sending email to {', '.join(target_emails)} regarding error")
    email_address = 'capewesley1@gmail.com'
    email_password = 'szlu cyer vcdo wyna'
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = ', '.join(target_emails)
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(email_address, email_password)
            smtp.send_message(msg)
        logging.info(f"Email sent: {subject}")
    except Exception as e:
        logging.error(f"Error: email not sent, continuing... {e}")

def check_apartment_availability():
    data = {
        "Community": ["No Apartments Currently Available"],
        "Apartment Type": ["No Apartments Currently Available"],
        "Date Available": ["No Apartments Currently Available"],
        "Status": ["No Apartments Currently Available"]
    }

    url = 'https://www.boisestate.edu/housing-apartments/apartments-availability/'
    response = requests.get(url)

    if response.status_code == 200:
        print('Request is successful')
    else:
        print('Request is unsuccessful')

    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    apartments_available = False

    try:
        rows = table.find_all('tr')

        for row in rows:
            cols = row.find_all('td')

            if len(cols) == 4:
                community = cols[0].get_text().strip()
                apartment_type = cols[1].get_text().strip()
                date_available = cols[2].get_text().strip()
                status = cols[3].get_text().strip()

                if "No Apartments Currently Available" in [community, apartment_type, date_available, status]:
                    continue
                else:
                    apartments_available = True

                    data["Community"].append(community)
                    data["Apartment Type"].append(apartment_type)
                    data["Date Available"].append(date_available)
                    data["Status"].append(status)
    except Exception as e:
        print(f"An error occurred: {e}")

    if apartments_available:
        df = pd.DataFrame(data)
        body = f"Available apartments in University: \n{df.to_string()}"
        send_email("Apartments Available", body)
    else:
        send_email("No Apartments Available in University Village", "Currently, there are no apartments available.")

def job():
    check_apartment_availability()

scheduler = BlockingScheduler()
scheduler.add_job(job, 'interval', minutes=10)
scheduler.start()
