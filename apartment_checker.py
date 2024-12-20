import requests
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.message import EmailMessage
import logging
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
import argparse

logging.basicConfig(level=logging.INFO)

def send_email(subject, body, target_emails):
    logging.info(f"Sending email to {', '.join(target_emails)} regarding error")
    email_address = 'capewesley1@gmail.com'
    email_password = 'szlu cyer vcdo wyna'
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = f"{body}\n\nEmail sent on: {current_time}"
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

def check_apartment_availability(target_emails):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        body = f"Available apartments in University as at {current_time}: \n{df.to_string()}"
        send_email("Apartments Available", body, target_emails)
    else:
        send_email("No Apartments Available in University Village", f"There are no apartments available as at {current_time}.", target_emails)

def job(target_emails):
    check_apartment_availability(target_emails)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Apartment Availability Checker")
    parser.add_argument(
        '--emails',
        nargs='+',
        required=True,
        help='List of recipient email addresses (space-separated)'
    )
    args = parser.parse_args()
    target_emails = args.emails

    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', hour=2, minute=0, args=[target_emails])
    scheduler.start()

