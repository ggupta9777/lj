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

def postProcess(actor, info):
    actor = re.sub("[\(\[].*?[\)\]]", "", actor)
    actor = actor.replace("'", '').replace(",", "")
    info = re.sub("[\(\[].*?[\)\]]", "", info)
    info = info.replace("\n", "")
    return actor, info

if __name__ == "__main__":

    # getActorNames()
    actor_names = open('actor_names.txt', 'r').read()
    actor_names = actor_names.split()

    actor_spouse = []
    tf = open("actor_spouse.txt", "w")
    for actor in actor_names:
        url = getUnfoldedURL(actor)
        if "starsunfolded" not in url:
            info = 'no match'
            rel = 'no match'
        else:
            if "http" not in url:
                url = "http://" + url
            req = urllib2.Request (url)
            response = urllib2.urlopen (req)
            html = response.read()
            if 'Religion</td><td class="column-2"' in html:
                rel = re.search(r'Religion</td><td class="column-2">(.*?)</td>', html, re.DOTALL).group()
                rel = BeautifulSoup(rel, "lxml").text[8:]
            else:
                rel = 'no match'
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
        actor, info = postProcess(actor, info)
        # print (actor, info, rel)
        # tf.write("%s \t ### \t %s \t ### \t %s\n" % (actor, info, rel))
    tf.close()