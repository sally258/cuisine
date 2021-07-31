import requests
from bs4 import BeautifulSoup
from Database import *
import codecs

helper = DBHelper('localhost', '3306', 'root', 'password', 'cuisine')

def createTable():
    """
    Tạo các bảng để lưu trữ dữ liệu
    :return:
    """
    # sql = "create table TAG(tag nvarchar(255) primary key)"
    # helper.createTable(sql)

    sql = "create table DISH(link varchar(255) primary key, title varchar(255), dish_name varchar(255), content MEDIUMTEXT)"
    helper.createTable(sql)

def getLinks():
    """
    Lấy đường dẫn và tiêu đề của tất cả bài viết về cách làm món ăn lưu vào database
    :return: None --
    """
    web_str = "https://vnexpress.net"

    req_thucdon = requests.get("https://vnexpress.net/doi-song/cooking/thuc-don")
    soup_thucdon = BeautifulSoup(req_thucdon.text, features='html.parser')
    k = 0
    for h3_thucdon in soup_thucdon.findAll('h3'):
        if h3_thucdon.get('class') == ['title_news']:
            a_thucdon = h3_thucdon.find('a')
            href_thucdon = web_str + a_thucdon.get('href')

            req_monan = requests.get(href_thucdon)
            soup_monan = BeautifulSoup(req_monan.text, features='html.parser')

            i = 1
            while True:
                link = href_thucdon + "-p" + str(i)
                req_link = requests.get(link)
                # điều kiện dừng hết trang để truy cập
                if i > 1 and req_link.url == href_thucdon:
                    break

                soup_link = BeautifulSoup(req_link.text, features='html.parser')
                for h2_link in soup_link.findAll('h2'):
                    if h2_link.get('class') == ['title_news']:
                        a_link = h2_link.find('a')
                        href = a_link.get('href')
                        title = a_link.get('title')

                        sql = "insert into dish(link, title) values(%s, %s)"
                        params = (href, title)
                        helper.insert(sql, *params)

                for h3_link in soup_link.findAll('h3'):
                    if h3_link.get('class') == ['title_news']:
                        a_link = h3_link.find('a')
                        href = a_link.get('href')
                        title = a_link.get('title')

                        sql = "insert into dish(link, title) values(%s, %s)"
                        params = (href, title)
                        helper.insert(sql, *params)
                i += 1

def getContent(link: str):
    """
    Lấy nội dung dựa trên link đã biết, đưa vào file content.txt
    :param link:
    :return:
    """
    req = requests.get(link)
    soup = BeautifulSoup(req.text, features='html.parser')

    if len(soup.findAll('h2')) > 0:
        # Mẫu dữ liệu được chia thành hai cột là nguyên liệu và cách làm
        file = codecs.open('content.txt', 'w', encoding='utf-8')

        h1 = soup.find('h1').text  # tiêu đề của bài viết
        file.write(h1 + '\n')

        # mô tả của bài viết
        for p_description in soup.findAll('p'):
            if p_description.get('class') == ['description']:
                file.write(p_description.text + '\n')

        # nguyên liệu
        file.write('\nNguyên liệu:\n')
        for li in soup.findAll('li'):
            ip = li.find('input')
            if ip != None and ip.get('type') == 'checkbox':
                file.write(ip['value'] + '\n')

        # cách làm
        file.write('\nCách làm:\n')
        i = 1
        for li in soup.findAll('li'):
            if li.get('class') == ['Normal']:
                text = str(i) + '. ' + li.text + '\n'
                file.write(text)
                i += 1

        file.write('\n')
        for p in soup.findAll('p'):
            if p.get('class') == ['Normal']:
                file.write(p.text + '\n')

        file.close()
    else:
        # Mẫu dữ liệu khi không được chia thành hai cột
        file = codecs.open('content.txt', 'w', encoding='utf-8')
        h1 = soup.find('h1').text  # tiêu đề của bài viết
        file.write(h1 + '\n')

        # mô tả của bài viết
        for p_description in soup.findAll('p'):
            if p_description.get('class') == ['description']:
                file.write(p_description.text + '\n')

        # nội dung bài viết
        for p in soup.findAll('p'):
            if p.get('class') == ['Normal']:
                file.write(p.text + '\n')
        file.close()

def setContent():
    """
    Đưa nội dung của từng link vào cơ sở dữ liệu ở cột content bảng dish
    :return: 
    """

    sql = "select link from dish" # lấy tất cả đường dẫn có trong cơ sở dữ liệu

    i = 1
    for link in helper.select(sql):

        getContent(link[0])
        file = codecs.open("content.txt", "r", encoding='utf-8')
        st = file.read()
        sql = "update dish set content = %s where link = %s"
        params = (st, link[0])
        helper.update(sql, *params)
        file.close()

        print("Đã xong", i, "món ăn")
        i += 1

def getDishName():
    """
    Lấy tất cả tên các món ăn có trong cơ sở dữ liệu lưu vào file dishname.txt
    :return:
    """
    file = codecs.open('dishname.txt', 'w', encoding='utf-8')

    sql = "select dish_name from dish"
    for dish_name in helper.select(sql):
        file.write(dish_name[0]+'\n')

    file.close()
if __name__ == '__main__':
    # createTable()
    # getLinks()
    # setContent()
    getDishName()
    pass
