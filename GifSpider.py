import requests
import time
import os
import threading
import re
from bs4 import BeautifulSoup

n = 0

path = 'D:\\gif_full\\'
if not (os.path.exists(path)):
    os.makedirs(path)

my_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0',
}


class DownloadGif(threading.Thread):
    def __init__(self, parameter):
        threading.Thread.__init__(self)
        self.parameter = parameter

    def run(self):
        global n
        for index in self.parameter:
            main_index = 'http://siji.party/?cate=all&page=' + str(index)
            response_main = requests.get(main_index)
            if response_main.status_code == 200:
                tag_a = BeautifulSoup(response_main.content, 'html.parser').select('a')
                for href in tag_a:
                    tag_href = str(href.get('href'))
                    if '/p/' in tag_href:
                        url_p = 'http://siji.party' + tag_href
                        response_p = requests.get(url=url_p, headers=my_headers)
                        if response_p.status_code == 200:
                            tag_img = BeautifulSoup(response_p.content, 'html.parser').select('img')
                            for src in tag_img:
                                url_img = str(src.get('src'))
                                if url_img.endswith('.gif'):
                                    if re.match(r'^https?:/{2}\w.+$', url_img):
                                        time_start = time.time()
                                        response_img = requests.get(url=url_img, headers=my_headers)
                                        time_end = time.time()
                                        time_used = time_end - time_start
                                        if response_img.status_code == 200:
                                            info_one = url_p, url_img, '下载完成', '耗时', str(time_used)
                                            print(info_one)
                                            name = path + str(n) + '.gif'
                                            content_one = str(info_one) + '\n' + name + '\n'
                                            with open(name, 'wb') as gif:
                                                gif.write(response_img.content)
                                            with open(path + "log.txt", 'a') as log:
                                                log.write(content_one)
                                            print(name, '写入完成')
                                            n = n + 1
                                            print('当前线程数量', threading.active_count())
                                        else:
                                            info_tow = url_p, url_img, '文件失效'
                                            print(info_tow)
                                    else:
                                        info_three = url_p, url_img, 'URL格式错误'
                                        print(info_three)
                                else:
                                    info_four = url_p, url_img, '未找到GIF'
                                    print(info_four)
                        else:
                            info_five = url_p, '失去响应'
                            print(info_five)
                    else:
                        info_six = tag_href, '不是正确的链接'
                        print(info_six)
            else:
                info_seven = main_index, '失去响应'
                print(info_seven)


class Task:
    def __init__(self, end, threads):
        self.end = end
        self.threads = threads

    def start(self):
        list_task = set()
        step = int(self.end / self.threads)
        for thread in range(self.threads):
            list_task.add(range(thread * step, thread * step + step))
        for i in list_task:
            t = DownloadGif(i)
            t.start()


if __name__ == '__main__':
    T = Task(550, 10)
    T.start()
