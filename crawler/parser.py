import lxml.html

class TrendingParser(object):
    def __init__(self, html):
        self.content = lxml.html.fromstring(html)

    def parse(self):
        items = self.content.xpath('//li[@class="repo-list-item"]')
        res = []
        for item in items:
            name = item.xpath('h3[@class="repo-list-name"]/a')[0]
            res.append({
                "name": "".join([s.strip() for s in name.xpath('span/text()|./text()[last()]')]),
                "url": "https://github.com" + name.attrib['href'],
                "language": item.xpath('p[@class="repo-list-meta"]/text()')[0].strip().split('\n')[0],
            })
        return res
