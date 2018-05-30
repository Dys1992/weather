import datetime
import json
import smtplib
from email.mime.text import MIMEText

import itchat
import requests
import schedule


class weather:
    def __init__(self, city_code):
        self.city_code = city_code

    def get_today_weather(self):
        nowTime = datetime.datetime.now().strftime('%m-%d')

        url = 'http://tj.nineton.cn/Heart/index/all?city='

        req = requests.get(url + self.city_code)

        weather_json = json.loads(req.text)
        # 城市名
        city_name = weather_json["weather"][0]["city_name"]
        # 天气
        text = weather_json["weather"][0]["now"]["text"]
        # 温度
        temperature = weather_json["weather"][0]["now"]["temperature"]
        # 风速
        wind_scale = weather_json["weather"][0]["now"]["wind_scale"]
        # PM25
        pm25 = weather_json["weather"][0]["now"]["air_quality"]["city"]["pm25"]
        # 空气质量
        quality = weather_json["weather"][0]["now"]["air_quality"]["city"]["quality"]
        # 建议
        details = weather_json["weather"][0]["today"]["suggestion"]["dressing"]["details"]

        remind_me = nowTime + city_name + " ->" + "  天气：" + text + "   温度：" + temperature + "   风速：" + \
                    wind_scale + "  PM25：" + pm25 + "  空气质量：" + quality + "  \n 建议：" + details

        se = SendEmail("352871913@qq.com", remind_me)
        se.send_email()


class SendEmail:
    def __init__(self, to_name, msg):
        self.to_name = to_name
        self.msg = msg

    def send_email(self):
        info = MIMEText(self.msg, 'plain', 'utf-8')

        from_addr = '1106058371@qq.com'
        password = 'nyabnknghkicggde'

        to_user = self.to_name  # 收件人邮箱地址
        smtp_server = 'smtp.qq.com'  # SMTP邮件服务器地址
        subject = "今日天气"

        msg = MIMEText(self.msg)
        msg['Subject'] = subject
        msg['From'] = from_addr
        msg['To'] = to_user

        s = smtplib.SMTP_SSL(smtp_server, 465)  # 定义一个s对象
        s.login(from_addr, password)  # auth发件人信息
        s.sendmail(from_addr, to_user, msg.as_string())
        s.quit()


# noinspection PyBroadException
def tu_ling(msg):
    url = 'http://www.tuling123.com/openapi/api'
    data = {
        'key': '56e63989b4e842e2aa1277c4bf74dff6',
        'info': msg['Text'],
        'userid': 'wechat-robot',
    }
    try:
        r = requests.post(url, data=data).json()
        return r.get('text')
    except:
        return


@itchat.msg_register('Text')
def text_reply(msg):
    # if not msg['FromUserName'] == myUserName:
    # itchat.send_msg(u"[%s]收到好友@%s 的信息：%s\n" %
    #                 (time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg['CreateTime'])),
    #                  msg['User']['NickName'],
    #                  msg['Text']), 'filehelper')
    reply = tu_ling(msg)
    # return u'[自动回复]您好，我现在有事不在，一会再和您联系。\n已经收到您的的信息：%s\n' % msg['Text']
    return '[自动回复]' + reply


def send_weather():
    p = weather('CHJS030000')
    itchat.send_msg(p.get_today_weather(), myUserName)


if __name__ == '__main__':
    itchat.auto_login()
    myUserName = itchat.get_friends(update=True)[0]["UserName"]
    itchat.run()
    schedule.every().day.at("17:49").do(send_weather)
