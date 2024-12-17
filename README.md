# Apartment Availability Checker

This script automates checking apartment availability from the Boise State University housing website and sends email notifications when new apartments are available.

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Scheduling](#scheduling)
- [License](#license)

---

## Description
The script scrapes apartment availability data from the Boise State University housing webpage and notifies specified recipients if apartments are available. It runs periodically using the APScheduler library.

---

## Features
- Scrapes apartment availability information from the Boise State University housing website.
- Sends email notifications if apartments are available.
- Provides detailed email updates with available apartment details.
- Supports automated scheduling (runs at 2:00 AM daily by default).

---

## Prerequisites
1. Python 3.8+
2. Gmail account with **App Password** enabled (for sending emails)
3. Required libraries:
    - `requests`
    - `beautifulsoup4`
    - `pandas`
    - `smtplib` (built-in)
    - `email` (built-in)
    - `apscheduler`

You can install the required libraries using:

```bash
pip install -r requirements.txt
```

---

## Installation
Clone the repository or download the script:

```bash
git clone <repository_url>
cd <project_directory>
```

---

## Usage
1. **Setup your Gmail App Password**
    - Go to your Google Account -> Security.
    - Enable 2-Step Verification.
    - Generate an App Password (e.g., for "Mail" and "Other").

2. **Run the Script**:

Use the following command with recipient email addresses:

```bash
python apartment_checker.py --emails email1@example.com email2@example.com
```

Replace `email1@example.com email2@example.com` with the target email addresses where notifications should be sent.

---

## Scheduling
The script uses APScheduler to run automatically at **2:00 AM daily**. You can adjust the timing in this block:

```python
scheduler.add_job(job, 'cron', hour=2, minute=0, args=[target_emails])
```

For example, to run at 6:30 PM daily:

```python
scheduler.add_job(job, 'cron', hour=18, minute=30, args=[target_emails])
```

---


## License
This project is licensed under the MIT License. Feel free to modify and distribute!

---

## Troubleshooting
- Ensure your Gmail account has **App Passwords** enabled.
- Check if your libraries are installed correctly using `pip list`.
- Verify the webpage URL (`https://www.boisestate.edu/housing-apartments/apartments-availability/`) is accessible.
- Enable "Allow Less Secure Apps" in your Gmail account settings (if required).

---

## Author
Desmond Kofi Boateng

---

**Enjoy automated apartment availability updates!**
