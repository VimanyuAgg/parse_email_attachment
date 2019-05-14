import email
import imaplib
import os
import config
import logging
import datetime
import traceback
import sys
import base64

today_date = str(datetime.datetime.now()).split(" ")[0]
current_path = os.path.dirname(os.path.realpath(__file__))

current_quarter = ''
current_month = int(today_date.split("-")[1])
if current_month <= 3:
    current_quarter = '01'
elif current_month <= 6:
    current_quarter = '02'

elif current_month <= 9:
    current_quarter = '03'

elif current_month <= 12:
    current_quarter = '04'

if sys.argv[1] == 'skills':
    SUBJECT = 'Scheduled report: Skills_Data_vim_pipeline'
    BASEFILE = 'Skills_Data_vim_pipeline_report.csv'
    SUBKEY = 'skills_data'
    FINAL_CSV = "skills_data_cleaned_{}.csv".format(today_date)

elif sys.argv[1] == "user_demographic":
    SUBJECT = 'Scheduled report: User Demographics PS Consultants v1_vim_pipeline'
    BASEFILE = 'User_Demographics_PS_Consultants_v1_vim_pipeline_report.csv'
    SUBKEY = 'user_demographic'
    FINAL_CSV = "user_demographic_data_cleaned_{}.csv".format(today_date)

# if sys.argv[1] == 'finance':
#
#
# if sys.argv[1] == 'all_project':
#     SUBJECT = 'Scheduled report: All projects v3_rag_vim_pipeline'
#     BASEFILE = 'All_projects_v3_rag_dashboard_vim_pipeline_report.csv'
#     SUBKEY = 'rag_status/all_project'
#     FINAL_CSV = "All_Projects_Cleaned_{}.csv".format(today_date)


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

info_handler = logging.FileHandler(os.path.join(current_path + "/logs/", today_date + '-info.log'))
info_handler.setLevel(logging.INFO)

error_handler = logging.FileHandler(os.path.join(current_path + "/logs/", today_date + '-error.log'))
error_handler.setLevel(logging.ERROR)

debug_handler = logging.FileHandler(os.path.join(current_path + "/logs/", today_date + '-debug.log'))
debug_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info_handler.setFormatter(formatter)
error_handler.setFormatter(formatter)
debug_handler.setFormatter(formatter)

logger.addHandler(info_handler)
logger.addHandler(error_handler)
logger.addHandler(debug_handler)


class FetchEmail():

    connection = None
    error = None
    mail_server="imap-mail.outlook.com"
    username= ''
    password= ''
    # self.save_attachment(self,msg,download_folder)

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)
        self.connection.select('EmailJobs')  # so we can mark mails as read

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def save_attachment(self, msg, download_folder=os.path.join(current_path)):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)

        return: file path to attachment
        """
        try:

            att_path = "No attachment found."
            for part in msg.walk():
                print(type(part))
                if part.get_content_maintype() == 'multipart':
                    continue
                if part.get('Content-Disposition').find(BASEFILE) == -1:
                    continue

                filename = part.get_filename()
                print(filename)
                att_path = os.path.join(download_folder, filename)

                if not os.path.isfile(att_path):
                    fp = open(att_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
            return att_path
        except Exception as e:
            logger.error("EXCEPTION OCCURED: {}".format(e))
            logger.error(traceback.format_exc())

    def fetch_unread_messages(self):
        """
        Retrieve unread messages
        """
        try:

            emails = []
            subject = SUBJECT
            (result, messages) = self.connection.search(None,'(UNSEEN SUBJECT "%s")' % subject)
            messages = list(map(lambda x: x.decode('utf-8'), messages))
            if result == "OK":
                for message in messages[0].split(' '):
                    try:
                        ret, data = self.connection.fetch(message,'(RFC822)')
                    except:
                        print("No new emails to read.")
                        self.close_connection()
                        exit()

                    byte_msg = data[0][1]

                    msg = email.message_from_string(byte_msg.decode('utf-8'))

                    if isinstance(msg, str) == False:
                        emails.append(msg)
                    response, data = self.connection.store(message, '+FLAGS','\\Seen')

                return emails

            self.error = "Failed to retreive emails."
            return emails
        except Exception as e:
            logger.error("EXCEPTION OCCURED: {}".format(e))
            logger.error(traceback.format_exc())


def get_required_attachment():

    try:
        logger.info("starting RAG Status report get attachment")
        mail_server = "imap-mail.outlook.com"
        username = base64.b64decode(config.username).decode('utf-8')
        password = base64.b64decode(config.userpsw).decode('utf-8')
        logger.info("Connecting to outlook server")
        myEmail = FetchEmail(mail_server, username, password)
        logger.info("Email connection established - Fetching emails")
        unread = myEmail.fetch_unread_messages()
        logger.info("Email Fetch Successful")
        logger.info("Unread len: {}".format(len(unread)))
        print(len(unread))

        for e in unread:
            print(type(e))
            logger.info("type of object: {}".format(type(e)))
            logger.info(myEmail.save_attachment(e))
            print(myEmail.save_attachment(e))

        print("all done-got attachment")
        logger.info("all done - got attachment")
    except Exception as e:
        logger.error("EXCEPTION OCCURED: {}".format(e))
        logger.error(traceback.format_exc())


if __name__== "__main__":
    get_required_attachment()