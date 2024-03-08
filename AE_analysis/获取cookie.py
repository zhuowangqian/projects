# coding = utf-8
import crawles

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

data = {
    'from': 'zh',
    'to': 'en',
    'query': '苹果',
    'transtype': 'realtime',
    'simple_means_flag': '3',
    'sign': '927377.705952',
    'token': '08ddb42ed65700b725cb72372fd71c5b',
    'domain': 'common',
    'ts': '1695988757955',
}

response = crawles.post(url, headers=headers, data=data, cookies=cookies)
print(response.text)
