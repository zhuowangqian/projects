import hashlib
import os
import re
import threading
import time
import pandas as pd
import requests
from lxml import etree
from selenium.webdriver.common.by import By

# 八爪鱼环境 用下面这个
from py_executor.base import BaseExecutor


def p_install(package):
    os.system(f'pip3 install {package}')


try:
    import pymongo
except:
    p_install('pymongo')
    time.sleep(5)
    import pymongo

try:
    from selenium import webdriver as uc
except:
    p_install('undetected_chromedriver2')
    time.sleep(5)
    from selenium import webdriver as uc


class AtomExecutor(BaseExecutor):
    name = 'beijingshicaizhengju'

    def init(self):
        pass

    def save_to_db(self, data, col):
        if data != 'exists':
            # 写入数据库
            x = col.insert_one(data)
            print(x)

    def get_content(self, contents, urlPre):
        content = []
        # 逐行判断
        for line in contents:
            if isinstance(line, str):  # 判断line是否与str为同一类型数据
                content.append(line)
            # 判断当前行是否包含图片
            elif line.xpath('.//img') != []:
                img = ''.join(line.xpath('.//img/@src'))
                if 'http' not in img:
                    key = re.search('(?<=W\d)(.\d\d\d\d\d)', img).group() if re.search('(?<=W\d)(.\d\d\d\d\d)',
                                                                                       img) != None else ''
                    img = img.replace('./', f'{urlPre}/{key}/')
                content.append(f"<img>{img}</img>")
            # 判断当前行是否为表格
            elif line.tag == 'table':
                content.append(self.get_table_text(line))
            # 判断当前行是否包含超链接
            elif line.xpath('.//a') != []:
                if line.tag == "li":
                    elementsContent = []
                    elements = line.xpath('./*')
                    # 处理li下所有文本
                    for el in elements:
                        if el.tag == 'a':
                            elementsContent.append(f"<a>{''.join(el.xpath('.//text()'))}</a>")
                        else:
                            elementsContent.append(''.join(el.xpath('.//text()')))
                    elementsContent = '\n'.join(elementsContent)
                    content.append(f"<li>{elementsContent}</li>")
                else:
                    content.append(f"<a>{''.join(line.xpath('.//a//text()'))}</a>")
            # 判断当前行是否包含strong标签
            elif line.xpath('.//strong') != []:
                values = []
                # 如果有strong，循环行里的所有元素
                for value in line.xpath('./strong|./text()'):
                    if isinstance(value, str):
                        values.append(value)
                    else:
                        values.append(f"<special>{''.join(value.xpath('.//text()'))}</special>")
                content.append(''.join(values).strip())
            elif line.tag == 'strong':
                content.append(''.join(f"<special>{''.join(line.xpath('.//text()'))}</special>"))
            # 文本行处理
            else:
                if line.tag == "li" and ''.join(line.xpath('.//text()')) != '':
                    content.append(f"<li>{''.join(line.xpath('.//text()')).strip()}</li>")
                else:
                    content.append(''.join(line.xpath('.//text()')).strip())
        content = '\n'.join(content)
        return content

    def get_table_text(self, table):
        content = []
        tbody = table.xpath('.//tbody')[0]
        trs = tbody.xpath('./tr')
        # 循环每行
        for tr in trs:
            tds = tr.xpath('./td')
            texts = []
            # 循环每行的每列
            for td in tds:
                text = ''.join(td.xpath('.//text()'))
                texts.append(f"<td>{text}</td>")
            texts = ''.join(texts)
            content.append(f"<tr>{texts}</tr>")
        content = '\n'.join(content)
        content = f'<table>{content}</table>'
        return content
        # for elem in table.iter(tag=('table', 'thead', 'tbody', 'tr', 'td', 'th')):
        #     # 删除所有样式属性
        #     elem.attrib.clear()
        # table = etree.tostring(table, encoding='unicode')
        # return table

    def get_att_file(self, contents, articleUrl, urlPre1):
        # 获取附件链接、附件名和附件类型
        # 超链接原始文本
        oldTexts = []
        # 超链接
        Urls = []
        # 附件类型
        fileTypes = []
        # 附件文件名
        extenalFileNames = []
        # 附件连接
        extenalFileUrl = []
        # 遍历所有a标签
        for aTag in contents:
            text = ''.join(aTag.xpath('.//text()'))
            oldTexts.append(text)
            url = ''.join(aTag.xpath('.//@href'))
            # 判断超链接是否需要补全
            if 'http' not in url:
                urlPre = re.sub('[^/]+(?!.*/)', '', articleUrl)
                if '../../' in url:
                    urlPre1 = re.sub('[^/]+(?!.*/)', '', urlPre)
                    url = url.replace('../../', urlPre1)
                else:
                    url = url.replace('./', urlPre)
            Urls.append(url)
            fileType = re.search('[^.]+(?!.*.)', url).group() if re.search('[^.]+(?!.*.)', url) != None else ''
            if fileType not in fileTypes:
                fileTypes.append(fileType)
            if fileType != "html" and fileType != "htm":
                extenalFileNames.append(text)
                extenalFileUrl.append(url)
            else:
                extenalFileNames.append('None')
                extenalFileUrl.append('None')

        attFiles = {
            "oldTexts": oldTexts,
            "Urls": Urls,
            "fileTypes": fileTypes,
            "extenalFileNames": extenalFileNames,
            "extenalFileUrl": extenalFileUrl,
        }
        return attFiles

    def get_data_model(self):
        data = {
            "创建时间": None,
            "更新时间": None,
            "爬取日期": None,
            "爬取网站": "北京市财政局",
            "国家/地区": '中国',
            "省/州": None,
            "市": '北京',
            "郡": None,
            "文章类型": '财政要闻',
            "正文": None,
            "税种": None,
            "法规名称/通知名称/法规新闻标题": None,
            "页面链接(信息来源)": None,
            "发文号": None,
            "来源": None,
            "超链接原始文本": None,
            "超链接": None,
            "附件文件名": None,
            "附件链接": None,
            "附件文件": None,
            "发文日期": None,
            "文章编号": None,
            "a标签数量": None,
            "超链接数量": None,
        }
        return data

    def get_detail_data(self, singleObj, types, urlPre, domain, wd):
        # 获取数据模板
        data = self.get_data_model()
        # 爬取时间
        currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        # 文章标题
        articleTitle = ''.join(singleObj.xpath('./a/@title'))
        # print(articleTitle)
        # 文章链接
        articleUrl = ''.join(singleObj.xpath('./a/@href'))
        articleUrl = articleUrl.replace('./', '/')
        # print(articleUrl)
        articleUrl = f"{urlPre}{articleUrl}"
        # print(articleUrl)
        # 文章编号
        articleId = hashlib.md5(articleUrl.encode(encoding='utf-8')).hexdigest()
        # 正文源码
        contentSource = self.request_get(articleUrl).text
        contentHtmlElement = etree.HTML(contentSource)
        # 文章来源
        articleSource = ''.join(
            contentHtmlElement.xpath('//div[contains(@class,"othermessage")]//span[contains(text(),"来源")]/text()'))
        articleSource = articleSource.replace('来源：', '')
        # 发文时间
        publishDate = ''.join(
            contentHtmlElement.xpath('//div[contains(@class,"othermessage")]//span[contains(text(),"日期")]/text()'))
        publishDate = publishDate.replace('日期：', '')
        publishDate = f"{publishDate} 00:00:00"
        # 发文号
        issueNumber = ''.join(contentHtmlElement.xpath('//li[contains(text(),"发文字号")]//span//text()'))
        # 获取正文所有段落
        contents = contentHtmlElement.xpath(
            '//div[@id="mainText"]/div/div/p[.//text()]|//div[@id="mainText"]/div/div/p[.//img]|//ul[@class="fujian"]/li|//div[@class="relevantdoc div_zcjd"]//li|//ul[@class="doc-info clearfix"]/li|//span[@class="zcjd_span"]|//div[@id="mainText"]/div/div/*[.//table]//table|//div[@id="mainText"]/div/div/div/p|//div[@id="mainText"]/div/div/div/p|//div[@id="mainText"]/div/div/strong|//div[@id="mainText"]/div/div/text()')

        # 正文内容
        # 正文为视频
        if contentHtmlElement.xpath('//iframe[contains(@class,"video")]') != []:
            wd.get(articleUrl)
            iframe = wd.find_element(By.XPATH, '//iframe[contains(@class,"video")]')
            wd.switch_to.frame(iframe)
            video = wd.find_element(By.XPATH, '//video//source')
            video = video.get_attribute('src')
            content = f"<video>{video}</video>"
        # 正文不为视频
        else:
            content = self.get_content(contents, urlPre)

        # 获取所有a标签
        aTags = contentHtmlElement.xpath(
            ' //div[@id="mainText"]/div/div/p[.//text()]//a|//div[@id="mainText"]/div/div/p[.//img]//a|//ul[@class="fujian"]/li//a|//div[@class="relevantdoc div_zcjd"]//li//a|//ul[@class="doc-info clearfix"]/li//a|//span[@class="zcjd_span"]//a|//div[@id="mainText"]/div/div/div/p//a|//div[@id="mainText"]/div/div/div/p//a|//div[@id="mainText"]/div/div/strong//a')
        # 获取正文附件
        attFiles = self.get_att_file(contents=aTags, articleUrl=articleUrl, urlPre1=urlPre)
        # 计算a标签数量
        aCountNub = len(aTags)

        # 获取正文附件
        # attFiles = self.get_att_file(contents, articleUrl=articleUrl, urlPre1=urlPre)
        oldTexts = attFiles['oldTexts']
        Urls = attFiles['Urls']
        fileTypes = attFiles['fileTypes']
        extenalFileUrl = attFiles['extenalFileUrl']
        extenalFileNames = attFiles['extenalFileNames']
        # 判断是否为在线文档
        if re.search('[^.]+(?!.*.)', articleUrl).group() != 'html':
            publishDate = ''.join(singleObj.xpath('./span//text()')) + ' 00:00:00'
            oldTexts.append(articleTitle)
            Urls.append(articleUrl)
            fileTypes.append(re.search('[^.]+(?!.*.)', articleUrl).group())
        # 判断是否超过时间范围
        publishDatecheck = time.strptime(publishDate, "%Y-%m-%d %H:%M:%S")
        publishDatecheck = int(time.mktime(publishDatecheck))
        # 设置抓取时间
        lastTimeCheck = "2018-01-01 00:00:00"
        lastTimeCheck = time.strptime(lastTimeCheck, "%Y-%m-%d %H:%M:%S")
        lastTimeCheck = int(time.mktime(lastTimeCheck))
        # 超链接数量
        urlCountNub = len(Urls)
        # 如果当前数据日期超出抓取范围，返回 0
        if publishDatecheck < lastTimeCheck:
            return 0
        fileTypes = ''
        if oldTexts:
            oldTexts = repr(oldTexts)
        else:
            oldTexts = None
        if Urls:
            Urls = repr(Urls)
        else:
            Urls = None
        if extenalFileNames:
            extenalFileNames = repr(extenalFileNames)
        else:
            extenalFileNames = None
        if extenalFileUrl:
            extenalFileUrl = repr(extenalFileUrl)
        else:
            extenalFileUrl = None
        # 截取文章标题最后四个字，判断文章类型
        key = articleTitle[-4:]
        for type in types:
            if type in key:
                data['文章类型'] = type
                break
        else:
            data['文章类型'] = domain
        data['发文号'] = issueNumber
        data['法规名称/通知名称/法规新闻标题'] = articleTitle
        data['页面链接(信息来源)'] = articleUrl
        data['正文'] = content
        data['发文日期'] = publishDate
        data['创建时间'] = currentTime
        data['更新时间'] = currentTime
        data['爬取日期'] = currentTime
        data['来源'] = articleSource
        data['超链接原始文本'] = oldTexts
        data['超链接'] = Urls
        data['附件文件名'] = extenalFileNames
        data['附件链接'] = extenalFileUrl
        data['附件文件'] = fileTypes
        data['文章编号'] = articleId
        data['a标签数量'] = aCountNub
        data['超链接数量'] = urlCountNub
        self.upload(data)
        return data

    def request_get(self, url):
        count = 0
        payload = {}
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'Secure HttpOnly; __jsluid_h=b97134eacfa1d51797fcf939ea404f0f; _va_ses=*; Hm_lvt_2953b5c39b9118db3e5df822218e5440=1689045156; Hm_lpvt_2953b5c39b9118db3e5df822218e5440=1689045328; _va_id=8ee3801a1c110cbd.1689045156.1.1689045334.1689045156.; Secure HttpOnly',
            'Pragma': 'no-cache',
            'Referer': 'http://czj.beijing.gov.cn/zwxx/czyw/index.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'
        }
        while True:
            try:
                response = requests.request("GET", url, headers=headers, data=payload, timeout=5)
                return response
            except:
                count += 1
            finally:
                if count > 10:
                    return "请求失败"

    def get_db_conect(self, colName):
        # 连云数据库
        # myclient = pymongo.MongoClient("mongodb://debaite:debaite001@1.116.224.26:27017/?authSource=debaite")
        # mydb = myclient["debaite"]
        # 连本地数据库
        myclient = pymongo.MongoClient("mongodb://localhost:27017")
        mydb = myclient["mymongo"]
        mycol = mydb[colName]
        return mycol

    def save_to_excel(self, filePath, addData):
        if os.path.exists(filePath):
            with pd.ExcelWriter(filePath, mode='a', engine="openpyxl") as writer:
                pd.DataFrame(addData).to_excel(writer, index=None)
        else:
            with pd.ExcelWriter(filePath) as writer:
                pd.DataFrame(addData).to_excel(writer, index=None)

    def crawl_thread(self, page, urlPre, domain, mycol, types, wd):
        while True:
            if page == 0:
                url = f"{urlPre}/index.html"
            else:
                url = f"{urlPre}/index_{page}.html"
            # 列表页源码
            listSource = self.request_get(url).text
            listHtmlElement = etree.HTML(listSource)
            list = listHtmlElement.xpath('//div[@class="ul-back"]/ul/li')
            # print(list)
            # 判断当前页是否有内容
            if list == []:
                break
            print(f'正在爬取{domain}第{page + 1}页...')
            for single in list:
                # print(single)
                data = self.get_detail_data(single, types, urlPre, domain, wd)
                # print(data)
                # data ==0 表示当前数据超出抓取范围，停止抓取
                if data == 0:
                    return 0
                x = mycol.insert_one(data)
                # 将要写入excel的数据存入容器addData
                for add in addData.keys():
                    addData[add].append(data[add])
                # print(x)
            page += 1

    def process_item(self, keyword):
        try:
            global addData
            addData = {
                "创建时间": [],
                "更新时间": [],
                "爬取日期": [],
                "爬取网站": [],
                "国家/地区": [],
                "省/州": [],
                "市": [],
                "郡": [],
                "文章类型": [],
                "正文": [],
                "税种": [],
                "法规名称/通知名称/法规新闻标题": [],
                "页面链接(信息来源)": [],
                "发文号": [],
                "来源": [],
                "超链接原始文本": [],
                "超链接": [],
                "附件文件名": [],
                "附件链接": [],
                "附件文件": [],
                "发文日期": [],
                "文章编号": [],
                'a标签数量': [],
                '超链接数量': [],
            }
            wd = uc.Chrome()
            # 链接数据库
            mycol = self.get_db_conect('beijing_test3')
            # 用于匹配文章类型
            types = ['公告', '通知', '政策指引', '问答', '政策解读', '操作指南', '法律', '规定', '办法', '规则', '制度',
                     '决定', '规程', '目录']
            domains = {
                "政策文件": "http://czj.beijing.gov.cn/zwxx/zcfg",
                "财政要闻": "http://czj.beijing.gov.cn/zwxx/czyw",
                "财政数据": "http://czj.beijing.gov.cn/zwxx/czsj",
                "政策解读": "http://czj.beijing.gov.cn/zwxx/zcjd",
            }
            # 多线程
            thread_list = []
            for domain in domains:
                urlPre = domains[domain]
                page = 0
                t = threading.Thread(target=self.crawl_thread,
                                     args=(page, urlPre, domain, mycol, types, wd))
                t.start()
                thread_list.append(t)
            for t in thread_list:
                t.join()
            print(addData)
            self.save_to_excel(filePath='北京市财政局.xlsx', addData=addData)
        except Exception as e:
            print(e, '123')
            self.logger.info(e)


if __name__ == '__main__':
    # 八爪鱼环境 用下面这个
    from py_executor.cli import invoke_for_debug

    params = {
        "MainKeys": [
            '1'
        ],

    }
    invoke_for_debug(__file__, params)
