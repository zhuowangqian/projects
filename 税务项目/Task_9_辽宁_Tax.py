import hashlib
import os
import re
import threading
import time
import pandas as pd
import requests
from lxml import etree
import json
import cchardet
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

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

    def save_to_W0db(self, data, col):
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
                    img = f'http://liaoning.chinatax.gov.cn/{img}'
                    if 'icons' in img:
                        img = ''
                        content.append(img)
                    else:
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
                    content.append(''.join(line.xpath('.//text()')))
                    content.append(f"<a>{''.join(line.xpath('.//a//text()'))}</a>")
            # 判断当前行是否包含strong标签
            elif line.xpath('.//strong') != [] or line.xpath('.//strong') != []:
                values = []
                # 如果有strong，循环行里的所有元素
                for value in line.xpath('./strong|./text()'):
                    if isinstance(value, str):
                        values.append(value)
                    else:
                        values.append(f"<special>{''.join(value.xpath('.//text()'))}</special>")
                content.append(''.join(values).strip())
            elif line.tag == 'strong' or line.tag == 'b':
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
                # urlPre = re.sub('[^/]+(?=.*/)', '', articleUrl)
                url = f'http://liaoning.chinatax.gov.cn{url}'
            # if '../../' in url:
            #     urlPre1 = re.sub('[^/]+(?=.*/)', '', urlPre)
            #     url = url.replace('../../', urlPre1)
            else:
                # url = url.replace('./', urlPre)
                url = url
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
            "爬取网站": "辽宁省税务局",
            "国家/地区": '中国',
            "省/州": '辽宁',
            "市": None,
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

    def get_detail_data(self, singleObj, types, urlPre, domain):
        if domain == '辽宁省税务局官网-政策文件-最新文件':
            data = self.get_data_model()
            # 爬取时间
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # 文章标题
            articleTitle = singleObj.xpath('.//a/@title')[0]
            # 文章链接
            articleUrl = singleObj.xpath('.//a/@href')[0]
            contentSource = self.request_get(url=articleUrl)
            contentHtmlElement = etree.HTML(contentSource)
            articleId = hashlib.md5(articleUrl.encode(encoding='utf-8')).hexdigest()
            issueNumber = re.findall('\[字号\]>begin-->(.*?)<', contentSource)[0]
            articleSource = re.findall('\[发文单位\]>begin-->(.*?)<', contentSource)[0]
            contents = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]|//div[@class="info-cont zoom"]/p[.//img]|//div[@class="info-cont zoom"]/p/strong|//div[@class="info-cont zoom"]/p/b')
            content = self.get_content(contents, articleUrl)
            # 正文内容
            publishDate_pre = contentHtmlElement.xpath('//meta[@name="PubDate"]|//meta[@name="pubDate"]')
            if publishDate_pre:
                publishDate = publishDate_pre[0].get('content')
            else:
                publishDate = None
            publishDate = str(publishDate) + ':00'
            # 获取正文附件
            aTags = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]//a|//div[@class="info-cont zoom"]/p[.//img]//a|//div[@class="info-cont zoom"]/p/strong//a|//div[@class="info-cont zoom"]/p/b//a')
            attFiles = self.get_att_file(contents=aTags, articleUrl=articleUrl, urlPre1=urlPre)
            aCountNub = len(aTags)
            oldTexts = attFiles['oldTexts']
            Urls = attFiles['Urls']
            fileTypes = attFiles['fileTypes']
            str1 = contentHtmlElement.xpath('//div[@id="pdfCon"]/script[@type = "text/javascript"]/text()')
            if str1 != []:
                extenalFileUrl = re.findall('window.open\(commonZb.getUrlParam\("(.*?)",', str1[0])
                extenalFileUrl = f'http://liaoning.chinatax.gov.cn{extenalFileUrl[0]}'
                extenalFileNames = contentHtmlElement.xpath('//p[@id = "pdfText"]/text()')
            else:
                extenalFileUrl = attFiles['extenalFileUrl']
                extenalFileNames = attFiles['extenalFileNames']
            if re.search('[^.]+(?!.*.)', articleUrl).group() != 'html':
                publishDate = ''.join(singleObj.xpath('./span//text()')) + ' 00:00:00'
                oldTexts.append(articleTitle)
                Urls.append(articleUrl)
                fileTypes.append(re.search('[^.]+(?!.*.)', articleUrl).group())
            # 判断是否超过时间范围
            publishDatecheck = time.strptime(publishDate, "%Y-%m-%d %H:%M:%S")
            publishDatecheck = int(time.mktime(publishDatecheck))
            # 设置抓取时间
            lastTimeCheck = "2022-09-01 00:00:00"
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
            # 截取文章标题最后2个字，判断文章类型
            key = articleTitle[-2:]
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
        elif domain == '辽宁省税务局官网-信息公开-通知公告':
            data = self.get_data_model()
            # 爬取时间
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # 文章标题
            articleTitle = singleObj.xpath('.//a/@title')
            # 文章链接
            articleUrl = singleObj.xpath('.//a/@href')[0]
            contentSource = self.request_get(url=articleUrl)
            contentHtmlElement = etree.HTML(contentSource)
            articleId = hashlib.md5(articleUrl.encode(encoding='utf-8')).hexdigest()
            issueNumber = None
            articleSource = re.findall('信息来源]>begin-->(.*?)<', contentSource)
            if articleSource:
                articleSource = re.findall('信息来源]>begin-->(.*?)<', contentSource)[0]
            else:
                articleSource = []
            contents = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]|//div[@class="info-cont zoom"]/p[.//img]|//div[@class="info-cont zoom"]/p/strong|//div[@class="info-cont zoom"]/p/b')
            content = self.get_content(contents, articleUrl)
            publishDate_pre = contentHtmlElement.xpath('//meta[@name="pubdate"]|//meta[@name="Pubdate"]')
            if publishDate_pre:
                publishDate = publishDate_pre[0].get('content')
                publishDate = str(publishDate) + ':00'
            else:
                publishDate = None
            if publishDate == None:
                publishDate = singleObj.xpath('.//span/text()')[0]
                publishDate = str(publishDate) + ' 00:00:00'

            aTags = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]//a|//div[@class="info-cont zoom"]/p[.//img]//a|//div[@class="info-cont zoom"]/p/strong//a|//div[@class="info-cont zoom"]/p/b//a')
            attFiles = self.get_att_file(contents=aTags, articleUrl=articleUrl, urlPre1=urlPre)
            aCountNub = len(aTags)
            oldTexts = attFiles['oldTexts']
            Urls = attFiles['Urls']
            fileTypes = attFiles['fileTypes']
            str1 = contentHtmlElement.xpath('//div[@id="pdfCon"]/script[@type = "text/javascript"]/text()')
            if str1 != []:
                extenalFileUrl = re.findall('window.open\(commonZb.getUrlParam\("(.*?)",', str1[0])
                extenalFileUrl = f'http://liaoning.chinatax.gov.cn{extenalFileUrl[0]}'
                extenalFileNames = contentHtmlElement.xpath('//p[@id = "pdfText"]/text()')
            else:
                extenalFileUrl = attFiles['extenalFileUrl']
                extenalFileNames = attFiles['extenalFileNames']
            if re.search('[^.]+(?!.*.)', articleUrl).group() != 'html':
                publishDate = ''.join(singleObj.xpath('./span//text()')) + ' 00:00:00'
                oldTexts.append(articleTitle)
                Urls.append(articleUrl)
                fileTypes.append(re.search('[^.]+(?!.*.)', articleUrl).group())

            # 判断是否超过时间范围
            publishDatecheck = time.strptime(publishDate, "%Y-%m-%d %H:%M:%S")
            publishDatecheck = int(time.mktime(publishDatecheck))
            # 设置抓取时间
            lastTimeCheck = "2022-09-01 00:00:00"
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
        elif domain == '辽宁省税务局官网-纳税服务-下载中心':
            data = self.get_data_model()
            # 爬取时间
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # 文章标题
            articleTitle = singleObj.xpath('.//a/@title')
            # 文章链接
            articleUrl = singleObj.xpath('.//a/@href')[0]
            contentSource = self.request_get(url=articleUrl)
            contentHtmlElement = etree.HTML(contentSource)
            articleId = hashlib.md5(articleUrl.encode(encoding='utf-8')).hexdigest()
            issueNumber = None
            articleSource = re.findall('信息来源]>begin-->(.*?)<', contentSource)
            if articleSource:
                articleSource = re.findall('信息来源]>begin-->(.*?)<', contentSource)[0]
            else:
                articleSource = []
            contents = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]|//div[@class="info-cont zoom"]/p[.//img]|//div[@class="info-cont zoom"]/p/strong|//div[@class="info-cont zoom"]/p/b')
            content = self.get_content(contents, articleUrl)
            publishDate_pre = contentHtmlElement.xpath('//meta[@name="pubdate"]|//meta[@name="Pubdate"]')
            if publishDate_pre:
                publishDate = publishDate_pre[0].get('content')
                publishDate = str(publishDate) + ':00'
            else:
                publishDate = None
            if publishDate == None:
                publishDate = singleObj.xpath('.//span/text()')[0]
                publishDate = str(publishDate) + ' 00:00:00'

            aTags = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]//a|//div[@class="info-cont zoom"]/p[.//img]//a|//div[@class="info-cont zoom"]/p/strong//a|//div[@class="info-cont zoom"]/p/b//a')
            attFiles = self.get_att_file(contents=aTags, articleUrl=articleUrl, urlPre1=urlPre)
            aCountNub = len(aTags)
            oldTexts = attFiles['oldTexts']
            Urls = attFiles['Urls']
            fileTypes = attFiles['fileTypes']
            str1 = contentHtmlElement.xpath('//div[@id="pdfCon"]/script[@type = "text/javascript"]/text()')
            if str1 != []:
                extenalFileUrl = re.findall('window.open\(commonZb.getUrlParam\("(.*?)",', str1[0])
                extenalFileUrl = f'http://liaoning.chinatax.gov.cn{extenalFileUrl[0]}'
                extenalFileNames = contentHtmlElement.xpath('//p[@id = "pdfText"]/text()')
            else:
                extenalFileUrl = attFiles['extenalFileUrl']
                extenalFileNames = attFiles['extenalFileNames']
            if re.search('[^.]+(?!.*.)', articleUrl).group() != 'html':
                publishDate = ''.join(singleObj.xpath('./span//text()')) + ' 00:00:00'
                oldTexts.append(articleTitle)
                Urls.append(articleUrl)
                fileTypes.append(re.search('[^.]+(?!.*.)', articleUrl).group())

            # 判断是否超过时间范围
            publishDatecheck = time.strptime(publishDate, "%Y-%m-%d %H:%M:%S")
            publishDatecheck = int(time.mktime(publishDatecheck))
            # 设置抓取时间
            lastTimeCheck = "2022-09-01 00:00:00"
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
        elif domain == '辽宁省税务局官网-政策文件-政策解读':
            data = self.get_data_model()
            # 爬取时间
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            # 文章标题
            articleTitle = singleObj.xpath('.//a/@title')
            # 文章链接
            articleUrl = singleObj.xpath('.//a/@href')[0]
            contentSource = self.request_get(url=articleUrl)
            contentHtmlElement = etree.HTML(contentSource)
            articleId = hashlib.md5(articleUrl.encode(encoding='utf-8')).hexdigest()
            issueNumber = None
            articleSource = re.findall('信息来源]>begin-->(.*?)<', contentSource)
            if articleSource:
                articleSource = re.findall('信息来源]>begin-->(.*?)<', contentSource)[0]
            else:
                articleSource = []
            contents = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]|//div[@class="info-cont zoom"]/p[.//img]|//div[@class="info-cont zoom"]/p/strong|//div[@class="info-cont zoom"]/p/b')
            content = self.get_content(contents, articleUrl)
            publishDate_pre = contentHtmlElement.xpath('//meta[@name="pubdate"]|//meta[@name="Pubdate"]')
            if publishDate_pre:
                publishDate = publishDate_pre[0].get('content')
                publishDate = str(publishDate) + ':00'
            else:
                publishDate = None
            if publishDate == None:
                publishDate = singleObj.xpath('.//span/text()')[0]
                publishDate = str(publishDate) + ' 00:00:00'

            aTags = contentHtmlElement.xpath(
                '//div[@class="info-cont zoom"]/p[.//text()]//a|//div[@class="info-cont zoom"]/p[.//img]//a|//div[@class="info-cont zoom"]/p/strong//a|//div[@class="info-cont zoom"]/p/b//a')
            attFiles = self.get_att_file(contents=aTags, articleUrl=articleUrl, urlPre1=urlPre)
            aCountNub = len(aTags)
            oldTexts = attFiles['oldTexts']
            Urls = attFiles['Urls']
            fileTypes = attFiles['fileTypes']
            str1 = contentHtmlElement.xpath('//div[@id="pdfCon"]/script[@type = "text/javascript"]/text()')
            if str1 != []:
                extenalFileUrl = re.findall('window.open\(commonZb.getUrlParam\("(.*?)",', str1[0])
                extenalFileUrl = f'http://liaoning.chinatax.gov.cn{extenalFileUrl[0]}'
                extenalFileNames = contentHtmlElement.xpath('//p[@id = "pdfText"]/text()')
            else:
                extenalFileUrl = attFiles['extenalFileUrl']
                extenalFileNames = attFiles['extenalFileNames']
            if re.search('[^.]+(?!.*.)', articleUrl).group() != 'html':
                publishDate = ''.join(singleObj.xpath('./span//text()')) + ' 00:00:00'
                oldTexts.append(articleTitle)
                Urls.append(articleUrl)
                fileTypes.append(re.search('[^.]+(?!.*.)', articleUrl).group())

            # 判断是否超过时间范围
            publishDatecheck = time.strptime(publishDate, "%Y-%m-%d %H:%M:%S")
            publishDatecheck = int(time.mktime(publishDatecheck))
            # 设置抓取时间
            lastTimeCheck = "2022-09-01 00:00:00"
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
        else:
            data = self.get_data_model()
            # 爬取时间
            currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            content = singleObj['faxInfo']
            publishDate = singleObj['startTime']
            # 正文中的链接 待取值
            # 判断是否超过时间范围
            publishDate = publishDate + ' 00:00:00'
            publishDatecheck = time.strptime(publishDate, "%Y-%m-%d %H:%M:%S")
            publishDatecheck = int(time.mktime(publishDatecheck))
            # 设置抓取时间
            lastTimeCheck = "2022-09-01 00:00:00"
            lastTimeCheck = time.strptime(lastTimeCheck, "%Y-%m-%d %H:%M:%S")
            lastTimeCheck = int(time.mktime(lastTimeCheck))
            # 如果当前数据日期超出抓取范围，返回 0
            if publishDatecheck < lastTimeCheck:
                return 0
            data['文章类型'] = domain
            data['发文号'] = None
            data['法规名称/通知名称/法规新闻标题'] = None
            data['页面链接(信息来源)'] = None
            data['正文'] = content
            data['发文日期'] = publishDate
            data['创建时间'] = currentTime
            data['更新时间'] = currentTime
            data['爬取日期'] = currentTime
            data['来源'] = None
            data['超链接原始文本'] = None
            data['超链接'] = None
            data['附件文件名'] = None
            data['附件链接'] = None
            data['附件文件'] = None
            data['文章编号'] = None
            data['a标签数量'] = None
            data['超链接数量'] = None
            self.upload(data)
            return data

    def request_get(self, url):
        count = 0
        payload = {}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'
        }
        while True:
            try:
                response = requests.request("GET", url, headers=headers, timeout=5)
                # response.encoding = response.apparent_encoding
                encoding = cchardet.detect(response.content)['encoding']
                response = response.content.decode(encoding)
                return response
            except:
                count += 1
            finally:
                if count > 10:
                    return "请求失败"

    def request_post(self, url, x, y):
        count = 0
        x = x
        y = y
        payload = {'startrecord': f'{x}',
                   'endrecord': f'{y}',
                   'perpage': '15',
                   'col': '1',
                   'webid': '1',
                   'path': 'http://liaoning.chinatax.gov.cn/',
                   'columnid': '46',
                   'sourceContentType': '1',
                   'unitid': '17901',
                   'webname': '国家税务总局辽宁省税务局',
                   'permissiontype': '0'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'

        }
        # cookies = {
        #     'JSESSIONID=FBEFDF7275B7D1A8A64493EE86A184CF; zh_choose_1=s; yfx_c_g_u_id_10003721=_ck23090615185416872753845764275; yfx_f_l_v_t_10003721=f_t_1693984734671__r_t_1694151581255__v_t_1694155780225__r_c_3'}
        while True:
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
                # response.encoding = response.apparent_encoding
                encoding = cchardet.detect(response.content)['encoding']
                response = response.content.decode(encoding)
                return response
            except:
                count += 1
            finally:
                if count > 10:
                    return "请求失败"

    def request_post2(self, url, x, y):
        count = 0
        x = x
        y = y
        payload = {'startrecord': f'{x}',
                   'endrecord': f'{y}',
                   'perpage': '15',
                   'col': '1',
                   'webid': '1',
                   'path': 'http://liaoning.chinatax.gov.cn/',
                   'columnid': '1975',
                   'sourceContentType': '1',
                   'unitid': '17884',
                   'webname': '国家税务总局辽宁省税务局',
                   'permissiontype': '0'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'

        }
        # cookies = {
        #     'JSESSIONID=FBEFDF7275B7D1A8A64493EE86A184CF; zh_choose_1=s; yfx_c_g_u_id_10003721=_ck23090615185416872753845764275; yfx_f_l_v_t_10003721=f_t_1693984734671__r_t_1694151581255__v_t_1694155780225__r_c_3'}
        while True:
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
                # response.encoding = response.apparent_encoding
                encoding = cchardet.detect(response.content)['encoding']
                response = response.content.decode(encoding)
                return response
            except:
                count += 1
            finally:
                if count > 10:
                    return "请求失败"

    def request_post3(self, url, x, y):
        count = 0
        x = x
        y = y
        payload = {'startrecord': f'{x}',
                   'endrecord': f'{y}',
                   'perpage': '15',
                   'col': '1',
                   'webid': '1',
                   'path': 'http://liaoning.chinatax.gov.cn/',
                   'columnid': '1778',
                   'sourceContentType': '1',
                   'unitid': '9237',
                   'webname': '国家税务总局辽宁省税务局',
                   'permissiontype': '0'}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67'

        }
        # cookies = {
        #     'JSESSIONID=FBEFDF7275B7D1A8A64493EE86A184CF; zh_choose_1=s; yfx_c_g_u_id_10003721=_ck23090615185416872753845764275; yfx_f_l_v_t_10003721=f_t_1693984734671__r_t_1694151581255__v_t_1694155780225__r_c_3'}
        while True:
            try:
                response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
                # response.encoding = response.apparent_encoding
                encoding = cchardet.detect(response.content)['encoding']
                response = response.content.decode(encoding)
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
            # with pd.ExcelWriter(filePath, mode='a', engine="xlsxwriter", options={'strings_to_urls': False}) as writer:
            with pd.ExcelWriter(filePath, mode='a', engine="openpyxl") as writer:
                pd.DataFrame(addData).to_excel(writer, index=None)
        else:
            with pd.ExcelWriter(filePath) as writer:
                pd.DataFrame(addData).to_excel(writer, index=None)

    def crawl_thread(self, page, urlPre, domain, mycol, types):
        # 列表页源码
        url = urlPre
        break_out = False
        if domain == '辽宁省税务局官网-政策文件-最新文件':
            while True:
                list = []
                if page == 0:
                    listSource = self.request_get(url)
                    listHtmlElement = etree.HTML(listSource)
                    list = listHtmlElement.xpath('//ul//li[contains(@class,"zcfgk zcfgk")]')
                if list == []:
                    break_out = True
                else:
                    print(f'正在爬取{domain}页...')
                    page += 1
                    for single in list:
                        data = self.get_detail_data(single, types, urlPre, domain)
                        # print(data)
                        if data == 0:
                            return 0
                        x = mycol.insert_one(data)
                        # # 将要写入excel的数据存入容器addData
                        for add in addData.keys():
                            addData[add].append(data[add])

                if break_out == True:
                    break
        elif domain == '辽宁省税务局官网-信息公开-通知公告':
            while True:
                for x in range(1, 1000, 45):
                    y = x + 44
                    print(x, y)
                    url = f'http://liaoning.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={x}&endrecord={y}&perpage=15'
                    listSource = self.request_post(url, x, y)
                    content = re.findall('<li(.*?)</li>', listSource)
                    html = []
                    for i in content:
                        content = f'<li{i}</li>'
                        html.append(content)
                    html = ''.join(html)
                    if html:
                        listHtmlElement = etree.HTML(html)
                        list = listHtmlElement.xpath('//li')
                    else:
                        list = []
                    if list == []:
                        break_out = True
                        break
                    else:
                        print(f'正在爬取{domain}页...')
                        for single in list:
                            data = self.get_detail_data(single, types, urlPre, domain)
                            print(data)
                            if data == 0:
                                return 0
                            x = mycol.insert_one(data)
                            # # 将要写入excel的数据存入容器addData
                            for add in addData.keys():
                                addData[add].append(data[add])
                            # print(x)
                if break_out == True:
                    break
        elif domain == '辽宁省税务局官网-纳税服务-下载中心':
            while True:
                for x in range(1, 1000, 45):
                    y = x + 44
                    print(x, y)
                    url = f'http://liaoning.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={x}&endrecord={y}&perpage=15'
                    listSource = self.request_post2(url, x, y)
                    content = re.findall('<li(.*?)</li>', listSource)
                    html = []
                    for i in content:
                        content = f'<li{i}</li>'
                        html.append(content)
                    html = ''.join(html)
                    if html:
                        listHtmlElement = etree.HTML(html)
                        list = listHtmlElement.xpath('//li')
                    else:
                        list = []
                    if list == []:
                        break_out = True
                        break
                    print(f'正在爬取{domain}页...')
                    for single in list:
                        data = self.get_detail_data(single, types, urlPre, domain)
                        print(data)
                        if data == 0:
                            return 0
                        x = mycol.insert_one(data)
                        # # 将要写入excel的数据存入容器addData
                        for add in addData.keys():
                            addData[add].append(data[add])
                        # print(x)
                if break_out == True:
                    break
        elif domain == '辽宁省税务局官网-政策文件-政策解读':
            while True:
                for x in range(1, 1000, 45):
                    y = x + 44
                    print(x, y)
                    url = f'http://liaoning.chinatax.gov.cn/module/web/jpage/dataproxy.jsp?startrecord={x}&endrecord={y}&perpage=15'
                    listSource = self.request_post3(url, x, y)
                    content = re.findall('<li(.*?)</li>', listSource)
                    html = []
                    for i in content:
                        content = f'<li{i}</li>'
                        html.append(content)
                    html = ''.join(html)
                    if html:
                        listHtmlElement = etree.HTML(html)
                        list = listHtmlElement.xpath('//li')
                    else:
                        list = []
                    if list == []:
                        break_out = True
                        break
                    else:
                        print(f'正在爬取{domain}页...')
                        for single in list:
                            data = self.get_detail_data(single, types, urlPre, domain)
                            print(data)
                            if data == 0:
                                return 0
                            x = mycol.insert_one(data)
                            # # 将要写入excel的数据存入容器addData
                            for add in addData.keys():
                                addData[add].append(data[add])
                            # print(x)
                if break_out == True:
                    break
        else:
            while True:
                currentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                currentYear = int(currentTime[0:4])
                for year in range(2023, currentYear + 1):
                    for month in range(1, 13):
                        if month < 10:
                            month = '0' + str(month)
                        if year == currentYear and month == 12:
                            break_out = True
                        url = f'http://liaoning.chinatax.gov.cn/dlzw/zqrl/lavyDateInfo.do?year={year}&month={month}&stamp=0.29639607472102547'
                        res = requests.get(url).text
                        print(res)
                        single = res.replace('[', '').replace(']', '')
                        print(single)
                        single = json.loads(single)
                        if single:
                            data = self.get_detail_data(single, types, urlPre, domain)
                            print(data)
                            if data == 0:
                                continue
                            x = mycol.insert_one(data)
                            # # 将要写入excel的数据存入容器addData
                            for add in addData.keys():
                                addData[add].append(data[add])
                                # print(addData)
                if break_out == True:
                    break

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
            # wd = uc.Chrome()
            # 链接数据库
            mycol = self.get_db_conect('beijing_test3')
            # 用于匹配文章类型
            types = ['公告', '通知', '政策指引', '问答', '政策解读', '操作指南', '法律', '规定', '办法', '规则', '制度',
                     '决定', '规程', '目录']
            domains = {

                '辽宁省税务局官网-政策文件-最新文件': 'http: // liaoning.chinatax.gov.cn / col / col1777 / index.html',

                # '辽宁省税务局官网-信息公开-通知公告': 'http: // liaoning.chinatax.gov.cn / col / col46 / index.html',
                #
                # '辽宁省税务局官网-纳税服务-下载中心': 'http: // liaoning.chinatax.gov.cn / col / col1975 / index.html',

                # '辽宁省税务局官网-纳税服务-办税日历': 'http: // liaoning.chinatax.gov.cn / col / col5211 / index.html',

                # '辽宁省税务局官网-政策文件-政策解读': 'http: // liaoning.chinatax.gov.cn / col / col1778 / index.html',
            }
            # 多线程
            thread_list = []
            for domain in domains:
                urlPre = domains[domain].replace(' ', '')
                # print(urlPre)
                page = 0
                t = threading.Thread(target=self.crawl_thread,
                                     args=(page, urlPre, domain, mycol, types))
                t.start()
                thread_list.append(t)
            for t in thread_list:
                t.join()
            # print(addData)
            self.save_to_excel(filePath='辽宁省财政局.xlsx', addData=addData)
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
