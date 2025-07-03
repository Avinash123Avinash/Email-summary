import streamlit as st
import imaplib
import email
import re
import string
from datetime import datetime, timedelta
from email.mime.text import MIMEText
import email.utils
import time

def preprocess_text(text):
    url_pattern = re.compile(r'(https?://\S+|www\.\S+|\S+@\S+\.\S+)')
    text = url_pattern.sub(r'', text)
    
    html_pattern = re.compile('<.*?>|{.*}|\[.*?\]')
    text = html_pattern.sub('', text)
    
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def get_emails(username, password,days,num_emails,receive_mail):
    email_body = "Here is your Today's emails summary:\n\n\n\n"
    
    try:
        imap_server = imaplib.IMAP4_SSL(host='imap.gmail.com')
        imap_server.login(username, password)
        imap_server.select('inbox')

        today = datetime.today()
        last_week = today - timedelta(days=days)
        
        date_format = '%d-%b-%Y'
        last_week_str = last_week.strftime(date_format)

        search_query = f'(SINCE {last_week_str})'
        result, message_numbers = imap_server.search(None, search_query)

        if result != 'OK':
            st.error("Failed to search emails.")
            return

        for message_number in message_numbers[0].split()[:num_emails]:  
            status, msg_data = imap_server.fetch(message_number, '(RFC822)')
            if status != 'OK':
                continue

            raw_email = msg_data[0][1]
            message = email.message_from_bytes(raw_email)

            # Extract email details
            from_ = preprocess_text(message["from"])
            subject = message["subject"]
            date = message["date"]

            email_body += f'From : {from_}\nDate : {date}\nSubject : {subject}\n\n\n'










            

        st.text_area("Email Summary", email_body, height=300)
        st.success("Email summary created!")
        if receive_mail:
            msg = MIMEText(email_body)
            msg['Subject'] = "Today's email summary"
            msg['From'] = username
            msg['To'] = username
            msg['Date'] = email.utils.formatdate()

            # Append the summary email to the inbox
            imap_server.append('INBOX', '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())

    except Exception as e:
        st.error(f"An error occurred: {e}")
    
    finally:
        imap_server.logout()

st.title("Daily Email Summary")
username = st.text_input("Email Address:")
password = st.text_input("Password:", type="password")
days = st.selectbox("Select Days:",[1,2,3,4,5,6,7,8,9,10])
num_emails = st.selectbox("Number of Emails to Fetch:", [5, 10, 15, 20, 25])
receive_mail = st.checkbox("Receive Email Summary")


if st.button("Submit"):
    if username and password:
        get_emails(username, password,days,num_emails,receive_mail)
else:
    st.warning("Please enter both your email address and password.")






# import streamlit as st
# import imaplib
# import email
# import re
# import string
# from datetime import datetime, timedelta
# from email.mime.text import MIMEText
# import email.utils
# import time

# def preprocess_text(text):
#     url_pattern = re.compile(r'(https?://\S+|www\.\S+|\S+@\S+\.\S+)')
#     text = url_pattern.sub(r'', text)
    
#     html_pattern = re.compile('<.*?>|{.*}|\[.*?\]')
#     text = html_pattern.sub('', text)
    
#     text = text.translate(str.maketrans('', '', string.punctuation))
#     text = re.sub(r'\s+', ' ', text).strip()
    
#     return text

# def get_emails(username, password, days, num_emails, receive_mail):
#     email_body = "Here is your Today's emails summary:\n\n\n\n"
    
#     try:
#         imap_server = imaplib.IMAP4_SSL(host='imap.gmail.com')
#         imap_server.login(username, password)
#         imap_server.select('inbox')

#         today = datetime.today()
#         last_week = today - timedelta(days=days)
#         date_format = '%d-%b-%Y'
#         last_week_str = last_week.strftime(date_format)

#         search_query = f'(SINCE {last_week_str})'
#         result, message_numbers = imap_server.search(None, search_query)

#         if result != 'OK':
#             st.error("Failed to search emails.")
#             return

#         for message_number in message_numbers[0].split()[:num_emails]:  
#             status, msg_data = imap_server.fetch(message_number, '(RFC822)')
#             if status != 'OK':
#                 continue

#             raw_email = msg_data[0][1]
#             message = email.message_from_bytes(raw_email)

#             from_ = preprocess_text(message.get("from", ""))
#             subject = message.get("subject", "(No Subject)")
#             date = message.get("date", "(No Date)")

#             # Extract the email content
#             body = ""
#             if message.is_multipart():
#                 for part in message.walk():
#                     content_type = part.get_content_type()
#                     content_dispo = str(part.get("Content-Disposition"))
#                     if content_type == "text/plain" and "attachment" not in content_dispo:
#                         charset = part.get_content_charset() or 'utf-8'
#                         try:
#                             body += part.get_payload(decode=True).decode(charset, errors="ignore")
#                         except:
#                             body += "[Error decoding part]"
#             else:
#                 charset = message.get_content_charset() or 'utf-8'
#                 try:
#                     body = message.get_payload(decode=True).decode(charset, errors="ignore")
#                 except:
#                     body = "[Error decoding body]"

#             # Preprocess body text
#             body = preprocess_text(body)

#             email_body += f'From: {from_}\nDate: {date}\nSubject: {subject}\nContent:\n{body}\n\n{"-"*60}\n\n'

#         st.text_area("Email Summary", email_body, height=300)
#         st.success("Email summary created!")

#         if receive_mail:
#             msg = MIMEText(email_body)
#             msg['Subject'] = "Today's email summary"
#             msg['From'] = username
#             msg['To'] = username
#             msg['Date'] = email.utils.formatdate()
#             imap_server.append('INBOX', '', imaplib.Time2Internaldate(time.time()), msg.as_bytes())

#     except Exception as e:
#         st.error(f"An error occurred: {e}")
    
#     finally:
#         imap_server.logout()

# # UI Elements
# st.title("Daily Email Summary")
# username = st.text_input("Email Address:")
# password = st.text_input("Password:", type="password")
# days = st.selectbox("Select Days:", list(range(1, 11)))
# num_emails = st.selectbox("Number of Emails to Fetch:", [5, 10, 15, 20, 25])
# receive_mail = st.checkbox("Receive Email Summary")

# if st.button("Submit"):
#     if username and password:
#         get_emails(username, password, days, num_emails, receive_mail)
#     else:
#         st.warning("Please enter both your email address and password.")

