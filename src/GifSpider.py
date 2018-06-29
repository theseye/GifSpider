import requests
import time
import os
import threading
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
            response = requests.get(main_index)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                a = soup.select('a')
                for href in a:
                    img_index = str(href.get('href'))
                    if '/p/' in img_index:
                        img_url = 'http://siji.party' + img_index
                        _response = requests.get(url=img_url, headers=my_headers)
                        if _response.status_code == 200:
                            _soup = BeautifulSoup(_response.content, 'html.parser')
                            _img = _soup.select('img')
                            for src in _img:
                                img = str(src.get('src'))
                                if img.endswith('.gif'):
                                    # noinspection PyBroadException
                                    try:
                                        time_start = time.time()
                                        r = requests.get(url=img, headers=my_headers)
                                        time_end = time.time()
                                    except Exception:
                                        continue
                                    else:
                                        if r.status_code == 200:
                                            info = img_url, img, '下载完成', '耗时', time_end - time_start
                                            print(info)
                                            name = path + str(n) + '.gif'
                                            with open(name, 'wb') as gif:
                                                gif.write(r.content)
                                            with open(path + "log.txt", 'a') as log:
                                                new_content = str(info) + '\n' + name + '\n'
                                                log.write(new_content)
                                            print(name, '写入完成')
                                            n = n + 1
                                            print('当前线程数量', threading.active_count())
                                        else:
                                            print(img, '文件失效')
                                else:
                                    print(img, '未找到GIF')


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
    T = Task(549, 50)
    T.start()
