import urllib2
import re
import requests
from bs4 import BeautifulSoup
import sys

def getActorNames():
    main_url = 'https://en.wikipedia.org/wiki/List_of_Indian_film_actors'
    req = urllib2.Request (main_url)
    response = urllib2.urlopen (req)
    html = response.read()
    actor_list = re.findall(r'<li><a href="/wiki/(.*?)"', html)
    actor_list = actor_list[:-30]
    actor_names = [str(s) for s in actor_list]
    tf = open("actor_names.txt", "w")
    tf.write("%s" % actor_names)
    tf.close()

def getUnfoldedURL(actor):
    goog_search = "https://www.google.co.in/search?sclient=psy-ab&client=ubuntu&hs=k5b&channel=fs&biw=1366&bih=648&noj=1&q=" + actor + "+starsunfolded"
    r = requests.get(goog_search)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.find('cite').text


if __name__ == "__main__":

    actor_names = open('actor_names.txt', 'r').read()
    actor_names = actor_names.split()
    actor_spouse = []
    for actor in actor_names:
        url = getUnfoldedURL(actor)
        if "starsunfolded" not in url:
            info = ' no match'
        else:
            if "http" not in url:
                url = "http://" + url
            req = urllib2.Request (url)
            response = urllib2.urlopen (req)
            html = response.read()
            if 'Wife/Spouse</td><td class="column-2">' in html:
                html = html.split('Wife/Spouse</td>' ,1)[1] 
                try:
                    info = re.search(r'<td class="column-2">(.*?)</td>', html, re.DOTALL).group()
                    info = BeautifulSoup(info, "lxml").text
                except AttributeError:
                    info = 'no match'
            elif 'Wife</td><td class="column-2">' in html:
                html = html.split('Wife</td>' ,1)[1] 
                try:
                    info = re.search(r'<td class="column-2">(.*?)</td>', html, re.DOTALL).group()
                    info = BeautifulSoup(info, "lxml").text
                except AttributeError:
                    info = 'no match'
            elif 'Spouse</td><td class="column-2">' in html:
                html = html.split('Spouse</td>' ,1)[1] 
                try:
                    info = re.search(r'<td class="column-2">(.*?)</td>', html, re.DOTALL).group()
                    info = BeautifulSoup(info, "lxml").text
                except AttributeError:
                    info = 'no match'
            else:
                info = 'no match'
        actor_spouse.append(info)
        print (actor, actor_spouse)

# spouse_list = []
# nspouse_list = []
# count = 0
# nSearches = 100
# for url in actor_url:
#     # if count <nSearches:
#     req = urllib2.Request (url)
#     response = urllib2.urlopen (req)
#     html = response.read()
#     if "(<abbr title=\"married\">" in html:
#         spouses = (html.split("(<abbr title=\"married\">"))
#         nSpouses = len(spouses) - 1
#         nspouse_list.append(nSpouses)
#         print (actor_list[count], nSpouses)
#         temp = " "
#         for k in range(nSpouses):
#             temp = temp + str(spouses[k])[-20:]
#             spouse_list.append(temp)
#     else:
#             spouse_list.append("NA")
#             nspouse_list.append(0)
#     count = count + 1
# print (count)

#Algo 
#1. google search for <actor starsunfolded"
#2. go to the starsunfolded url
#3. return 0 if no url found, decide later
#3. search for spouse pattern
#4. remove info between html tags
#5. get the name and form the database
#6. religion of actor (can use starsunfolded)
#7. religion of wife (word matching)