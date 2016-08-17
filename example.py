#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import re
html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

#soup = BeautifulSoup(html_doc, 'html.parser')
soup = BeautifulSoup(html_doc, 'html5lib')
str = "08月14日 16:42"
pattern = re.compile(r'^(\d)')
print pattern.match(str)
#date = re.sub(r'^(\d{2})',"",str)

if __name__ == "__main__":
#    print(soup.prettify())
    print("----------------------------")
    print(soup.title)
    print("----------------------------")
    print(soup.title.string)
    for link in soup.find_all('a'):
        print(link.get('href'))
    print("----------------------------")
    tag = soup.a
    print(tag.name)