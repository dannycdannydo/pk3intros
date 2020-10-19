import imaplib
import mailparser


def get_email_data():
    return_data =[]
    EMAIL = 'pk3agency1@gmail.com'
    PASSWORD = 'sKLC#9aqMr'
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
        }
        for response_part in data:
            if isinstance(response_part, tuple):
                mail = mailparser.parse_from_bytes(response_part[1])
                messagedata["message_body"] = mail.text_plain[0][0:mail.text_plain[0].index("<")]
                recipcount = 1
                for i in mail.from_[0]:
                    if "daniel" in i.lower():
                        messagedata["message_from"] = "Daniel Campbell"
                    if "james" in i.lower():
                        messagedata["message_from"] = "James Kinsler"
                    if "mark" in i.lower():
                        messagedata["message_from"] = "Mark Powell"
                for i in mail.to[0]:
                    if "pk3" in i.lower():
                        continue
                    if "@" in i.lower():
                        messagedata["message_recipient"].append(
                                                                     {"email": i.lower(),
                                                                      "name": i[0:i.index("@")],
                                                                      "org": i[i.index("@") + 1:i.index(".")]
                                                                      }
                        )
                        recipcount += 1
                messagedata["message_date"] = mail.date
                messagedata["message_subject"] = mail.subject
                return_data.append(messagedata)
    return return_data