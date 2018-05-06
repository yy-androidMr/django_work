import requests
from pyquery import PyQuery as pq

if __name__ == '__main__':
    r = requests.get('http://www.smdyy.cc/kan/81677.html')
    doc = pq(r.text)
    play_list = doc('.play-list')
    div_list = play_list('div').items()
    div_item1 = None
    for div in div_list:
        div_item1 = div
        break
    a_tag_list = div_item1('a').items()
    for a_tag in a_tag_list:
        print(a_tag.attr.href)
    # ttt = div_list.__str__()
    # tv_list = ttt.replace('</div>', '</div>SPILTE_STR').split('SPILTE_STR')
    #
    # tv_item = pq(tv_list[0])

    # print(tv_item)
