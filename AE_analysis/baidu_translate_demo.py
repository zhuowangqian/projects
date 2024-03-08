# -*-coding:utf-8-*-
import time
import json
import crawles
import re
import time
from crawles import execjs
import requests
import datetime
import cchardet
import csv
import pandas as pd
import pymysql

db = pymysql.connect(
    user='root',
    password='Qian1314',
    database='test'
)
cursor = db.cursor()

# sql1 = 'describe baidu_translate2'
# sql2 = 'Alter table baidu_translate2 modify column a varchar(255) ;'
# cursor.execute(sql2)
# result = cursor.fetchall()
# print(result)
# import execjs
# f = open('js.js', 'r', encoding='utf-8')
# text = f.read()
# f.close()
# js = execjs.compile(text)

# res = js.call('b','苹果')
# print(res)
import pandas as pd
data = pd.read_excel(io=r'C:\Users\Administrator\Desktop\\aliexpress\品类分析.xlsx', sheet_name="选品（大类）")
dict = data.to_dict()
translate_obj = []
for x, y in dict["category_leaf_name"].items():
    translate_obj.append(y)

url = 'https://fanyi.baidu.com/v2transapi'

cookies = {
    'BDUSS': 'pjaUJ3V04teWs3bUhRdlcxS3JRall3U3dQRHd3YzZ0eE50Z2tsVll5bFFsZGhrSVFBQUFBJCQAAAAAAAAAAAEAAADaIUeHemh1b3dhbmdxaWFuNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAIsWRQCLFkNE',
    'BDUSS_BFESS': 'pjaUJ3V04teWs3bUhRdlcxS3JRall3U3dQRHd3YzZ0eE50Z2tsVll5bFFsZGhrSVFBQUFBJCQAAAAAAAAAAAEAAADaIUeHemh1b3dhbmdxaWFuNwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFAIsWRQCLFkNE',
    'BIDUPSID': 'FC4D6FFFA4453EEF7532394F3FBBBE85',
    'PSTM': '1693550709',
    'ZFY': 'ob5zFAHsO9lcNLi:AyFHMUcjSgIFvGPHgBbFVQL5x92g:C',
    'BAIDUID': 'FC4D6FFFA4453EEF7532394F3FBBBE85:SL=0:NR=10:FG=1',
    'BAIDUID_BFESS': 'FC4D6FFFA4453EEF7532394F3FBBBE85:SL=0:NR=10:FG=1',
    'BAIDU_WISE_UID': 'wapp_1694429846569_286',
    'APPGUIDE_10_6_2': '1',
    'REALTIME_TRANS_SWITCH': '1',
    'FANYI_WORD_SWITCH': '1',
    'HISTORY_SWITCH': '1',
    'SOUND_SPD_SWITCH': '1',
    'SOUND_PREFER_SWITCH': '1',
    'RT': '\"z=1&dm=baidu.com&si=092b21c5-89d2-4903-bd55-cb6dfa42c97b&ss=lmydxfh3&sl=3&tt=28i&bcn=https%3A%2F%2Ffclog.baidu.com%2Flog%2Fweirwood%3Ftype%3Dperf&ld=ns6&ul=qmt&hd=qnx\"',
    'APPGUIDE_10_6_5': '1',
    'Hm_lvt_64ecd82404c51e03dc91cb9e8c025574': '1694751487,1695043849,1695988742',
    'Hm_lpvt_64ecd82404c51e03dc91cb9e8c025574': '1695988746',
    'ab_sr': '1.0.1_ZWVlNjVjMmM5MWJjYjZlOWQzZDkxZDgxNzIwYTdkYTkyNmUzYmViY2ZlN2UwNDIzZjhkZGZlNjYwYmNhMDRmYWJmNzFlMGM3MWRhZGM0YzFlZDMwY2Y0YTliMTVlOTVmZGI3ZGQ3NGZhZGM4MTVkZDIxMmE3NDdhOWNmYTc0ZmY0NWEwZGZiNzc5MzU2MjU5YWMxMGVhOGI1MGJhMmQ1NjI1NjViNTk1ZTJhMzZjZWNlMjA2YTI5NDgyMjUxMDgx',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Acs-Token': '1695988583847_1695988758019_oYGtZoq5Vj0BZGOSLI6W52+/TOV1IwrEawXFMa7IAA+7GqgWL9h9zQE1jlk4xon1NvH1XFJAhSPJqsePzEQ/gbUbV06rr2V/ZJwQ1B9QtcEQmP1CMBDSqtJmo3LJQ+2+yvN/hcy+kkSH1S1L0rWz7JQgfDnIaurJq4OoeabDo5bd3biOBKu9OSwQn5rPZk9Ibusj9O3D3/r9AlhtgdMKREZN9zROVh/LGbdl/KMbTqRM4KgRozeaC2lkHBTlsnn3kD6y9qC7KaBhoNK08oLwRIQkEhW5lmjDCNmqSI8QlrzNdk6KKWS2XlJs16KMj5eAhPnLwdMjphppPU2BLqsXZHYEfLZ/X7qKKphi6uHLdR9Scilv5NqUthMwRPwhBKBBMCcEkmrUBySqTIqweSPzE0ZW6Aw41y/ng7PEklNieEhhAUUZM8DzRrc8rNKhf19Oj2OVwx8iSqfLAhEefnQD06NucRWYSsfmET64Hf7lDlpEm9R8i6j9/c4EEVxMQWT6RxNXLUkS3CtP/05uynO4lA==',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'DNT': '1',
    'Origin': 'https://fanyi.baidu.com',
    'Referer': 'https://fanyi.baidu.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '\"Windows\"',
}

