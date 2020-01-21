import os

import requests
from pyquery import PyQuery as Pq

requests.urllib3.disable_warnings()


def get_page(url, filename):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/79.0.3945.117 Safari/537.36 ",
        "Referer": "https://blog.csdn.net/whatday/article/list/1"
    }
    folder = 'cached'
    # 建立 cached 文件夹
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = os.path.join(folder, filename)
    if os.path.exists(path):
        with open(path, 'rb') as f:
            s = f.read()
            return s
    else:
        # 发送网络请求, 把结果写入到文件夹中
        r = requests.get(
            url=url,
            headers=headers,
            verify=False,
        )
        page = r.content
        with open(path, 'wb') as f:
            f.write(page)
            return page


def create_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def save_md(page, name):
    e = Pq(page)
    md = e(".blog-content-box .htmledit_views")
    pic = md("img")

    for p in pic.items():
        pic_path = p.attr("src")
        print(pic_path)
        # TODO: 图片下载和地址替换
        ###

    folder = "md"
    create_folder(folder)
    filename = "{}.md".format(name)
    path = os.path.join(folder, filename)
    if not os.path.exists(path):
        with open(path, 'w', encoding="UTF8") as f:
            f.write(str(md))


def cached_page(url):
    """
    保存缓存页面
    """
    page_dic = {}
    filename = '{}.html'.format(url.split('/')[-1])
    page = get_page(url, filename)
    e = Pq(page)
    # tmp = e('.article-list .article-item-box.csdn-tracking-statistics .h4')
    # print(tmp)
    items = e('.article-list .article-item-box.csdn-tracking-statistics').items()
    for i in items:
        k = i.attr("data-articleid")
        v = str(i("h4")("a").text())
        page_dic[k] = v
    for p in page_dic.items():
        url = "https://blog.csdn.net/whatday/article/details/{}".format(p[0])
        print(p[0], p[1])
        page = get_page(url, "{}.html".format(p[0]))
        save_md(page, p[0])
    # items = items.children(".article-item-box.csdn-tracking-statistics")
    # print(items)
    return page


def main():
    # git test..
    # url = "https://blog.csdn.net/whatday/article/details/103953281"
    for i in range(1, 56):
        url = "https://blog.csdn.net/whatday/article/list/{}".format(i)
        # url = "https://blog.csdn.net/whatday/article/list/1"
        cached_page(url)
        print("第{}页".format(i))


if __name__ == "__main__":
    main()
