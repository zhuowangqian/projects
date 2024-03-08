# -*-coding:utf-8-*-
# import time
import json
import re
import time
from crawles import execjs
import requests
# import datetime
# import cchardet
import csv
import pandas as pd
import pymysql
import os
from sqlalchemy import create_engine, text


class Baidu_translate():

    def __init__(self):
        pass

    def save_to_sql(self, data):
        db = pymysql.connect(
            user='root',
            password='Qian1314',
            database='test'
        )
        cursor = db.cursor()
        sql = 'insert into baidu_translate2(' \
              'a,b,c,d,e,f' \
              ') values (' \
              '%s,%s,%s,%s,%s,%s' \
              ');'
        # translate_result, sentence_instances, similar_words, simple_means, synthesize_means, zdict
        for i, values in enumerate(data['translate_result']):
            try:
                cursor.execute(sql, (
                    data['translate_result'][i], data['sentence_instances'][i], data['similar_words'][i],
                    data['zdict'][i],
                    data['simple_means'][i], data['synthesize_means'][i]))
                db.commit()
            except:
                continue


    # def save_to_sql(self,):
    #     sql = "insert into baidu_translate2(" \
    #           "a,b,c,d,e,f,g" \
    #           ")values(" \
    #           "%s,%s,%s,%s,%s,%s,%s" \
    #           ");"
    # cursor.execute(sql, (
    #     str(query), str(translate_result), str(sentence_instances), str(similar_words), str(zdict),
    #     str(simple_means),
    #     str(synthesize_means)))
    # db.commit()

    def request_get(self, translate_obj):
        url = 'https://fanyi.baidu.com/v2transapi'
        # cookies 会在一段时间后失效  待进一步逆向或者通过selenium获取
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
        js = execjs('js.js')
        sign = js.call('b', query)
        mytime = time.time()
        data = {
            'from': from_language,
            'to': to_language,
            'query': query,
            'transtype': 'realtime',
            'simple_means_flag': '3',
            'sign': sign,
            'token': '08ddb42ed65700b725cb72372fd71c5b',
            'domain': 'common',
            'ts': mytime,
        }
        request = requests.post(url, headers=headers, data=data, cookies=cookies, timeout=60)
        response = request.text
        print(response)
        try:
            json_data = json.loads(response)
        except:
            json_data = {}
        return json_data

    def dict_model(self):
        data = {
            'translate_result': None,
            'sentence_instances': None,
            'similar_words': None,
            'simple_means': None,
            'synthesize_means': None,
            'zdict': None
        }
        return data

    def data_process(self, json_data):
        data_model = self.dict_model()
        # 翻译结果
        try:
            translate_result = json_data['trans_result']['data'][0]['dst']
        except:
            translate_result = "None"
        # 例句
        try:
            sentence_instances0 = json_data['liju_result']['double']
            data1 = sentence_instances0
            str1 = re.sub('^\[\[\[', '', data1)
            str2 = re.sub(']$', '', str1)
            list = re.findall('\[.*?\]', str2)
            # print(list)
            if list != []:
                # 文本乱码，需要将所有文本单独取出，重新进行编解码
                sentences = []
                for index, i in enumerate(list):
                    text0 = re.findall('\["(.*?)",', i)
                    text = text0[0].replace('\/', '')
                    if text:
                        try:
                            text = text.encode('utf-8').decode('unicode-escape')
                            sentences.append(text)
                        except:
                            pass
                    else:
                        text = "None"
                        sentences.append(text)
                sentences_1 = ' '.join(sentences)
                sentences = sentences_1.split('.')
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
                    try:
                        text = i[0]
                        data = text
                        dict1 = {str(index): data}
                        sentence_instances.update(dict1)
                    except:
                        dict1 = {str(index): "None"}
                        sentence_instances.update(dict1)
            else:
                sentence_instances = 'None'
        except:
            sentence_instances = 'None'


        # 其他数据
        try:
            similar_words = json_data['dict_result']['general_knowledge']['similar_words']
            # print(similar_words)
        except:
            similar_words = None
        try:
            simple_means = json_data['dict_result']['simple_means']
            # print(simple_means)
        except:
            simple_means = None
        try:
            synthesize_means = json_data['dict_result']['synthesize_means']
            # print(synthesize_means)
        except:
            synthesize_means = None
        try:
            zdict = json_data['dict_result']['zdict']
            # print(zdict)
        except:
            zdict = None
        # 数据封装   要注意变量名称，尽量不要重复

        data_model['translate_result'] = translate_result
        data_model['sentence_instances'] = str(sentence_instances)
        data_model['similar_words'] = similar_words
        data_model['simple_means'] = simple_means
        data_model['synthesize_means'] = synthesize_means
        data_model['zdict'] = zdict
        data = data_model
        return data

    def save_text(self, filename, data):
        # 储存例句
        try:
            f = open(filename, 'w+', encoding='utf-8')
            for i, values in enumerate(data['sentence_instances']):
                for x, y in values.items():
                    data1 = x + ' ' + y + '\n'
                    f.writelines(data1)

        except:
            f = open(filename, 'w+', encoding='utf-8')
            data1 = "None"
            f.writelines(data1)
        f.close()

    def save_to_csv(self, filename, data):
        with open(filename, 'w', encoding='utf-8') as file:
            csv_writer = csv.writer(file)
            csv_writer.writerow(['翻译结果', '例句', '关联词汇', '字典解释', '简单释义', '综合释义'])
            for i, values in enumerate(data['translate_result']):
                csv_writer.writerow([data['translate_result'][i],
                                     data['sentence_instances'][i], data['similar_words'][i], data['zdict'][i],
                                     data['simple_means'][i],
                                     data['synthesize_means'][i]]
                                    )

    def save_to_excel(self, filePath, addData):
        if os.path.exists(filePath):
            # with pd.ExcelWriter(filePath, mode='a', engine="xlsxwriter", options={'strings_to_urls': False}) as writer:
            with pd.ExcelWriter(filePath, mode='a', engine="openpyxl") as writer:
                pd.DataFrame(addData).to_excel(writer, index=None, sheet_name='sheet2')
        else:
            with pd.ExcelWriter(filePath) as writer:
                pd.DataFrame(addData).to_excel(writer, index=None, sheet_name='sheet2')

    # def crawl_thread():
    #     # 多线程
    #     thread_list = []
    #     for domain in domains:
    #         urlPre = domains[domain].replace(' ', '')
    #         # print(urlPre)
    #         page = 0
    #         t = threading.Thread(target=self.crawl_thread,
    #                              args=(page, urlPre, domain, mycol, types))
    #         t.start()
    #         thread_list.append(t)
    #     for t in thread_list:
    #         t.join()
    def read_sql(self):
        MYSQL_HOST = 'localhost'
        MYSQL_PORT = '3306'
        MYSQL_USER = 'root'
        MYSQL_PASSWORD = 'Qian1314'
        MYSQL_DB = 'test'
        engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'
                               % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))
        conn = engine.connect()
        sql = text('SELECT * FROM 品类分析1')
        df2 = pd.read_sql(sql, conn)
        # pd.set_option('display.unicode.ambiguous_as_wide', True)
        # pd.set_option('display.unicode.east_asian_width', True)
        df2 = df2.to_dict()
        return df2

    def process_items_excel(self):
        try:
            # data1 = pd.read_excel(io=r'C:\Users\Administrator\Desktop\\aliexpress\品类分析.xlsx', sheet_name="选品（大类）")
            data1 = pd.read_excel(io=r'C:\Users\Administrator\Desktop\\aliexpress\品类分析.xlsx', sheet_name="物流")

            dict = data1.to_dict()
            addData = {
                'translate_result': [],
                'sentence_instances': [],
                'similar_words': [],
                'simple_means': [],
                'synthesize_means': [],
                'zdict': [],
            }
            for index, translate_obj in dict["logist_company"].items():
                print(translate_obj)
                if translate_obj:
                    json_data = self.request_get(translate_obj)
                    data = self.data_process(json_data)
                    print(data)
                    for keys, values in data.items():
                        addData[keys].append(values)
                    # print(addData)
                else:
                    break

            self.save_text('tras_result.text', data1)
            self.save_to_csv('tras_result.csv', data=addData)
            self.save_to_excel('tras_result.xlsx', addData=addData)
            self.save_to_sql(data=addData)

        except Exception as e:
            print(e, 'error')

    def process_items_sql(self):
        try:
            dict = self.read_sql()
            # data = pd.read_excel(io=r'C:\Users\Administrator\Desktop\\aliexpress\品类分析.xlsx', sheet_name="选品（大类）")
            addData = {
                'translate_result': [],
                'sentence_instances': [],
                'similar_words': [],
                'simple_means': [],
                'synthesize_means': [],
                'zdict': [],
            }
            for index, translate_obj in dict["category_leaf_name"].items():
                print(translate_obj)
                if translate_obj:
                    json_data = self.request_get(translate_obj)
                    time.sleep(5)
                    data = self.data_process(json_data)
                    print(data)
                    for keys, values in data.items():
                        addData[keys].append(values)
                else:
                    break

            self.save_text('tras_result2.text', dict)
            self.save_to_csv('tras_result2.csv', data=addData)
            self.save_to_excel('tras_result2.xlsx', addData=addData)
            self.save_to_sql(data=addData)

        except Exception as e:
            print(e, 'error')


if __name__ == '__main__':
    code = Baidu_translate()
    code.process_items_excel()
    # code.process_items_sql()