#  langList: { 'zh': '中文','jp': '日语','jpka': '日语假名','th': '泰语','fra': '法语','en': '英语','spa': '西班牙语','kor': '韩语','tr': '土耳其语','vie': '越南语','ms': '马来语','de': '德语','ru': '俄语','ir': '伊朗语','ara': '阿拉伯语','est': '爱沙尼亚语','be': '白俄罗斯语','bul': '保加利亚语','hi': '印地语','is': '冰岛语','pl': '波兰语','fa': '波斯语','dan': '丹麦语','tl': '菲律宾语','fin': '芬兰语','nl': '荷兰语','ca': '加泰罗尼亚语','cs': '捷克语','hr': '克罗地亚语','lv': '拉脱维亚语','lt': '立陶宛语','rom': '罗马尼亚语','af': '南非语','no': '挪威语','pt_BR': '巴西语','pt': '葡萄牙语','swe': '瑞典语','sr': '塞尔维亚语','eo': '世界语','sk': '斯洛伐克语','slo': '斯洛文尼亚语','sw': '斯瓦希里语','uk': '乌克兰语','iw': '希伯来语','el': '希腊语','hu': '匈牙利语','hy': '亚美尼亚语','it': '意大利语','id': '印尼语','sq': '阿尔巴尼亚语','am': '阿姆哈拉语','as': '阿萨姆语','az': '阿塞拜疆语','eu': '巴斯克语','bn': '孟加拉语','bs': '波斯尼亚语','gl': '加利西亚语','ka': '格鲁吉亚语','gu': '古吉拉特语','ha': '豪萨语','ig': '伊博语','iu': '因纽特语','ga': '爱尔兰语','zu': '祖鲁语','kn': '卡纳达语','kk': '哈萨克语','ky': '吉尔吉斯语','lb': '卢森堡语','mk': '马其顿语','mt': '马耳他语','mi': '毛利语','mr': '马拉提语','ne': '尼泊尔语','or': '奥利亚语','pa': '旁遮普语','qu': '凯楚亚语','tn': '塞茨瓦纳语','si': '僧加罗语','ta': '泰米尔语','tt': '塔塔尔语','te': '泰卢固语','ur': '乌尔都语','uz': '乌兹别克语','cy': '威尔士语','yo': '约鲁巴语','yue': '粤语','wyw': '文言文','cht': '中文繁体'    },

