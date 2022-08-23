import random
from time import time, localtime
import requests
from datetime import datetime

#########################################################################################################
# 微信消息模版
'''
{{date.DATA}}
 今天是我们认识的第{{time.DATA}}天
 城市：{{city.DATA}}
 天气：{{weather.DATA}}
 最低气温: {{min_wd.DATA}}℃
 最高气温: {{max_wd.DATA}}℃
 今日建议: {{tips.DATA}}

 随机一言: {{yy.DATA}}

 林夕提醒您:亲,疫情期间出门请戴好口罩哟!
 疫情通告更新: {{yiqing.DATA}}
'''
# 接收的用户
users = ["o0B9F6AwpYHae4zFetfE2FFeEipw"]
# 模板ID
template_list=['9DLD8-sjMDpvmvymE8KdPiFTrsFK_Z3jOzIrp6jKgyc','模板2','模板3']
# 城市id查询(https://img.weather.com.cn/newwebgis/fc/nation_fc24h_wea_2022010420.json)
city_id=['101221201','地区id2','地区id3']
# 测试号配置信息
app_id = "wx5f78b65377bb1105"
app_secret = "fea851ba0056557a99c5fe640201d221"
##########################################################################################################

# 获取token
def get_access_token():
    post_url = (
        f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}")
    access_token = requests.get(post_url).json()['access_token']
    print('[INFO]获取token成功!')
    return access_token

# 获取随机颜色
def get_color():
    get_colors = lambda n: list(map(lambda i: "#" + "%06x" % random.randint(0, 0xFFFFFF), range(n)))
    color_list = get_colors(100)
    return random.choice(color_list)


# 随机一言
def yiyan():
    url = 'http://api.botwl.cn/api/yiyan?type='
    yy = requests.get(url).text
    print('[INFO]一言模块加载正常')
    return yy

# 疫情
def cqyq():
    url = 'https://opendata.baidu.com/data/inner?tn=reserved_all_res_tn&resource_id=28565&query=重庆新型肺炎最新动态'
    data = requests.get(url).json()['data'][0]['result']['items']
    data_print = '\n'
    for i in range(4):
        title = data[i]['eventDescription']
        # url = data[i]['eventUrl']
        data_print += title+"\n"
    print('[INFO]疫情模块加载正常')
    return data_print

# 获取温度
def get_weather(city_id):
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    #print(t)
    headers = {
        "Referer": "http://www.weather.com.cn/",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = f"http://d1.weather.com.cn/weather_index/{city_id}.html?_={t}"
    response = requests.get(url, headers=headers)
    response.encoding = "utf-8"
    # print(response.text)
    response_data_0 = eval(response.text.split(";")[0].split("=")[-1])
    response_data_2 = eval(response.text.split(";")[2].split("=")[-1])
    response_data_3 = eval(response.text.split(";")[3].split("=")[-1])
    weatherinfo_0 = response_data_0["weatherinfo"]
    # 城市名称
    city_name = weatherinfo_0['city']
    # 最高气温
    max_wd = weatherinfo_0["temp"]
    # 最低气温
    min_wd = weatherinfo_0["tempn"]
    # 天气
    weather = weatherinfo_0["weather"]
    # 相对湿度
    shidu = response_data_2['SD']
    # 生活指数
    zs=response_data_3['zs']
    tips = '\n晨练'+zs['cl_hint']+':'+zs['cl_des_s']+'\n穿衣小贴士:'+zs['ct_des_s']
    print('[INFO]天气模块加载正常')
    return city_name, weather, max_wd, min_wd,shidu, tips



# 推送信息
def send_message(template_id,to_user, access_token, city_name , weather, max_wd, min_wd,shidu, tips, yy,cqyq):
    url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}".format(access_token)
    week_list = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"]
    today = datetime.date(datetime(year=localtime().tm_year, month=localtime().tm_mon, day=localtime().tm_mday))
    week = week_list[today.isoweekday() % 7]
    data = {
        "touser": to_user,
        "template_id": template_id,  # 模板id
        "url": "http://linxi.tk",
        "topcolor": "#FF0000",
        "data": {
            "date": {
                "value": "{} {}".format(today, week),
                "color": get_color()
            },
            "time": {
                "value": (datetime.today() - datetime(2017,9,1)).days,
                "color": get_color()
            },
            "city": {
                "value": city_name,
                "color": get_color()
            },
            "weather": {
                "value": weather,
                "color": get_color()
            },
            "min_wd": {
                "value": min_wd,
                "color": get_color()
            },
            "max_wd": {
                "value": max_wd,
                "color": get_color()
            },
            "tips": {
                "value": tips,
                "color": get_color()
            },
            "shidu": {
                "value": shidu,
                "color": get_color()
            },
            "yy": {
                "value": yy,
                "color": get_color()
            },
            "yiqing": {
                "value": cqyq,
                "color": get_color()
            },
            "wh": {
                "value": "希望收到消息的你永远开心！",
                "color": get_color()
            },
        }
    }
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    response = requests.post(url, headers=headers, json=data).json()
    if response["errcode"] == 40037:
        print("[INFO]推送消息失败，请检查模板id是否正确")
    elif response["errcode"] == 40036:
        print("[INFO]推送消息失败，请检查模板id是否为空")
    elif response["errcode"] == 40003:
        print("[INFO]推送消息失败，请检查微信号是否正确")
    elif response["errcode"] == 0:
        print("[INFO]推送消息成功")
    else:
        print(response)


if __name__ == "__main__":
    # 获取accessToken
    accessToken = get_access_token()
    # 一言信息
    yy = yiyan()
    # 疫情信息
    cqyq=cqyq()
    # 公众号推送消息
    for user in users:
        # 传入省份和市获取天气信息
        city_name, weather, max_wd, min_wd,shidu,tips = get_weather(city_id[users.index(user)])
        send_message(template_list[users.index(user)],user, accessToken, city_name, weather, max_wd, min_wd,shidu,tips, yy,cqyq)
