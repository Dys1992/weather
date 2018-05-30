import datetime
import json

import requests
import schedule


def get_today_weather():
    nowTime = datetime.datetime.now().strftime('%m-%d')

    url = 'http://tj.nineton.cn/Heart/index/all?city=CHJS030000'

    req = requests.get(url)

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

    print(remind_me)


get_today_weather()

schedule.every().day.at("17:59").do(get_today_weather)
schedule.run_pending()
