import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import requests

from logger.logging_config import logger
# Logging =  Logging().logger(level='INFO')
def is_connected():
    try:
        response = requests.get("https://www.baidu.com", timeout=5)
        return True
    except requests.ConnectionError:
        print("No internet connection.")
        return False
def email_server(emailContext,mail_host,mail_user,mail_pass,receivers):
    if not is_connected():
        logger.error("network hava problem")
        return
    # 第三方 SMTP 服务
    mail_host = mail_host  # 设置服务器
    mail_user = mail_user  # 用户名
    mail_pass = mail_pass  # 口令
    sender = mail_user
    receivers = receivers  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    message = MIMEText(emailContext, 'plain', 'utf-8')
    message['From'] = Header("RL", 'utf-8')
    message['To'] = Header("RLer", 'utf-8')
    subject = 'RL-Email'
    message['Subject'] = Header(subject, 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        logger.info("email successfully")
    except smtplib.SMTPException:
        logger.error("Error: email send fail")


def mkdir_filepath(dir,file_name):
    root_path = os.getcwd()
    log_folder_path = os.path.join(root_path, dir)
    if not os.path.exists(log_folder_path):
        os.makedirs(log_folder_path)
    file_path = os.path.join(log_folder_path, file_name)
    return file_path