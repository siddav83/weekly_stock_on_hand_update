from selenium import webdriver
from selenium.common.exceptions import WebDriverException  # Import for error handling
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from test_data import test_data

# Set Chrome driver path
chrome_driver_path = "./chromedriver/chromedriver.exe"

try:
    # Create Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"webdriver.chrome.driver={chrome_driver_path}")

    # Initialize Chrome driver
    driver = webdriver.Chrome(options=chrome_options)

    driver.implicitly_wait(10)  # Wait for elements to load

    # Navigate to website
    driver.get("")

    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "username"))
    )
    element.click()
    element.send_keys("sarah")

    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "password"))
    )
    element.click()
    element.send_keys("qeLp}akn7C*H")

    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']"))
    )
    element.click()

    element = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Products']"))
    )
    element.click()

    link = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "(//a[text()='Overview'])[2]"))
    )
    link.click()

    header = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "tableone"))
    )

   

    elements = driver.find_elements(By.XPATH, "//tr")

    data_list = []

    for element in elements:

        td_elements = element.find_elements(By.TAG_NAME, 'td')
    
        if len(td_elements) >= 4:
            td_2_data = td_elements[1].text.strip()
            td_4_data = td_elements[3].text.strip()
                
            data_list.append([td_2_data, td_4_data])

            # print(data_list)

    new_list =[]

    for check in test_data:
        for test in data_list:
            if check[0] == test[0]:
                new_list.append([test[0], check[1], test[1]])
                break  # Break out of the inner loop once a match is found
    
    print(new_list)


    csv_file = 'data.csv'

# Writing data to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_list)

    print(f"Data has been written to {csv_file}")

    email_sender = ''
    email_receiver = ''
    email_subject = 'CSV File Attachment'
    email_body = 'Please find the attached  stock on hand CSV file.'

    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = email_subject

    # Attach the CSV file
    with open(csv_file, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {csv_file}')
        msg.attach(part)

    # Attach email body
    msg.attach(MIMEText(email_body, 'plain'))

    # Connect to the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login('', '')

    # Send the email
    smtp_server.send_message(msg)
    smtp_server.quit()

    print('Email sent successfully.')


except WebDriverException as e:
    print("Error encountered:", e)
finally:
    # Ensure driver closure
    if driver:
        driver.quit()
