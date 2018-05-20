from urllib.request import urlopen

import datetime
import requests
#
#
# def get_out_ip():
#     url = r'http://1212.ip138.com/ic.asp'
#     r = requests.get(url)
#     txt = r.text
#     ip = txt[txt.find("[") + 1: txt.find("]")]
#     print('ip:' + ip)
#     return ip
#
#
# if __name__ == '__main__':
#     my_ip = urlopen('http://ip.42.pl/raw').read()
#     print('ip.42.pl', my_ip)
#     # get_out_ip()
#

import requests
import re
import time


def get_ip_by_ip138():
    response = requests.get("http://www.cip.cc/")
    content = response.content.decode(errors='ignore')
    # print(content)
    ip = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", content).group(0)
    return ip


if __name__ == '__main__':
    file = open('pi_digits.txt', 'a+')
    while True:
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ip = get_ip_by_ip138()
        data = nowTime + ' IP:' + ip + '\n'
        print(data)
        file.write(data)
        file.flush()
        time.sleep(10)
        # print("本机的ip地址为:", get_ip_by_ip138())
