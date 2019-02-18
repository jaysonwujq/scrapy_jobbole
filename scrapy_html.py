import requests
from requests import exceptions
import re

def get_html(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    headers = {'User-Agent': user_agent}
    try:
        res = requests.get(url, headers=headers)
        return res.text
    except exceptions.Timeout as e:
        print(e)

def get_link(html):
    reg = r'href="(.*?wechat_redirect)" target="_blank">(.*?)</a>'
    link_pattern = re.compile(reg)
    link_list = re.findall(link_pattern, html)
    return link_list

def save_html(url, name):
    name = name.replace('（', '').replace('）', '').replace('：', '-').replace(':', '-')
    with open(r'./html/%s.html'%name, 'w', encoding='utf8') as fo:
        res = get_html(url)
        fo.write(res)


if __name__ =='__main__':
    res = get_html('http://www.biotrainee.com/thread-1376-1-1.html')
    save_html('http://www.biotrainee.com/thread-1376-1-1.html', '直播我的基因组分析')
    link = get_link(res)
    #print(link)
    for i in link:
       save_html(i[0], i[1])
