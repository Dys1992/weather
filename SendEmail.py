from email.mime.text import MIMEText
import smtplib


class SendEmail:
    def __init__(self, to_name, msg):
        self.to_name = to_name
        self.msg = msg

    def send_email(self):
        info = MIMEText(self.msg, 'plain', 'utf-8')

        from_addr = '1106058371@qq.com'
        password = 'Fanyu1992'
        # 收件人邮箱地址
        to_user = self.to_name
        # SMTP邮件服务器地址
        smtp_server = 'qq.smtp.com'

        s = smtplib.SMTP(smtp_server, 25)  # 定义一个s对象
        s.set_debuglevel(1)  # 打印debug日志
        s.login(from_addr, password)  # auth发件人信息
        s.sendmail(from_addr, to_user, info.as_string())
        s.quit()
