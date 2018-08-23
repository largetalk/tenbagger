#--coding:utf8--
from BeautifulSoup import BeautifulSoup
import urllib2

start_url = 'http://bbs.tianya.cn/post-stocks-1062591-%s.shtml'
saved_file = "content.txt"

def spider(url, f):
    r = urllib2.urlopen(url)

    h = r.read()
    txt = extract(h)

    f.write(txt.encode('utf8'))
    f.write('\r\n=============================\r\n')
    return fetch_next_url(h)



def extract(html):
    soup = BeautifulSoup(html)
    txt = []
    blocks = soup.findAll(name = "div",
                          attrs = {'class': 'atl-item'})

    for block in blocks:
        arthur = block.find("a", attrs={"class": "js-vip-check"}).text
        content = block.find(name = "div",
                            attrs = {'class' : "bbs-content"}).text
        txt.append('%s :\r\n%s' % (arthur, content))
    return '\r\n--------------------\r\n'.join(txt)


def fetch_next_url(html):
    return None


def main():
    with open(saved_file, 'w+') as f:
        for i in range(1, 88):
            spider(start_url % i, f)


if __name__ == '__main__':
    main()