from_language = 'en'
to_language = 'zh'
query = translate_obj
mytime = time.time()
js = execjs('js.js')
for i in query:
    sign = js.call('b', i)
    data = {
        'from': from_language,
        'to': to_language,
        'query': i,
        'transtype': 'realtime',
        'simple_means_flag': '3',
        'sign': sign,
        'token': '08ddb42ed65700b725cb72372fd71c5b',
        'domain': 'common',
        'ts': mytime,
    }
    response = requests.post(url, headers=headers, data=data, cookies=cookies).text
    json_data = json.loads(response)
    print(json_data)
    # print(json_data)
    # print(json_data)
    # 例句处理
    # print(response)
    sentence_instances = json_data['liju_result']['double']
    sentence_instances = f'sentences:{sentence_instances}'
    data = sentence_instances
    str1 = re.sub('^\[\[\[', '', data)
    str2 = re.sub(']$', '', str1)
    list = re.findall('\[.*?\]', str2)

    # 文本乱码，需要将所有文本单独取出，重新进行编解码
    sentences = []
    for index, i in enumerate(list):
        text = re.findall('\["(.*?)",', i)
        if text:
            text = text[0].encode('utf-8').decode('unicode-escape')
            sentences.append(text)
        else:
            text = []
            sentences.append(text)
    sentences = ' '.join(sentences)
    sentences = sentences.split('.')
    sentence1 = []
    for index1, i in enumerate(sentences):
        i = i.strip() + '.'
        data = i.split('?')
        data2 = []
        index0 = []
        for index2, e in enumerate(data):
            if '？' in e:
                e = e.strip() + '?'
                data2.append(e)
                index0.append(index2)
                data.pop(index2)
        sentence1.append(data)
        if data2 != []:
            sentence1.append(data2)

    sentence_instances = {}
    for index, i in enumerate(sentence1):
        if type(i) == list:
            text = i[0]
            data = text
            dict1 = {str(index): data}
            sentence_instances.update(dict1)
        else:
            data = 'None'
            dict1 = {str(index): data}
            sentence_instances.update(dict1)

    f = open('data.text', 'w+', encoding='utf-8')
    for x, y in sentence_instances.items():
        data = x + ' ' + y + '\n'
        f.writelines(data)
    f.close()
    translate_result = json_data['trans_result']['data'][0]['dst']
    print(translate_result)
    try:
        if json_data['dict_result']:
            dict_result = json_data['dict_result']
            simple_means = json_data['dict_result']['simple_means']
            similar_words = json_data['dict_result']['general_knowledge']['similar_words']
            zdict = json_data['dict_result']['zdict']
            synthesize_means = json_data['dict_result']['synthesize_means']
    except:
        dict_result = []
        similar_words = []
        simple_means = []
        synthesize_means = []
        zdict = []

    # print(translate_result, similar_words, simple_means, synthesize_means,
    #       zdict, sentence_instances, sep='\n')

    with open('data.csv', 'w+', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(['翻译结果', '例句', '关联词汇', '字典解释', '简单释义', '综合释义'])
        csv_writer.writerow([str(translate_result),
                             str(sentence_instances), str(similar_words), str(zdict), str(simple_means),
                             str(synthesize_means)])

    # sql = "insert into baidu_translate2(" \
    #       "a,b,c,d,e,f,g" \
    #       ")values(" \
    #       "%s,%s,%s,%s,%s,%s,%s" \
    #       ");"
    # cursor.execute(sql, (
    #     str(query), str(translate_result), str(sentence_instances), str(similar_words), str(zdict), str(simple_means),
    #     str(synthesize_means)))
    # db.commit()
