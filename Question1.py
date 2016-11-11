#You may need this https://support.google.com/accounts/answer/6010255
#Program to download emails using specific keyword in Subject.(Gmail API) 
import email
import getpass
import imaplib
import os

default_dir = '.' # save attachments to default dir: current
user = raw_input("Enter your Gmail username:")
password = getpass.getpass("Enter your password: ")

# https://docs.python.org/2/library/imaplib.html 
m = imaplib.IMAP4_SSL("imap.gmail.com")# connect to Server
m.login(user,password)
# we can check different folders by using m.list()
m.select("INBOX") # Choose a mailbox(folder)
# search for particular keyword in Subject. for example netflix, uber to download only those mails
# Inorder to download based on Sender you and use 'From' instead of 'Subject'
resp, items = m.search(None, 'Subject', '"UBER"')
items = items[0].split()

for emailid in items:
    resp, data = m.fetch(emailid, "(RFC822)") # RFC822 is used to get whole email
    email_body = data[0][1]
    mail = email.message_from_string(email_body)
    
    for part in mail.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True)
            f = open('Download_file', 'a+')
            f.write("["+mail["From"]+"] :" + mail["Subject"])
            f.write("Body:"+ body)
	    f.write("\n ************ \n")
            f.close()            
        if part.get_content_maintype() == 'multipart':
            continue

        # Check if Attachment
        if part.get('Content-Disposition') is None:
            continue

        filename = mail["From"]
        
        att_path = os.path.join(default_dir, filename)

        #Check if its already there
        if not os.path.isfile(att_path) :
            # finally write the stuff
            fp = open(att_path, 'wb')
            fp.write(part.get_payload(decode=True))
            fp.close()
