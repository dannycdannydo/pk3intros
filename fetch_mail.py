import imaplib
import re
import mailparser
from datetime import datetime
import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__
import codecs
import base64

def get_email_data():
    return_data =[]
    EMAIL = 'pk3agency1@gmail.com'
    PASSWORD = 'admctymaykkiuhxq'
    SERVER = 'imap.gmail.com'

    # connect to the server and go to its inbox
    email = imaplib.IMAP4_SSL(SERVER)
    email.login(EMAIL, PASSWORD)
    # we choose the inbox but you can select others
    email.select('inbox')

    # we'll search using the ALL criteria to retrieve
    # every message inside the inbox
    # it will return with its status and a list of ids
    # change to UNSEEN for working model
    status, data = email.search(None, 'ALL')
    # the list returned is a list of bytes separated
    # by white spaces on this format: [b'1 2 3', b'4 5 6']
    # so, to separate it first we create an empty list
    mail_ids = []
    # then we go through the list splitting its blocks
    # of bytes and appending to the mail_ids list

    for block in data:
        # the split function called without parameter
        # transforms the text or bytes into a list using
        # as separator the white spaces:
        # b'1 2 3'.split() => [b'1', b'2', b'3']
        mail_ids += block.split()

    # now for every id we'll fetch the email
    # to extract its content
    for i in mail_ids:
        # the fetch function fetch the email given its id
        # and format that you want the message to be
        status, data = email.fetch(i, '(RFC822)')
        # the content data at the '(RFC822)' format comes on
        # a list with a tuple with header, content, and the closing
        # byte b')'
        messagedata = {
            "message_body": None,
            "message_from": None,
            "message_subject": None,
            "message_recipient":[],
            "message_date": None,
            "message_attachments": [],
            "message_filename": None
        }
        for response_part in data:
            if isinstance(response_part, tuple):
                mail = mailparser.parse_from_bytes(response_part[1])
                messagedata["message_body"] = mail.text_plain[0][0:mail.text_plain[0].index("<")]
                for i in mail.from_[0]:
                    if "daniel" in i.lower():
                        messagedata["message_from"] = "Daniel Campbell"
                    if "james" in i.lower():
                        messagedata["message_from"] = "James Kinsler"
                    if "mark" in i.lower():
                        messagedata["message_from"] = "Mark Powell"
                recipcount = 1
                for i in mail.to[0]:
                    if "pk3" in i.lower():
                        continue
                    if "@" in i.lower():
                        backhalf = i[i.index("@"): len(i)]
                        messagedata["message_recipient"].append(
                                                                     {"email": i.lower(),
                                                                      "name": i[0:i.index("@")].upper(),
                                                                      "org": backhalf[1:backhalf.index(".")].upper()
                                                                      }
                        )
                        recipcount += 1
                messagedata["message_date"] = mail.date.strftime("%Y %m %d").replace(" ", "")
                messagedata["message_subject"] = mail.subject
                return_data.append(messagedata)
        now = datetime.now()
        filename = messagedata["message_subject"] + now.strftime("%m/%d/%Y, %H:%M:%S")
        messagedata["message_filename"] = re.sub('[^A-Za-z0-9]+', ' ', filename).replace(" ", "")
        f = open('%s/%s.eml' % ("emails", messagedata["message_filename"]), 'wb')
        f.write(data[0][1])
        uploadToStorage("emails/" + messagedata["message_filename"] + ".eml", messagedata["message_filename"] + ".eml")
        f.close()
        os.remove("emails/" + messagedata["message_filename"] + ".eml")
    return return_data

def uploadToStorage(filepath, filename):
    blobpath = filepath
    try:
        blob = BlobClient.from_connection_string(conn_str="DefaultEndpointsProtocol=https;AccountName=trakr;AccountKey=aYmghpgtLyvrbGRQnmG5Hzsdy3mVc9k3lssKMh4IOK3ci1M7VrgLb6/KqLIqvPNl/DlCWmL2B3RRWmlXWZykUg==;EndpointSuffix=core.windows.net", container_name="pk3intros",
                                                 blob_name=filename)
        with open(blobpath, "rb") as data:
            blob.upload_blob(data)
    except:
        print("Upload to Blob failed or File Already Exists in Storage")
        return(["fail",filepath])
    return()