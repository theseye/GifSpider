import requests
import time
import os
import threading
import re
from bs4 import BeautifulSoup

n = 0
lock = threading.Lock()

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
        for index in self.parameter:
            main_page = 'http://siji.party/?cate=all&page=' + str(index)
            response_main = requests.get(main_page)
            if response_main.status_code == 200:
                tag_a = BeautifulSoup(response_main.content, 'html.parser').select('a')
                url_p = set()
                for a in tag_a:
                    tag_href = str(a.get('href'))
                    if '/p/' in tag_href:
                        url_p.add('http://siji.party' + tag_href)
                    else:
                        info_one = tag_href, '不是正确的链接'
                        print(info_one)
                for p in url_p:
                    response_p = requests.get(url=p, headers=my_headers)
                    if response_p.status_code == 200:
                        tag_img = BeautifulSoup(response_p.content, 'html.parser').select('img')
                        for img in tag_img:
                            url_img = str(img.get('src'))
                            if url_img.endswith('.gif'):
                                if re.match(r'^https?:/{2}\w.+$', url_img):
                                    time_start = time.time()
                                    response_img = requests.get(url=url_img, headers=my_headers)
                                    time_end = time.time()
                                    time_used = time_end - time_start
                                    if response_img.status_code == 200:
                                        lock.acquire()
                                        global n
                                        name = path + str(n) + '.gif'
                                        with open(name, 'wb') as gif:
                                            gif.write(response_img.content)
                                        info_two = main_page, p, url_img, '下载完成', '耗时', time_used, name, '写入完成'
                                        with open(path + "!log.txt", 'a') as log:
                                            log.write(str(info_two) + '\r\n')
                                        print(info_two)
                                        print('当前线程数量', threading.active_count())
                                        n = n + 1
                                        lock.release()
                                    else:
                                        info_three = p, url_img, '文件失效'
                                        print(info_three)
                                else:
                                    info_four = p, url_img, 'URL格式错误'
                                    print(info_four)
                            else:
                                info_five = p, url_img, '未找到GIF'
                                print(info_five)
                    else:
                        info_six = p, '失去响应'
                        print(info_six)
            else:
                info_seven = main_page, '失去响应'
                print(info_seven)


class Task:
    def __init__(self, end, threads):
        self.end = end
        self.threads = threads

    def start(self):
        list_task = []
        step = int(self.end / self.threads)
        for thread in range(self.threads):
            list_task.append(range(thread * step, thread * step + step))
        for i in list_task:
            t = DownloadGif(i)
            t.start()


if __name__ == '__main__':
    T = Task(550, 100)
    T.start()
