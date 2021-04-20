#import sqlite3
import ssl
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error
import re

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# options = {1: {'activities': 'act', 'artists': 'ats', 'childcare': 'kid', 'classes': 'cls', 'events': 'eve',
#               'general': 'com', 'groups': 'grp', 'local_news': 'vnn', 'lost_found': 'laf', 'missed_connections': 'mis',
#               'musicians': 'muc', 'pets': 'pet', 'rideshare': 'rid', 'volunteers': 'vol'},
#           2: {'automotive': 'aos', 'beauty': 'bts', 'cell/mobile': 'cms', 'computer': 'cps', 'creative': 'crs',
#               'event': 'evs',
#               'farm+garden': 'fgs', 'financial': 'fns', 'household': 'hss', 'labor/move': 'lbs', 'legal': 'lgs',
#               'lessons': 'lss', 'marine': 'mas', 'pet': 'pas', 'real_estate': 'rts', 'skilled_trade': 'sks',
#               'sm_biz_ads': 'biz',
#               'travel/vac': 'trv', 'write/ed/tran': 'wet'},
#           3: {'antiques': 'ata', 'appliances': 'ppa', 'arts+crafts': 'ara', 'atv/utv/sno': 'sna', 'auto_parts': 'pta',
#               'aviation': 'ava', 'baby+kid': 'baa', 'barter': 'bar', 'beauty+hlth': 'haa', 'bike_parts': 'bip',
#               'bikes': 'bia', 'boat_parts': 'bpa',
#               'boats': 'boo', 'books': 'bka', 'business': 'bfa', 'cars+trucks': 'cta', 'cds/dvd/vhs': 'ema',
#               'cell_phones': 'moa', 'clothes+acc': 'cla',
#               'collectibles': 'cba', 'computer_parts': 'syp', 'computers': 'sya', 'electronics': 'ela',
#               'farm+garden': 'gra', 'free': 'zip', 'furniture': 'fua',
#               'garage_sale': 'gms', 'general': 'foa', 'heavy_equip': 'hva', 'household': 'hsa', 'jewelry': 'jwa',
#               'materials': 'maa', 'motorcycle_parts': 'mpa',
#               'motorcycles': 'mca', 'music_instr': 'msa', 'photo+video': 'pha', 'rvs+camp': 'rva', 'sporting': 'sga',
#               'tickets': 'tia', 'tools': 'tla', 'toys+games': 'taa',
#               'trailers': 'tra', 'video_gaming': 'vga', 'wanted': 'waa', 'wheels+tires': 'wta'}}

#conn = sqlite3.connect('craigslist.sqlite')
#cur = conn.cursor()
#cur.execute('''CREATE TABLE IF NOT EXISTS Webs (id INTEGER PRIMARY KEY, URL TEXT UNIQUE)''')
#
class Collector:
    def __init__(self, web_url):
        self.web_url = web_url
        self.headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
        self.resp = urllib.request.Request(self.web_url, headers=self.headers)
        self.html = urllib.request.urlopen(self.resp, context=ctx).read()

    def totalcount_factor(self):
        soup = BeautifulSoup(self.html, "html.parser")
        tg = soup.find("span", {"class": "totalcount"})
        if str(tg) == "None":
            print("tg is none")
            self.factor = 0
            return self.factor
        else:
            ti = re.findall("[0-9]+", str(tg))
            self.factor = int(ti[0]) / 120  # the reason for having self.factor is to print out the number of results
            return self.factor

    def collect(self):
        url_count = []
        number = int(self.factor)
        if self.factor == 0:
            pass
        else:
            for i in range(1, int(number) + 1):
                num_url = self.web_url + '?s=' + str(i * 120)
                url_count.append(num_url)

            url_count.insert(0, self.web_url)
            webs = []
            for address in url_count:
                headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
                resp = urllib.request.Request(address, headers=headers)
                html = urllib.request.urlopen(resp, context=ctx).read()
                soup = BeautifulSoup(html, "html.parser")
                tags = soup('a')
                for tag in tags:
                    href = tag.get('href', None)
                    if href is None: continue
                    if href.startswith('#'): continue
                    if href.startswith('/'): continue
                    if not href.endswith('html'): continue
                    if href not in webs:
                        webs.append(href)
                        #print(href)
                return webs
