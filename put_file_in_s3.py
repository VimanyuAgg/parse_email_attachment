import boto3
import config
import get_attachment
import manipulate_csv
import os
import datetime
import logging
import traceback
import send_email

today_date = str(datetime.datetime.now()).split(" ")[0]
current_path = os.path.dirname(os.path.realpath(__file__))


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

logger.info("initiating put file in s3")
logger.info("Calling get attachment module")
get_attachment.get_required_attachment()
logger.info("get attachment module successfully called")
logger.info("calling csv manipulation")
manipulate_csv.manipulate_csv()
logger.info("csv manipulation done")
logger.info("now creating boto3 resources")

try:

    s3 = boto3.resource('s3',aws_access_key_id=config.AWS_ACCESS_KEY_LAKE,
                             aws_secret_access_key=config.AWS_SECRET_LAKE)

    logger.info("Opening data connections")
    data = open(os.path.join(current_path,get_attachment.FINAL_CSV), 'rb')
    logger.info("Data file stream opened")

# response = s3.Bucket('aws-junipergtmprod-data-stage').delete_objects(
#     Delete={
#         'Objects': [
#             {
#                 'Key': 'professional_services/abcd'
#             },
#             {
#                 'Key': 'professional_services/download.jpeg'
#             }
#         ]
#     })
# print response

    logger.info("Putting file in S3 bucket")
    s3.Bucket('aws-junipergtmprod-data-stage').put_object(Key='professional_services/{}/dt5={}/{}'.format(get_attachment.SUBKEY,today_date,get_attachment.FINAL_CSV),
                                                          Body=data,
                                                          ServerSideEncryption='AES256')
    logger.info("File put in S3 bucket. All done - Pending S3 to hive transfer.")
    send_email.send_success_email(get_attachment.SUBJECT)

except Exception as e:
    logger.error("EXCEPTION OCCURED: {}".format(e))
    logger.error(traceback.format_exc())
    send_email.send_error_email(get_attachment.SUBJECT)
# s3_client = boto3.client('s3',aws_access_key_id=config.AWS_ACCESS_KEY_LAKE,
#                          aws_secret_access_key=config.AWS_SECRET_LAKE)

# s3_client.upload_file("Project_Downtime_Report__{}_cleaned.csv".format(manipulate_csv.today_date), 'aws-junipergtmprod-data-stage',
#                       'professional_services/project_downtime/dt2={}/Project_Downtime_Report__{}.csv'.format(manipulate_csv.today_date,manipulate_csv.today_date), ExtraArgs={'ServerSideEncryption':'AES256'})
#
# s3_client.put_object(Bucket='aws-junipergtmprod-data-stage',
#                      Key='professional_services/project_downtime/dt4={}/Project_Downtime_Report__{}_cleaned.csv'.format(manipulate_csv.today_date,manipulate_csv.today_date),
#                      Body=open(os.path.dirname(os.path.realpath(__file__))+'/Project_Downtime_Report__{}_cleaned.csv'.format(manipulate_csv.today_date),'r'),
#                      ServerSideEncryption='AES256')




