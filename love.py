import matplotlib.pyplot as plt
import numpy as np
import urllib2
import time
import sys
import re

male = []
female = []

main_url = 'https://en.wikipedia.org/wiki/List_of_Indian_film_actors'

req = urllib2.Request (main_url)
response = urllib2.urlopen (req)
html = response.read()
actor_list = re.findall(r'<li><a href="/wiki/(.*?)"', html)
actor_list = actor_list[:-30]
actor_url = ['https://en.wikipedia.org/wiki/' + str(s) for s in actor_list]

spouse_list = []
nspouse_list = []
count = 0
nSearches = 100
for url in actor_url:
    if count <nSearches:
        req = urllib2.Request (url)
        response = urllib2.urlopen (req)
        html = response.read()
        if "(<abbr title=\"married\">" in html:
            spouses = (html.split("(<abbr title=\"married\">"))
            nSpouses = len(spouses) - 1
            nspouse_list.append(nSpouses)
            print (actor_list[count], nSpouses)
            temp = " "
            for k in range(nSpouses):
                temp = temp + str(spouses[k])[-20:]
                spouse_list.append(temp)
        else:
                spouse_list.append("NA")
                nspouse_list.append(0)
        count = count + 1