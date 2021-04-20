import re
import ssl
import time
import sqlite3
import pandas as pd
from bs4 import BeautifulSoup
import urllib.request, urllib.parse, urllib.error

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('CListest.sqlite')
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Pages
(post_id INTEGER PRIMARY KEY, 'url' TEXT UNIQUE , 'vin' TEXT, 'condition' TEXT, 'cylinders' TEXT, 'drive' TEXT, 'fuel' TEXT,
'odometer' TEXT, 'paint_color' TEXT, 'car_size' TEXT,'title_status' TEXT, 'transmission' TEXT, 'car_type' TEXT, 'post_time' TEXT,
'model' TEXT, 'price' TEXT, 'map_address' TEXT, 'map_link' TEXT, 'model_year' TEXT )''')

# TODO: Optimize code with Dataframes
# TODO: Images, description text, number extraction from items

class Dictator:
    def __init__(self, web_list):
        self.web_list = web_list

        empty_dict = dict.fromkeys(
            ['url', 'vin', 'condition', 'cylinders', 'drive', 'fuel', 'odometer', 'paint_color', 'car_size', 'title_status'
                , 'transmission', 'car_type', 'post_time', 'model', 'price', 'map_address', 'map_link', 'model_year'])

        count = 0
        for url in self.web_list:
            time.sleep(0.0001)

            # REQUESTS
            headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
            resp = urllib.request.Request(url, headers=headers)
            html = urllib.request.urlopen(resp, context=ctx).read()

            # BS PARSER
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.findAll("p", {"class": "attrgroup"})

            # Attribute tags
            tagging = re.findall("(?<=>).*?(?<=<)", str(tags))
            tagger = (re.sub(r'[^\w\s]', '', str(tagging))).split("  ")
            bella = [x.strip() for x in tagger if x.strip()]
            hadid = bella[1:]
            initial_attribute_dictionary = dict(zip(hadid[::2], hadid[1::2]))

            #      TIME OF THE POST
            time_tag = soup.findAll("time", {"class": "date timeago"})
            timet = str(time_tag).split(" ")
            tday = (timet[3]).split('"')
            tdot = tday[1].split("T")
            post = tdot[0] + ' ' + tdot[1][0:8]

            # TITLE / MODEL OF THE POST
            mod = soup.findAll("span", {"id": "titletextonly"})
            model_tag = re.findall("(?<=>).*?(?=<)", str(mod))
            model_name = re.sub(r'[^\w\s]', '', str(model_tag))

            # PRICE
            prices = soup.findAll("span", {"class": "price"})
            price_tag = re.findall("[0-9]+", str(prices))
            price_amount = re.sub(r'[^\w\s]', '', str(price_tag))
            if price_amount == " ": price_amount = None

            # LOCION HYPERLINK
            try:
                maplink = str(soup.find("p", {"class", "mapaddress"})).split('"')[3]
                initial_attribute_dictionary["map_link"] = str(maplink)
            except:
                pass

            mapaddress = soup.find("small")
            mpa = re.findall("(?<=>).*?(?=<)", str(mapaddress))
            smap = re.sub(r'[^\w\s]', '', str(mpa))
            if smap == 'google map': smap = None


            initial_attribute_dictionary["post_time"] = post
            initial_attribute_dictionary["model"] = model_name
            initial_attribute_dictionary["price"] = price_amount
            initial_attribute_dictionary["map_address"] = smap
            empty_dict.update(initial_attribute_dictionary)

            vin = empty_dict.get('vin')
            condition = empty_dict.get('condition')
            cylinders = empty_dict.get('cylinders')
            drive = empty_dict.get('drive')
            fuel = empty_dict.get('fuel')
            odometer = empty_dict.get('odometer')
            paint_color = empty_dict.get('paint color')
            car_size = empty_dict.get('car_size')
            title_status = empty_dict.get('title status')
            transmission = empty_dict.get('transmission')
            car_type = empty_dict.get('car_type')
            post_time = empty_dict.get('post_time')
            model = empty_dict.get('model')
            price = empty_dict.get('price')
            map_address = empty_dict.get('map_address')
            map_link = empty_dict.get('map_link')

            query = 'INSERT OR IGNORE INTO Pages (url, vin, condition, cylinders, drive, fuel, odometer, paint_color, car_size, ' \
                    'title_status, transmission, car_type, post_time, model, price, map_address, map_link) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'
            cur.execute(query,
                        (url, vin, condition, cylinders, drive, fuel, odometer, paint_color, car_size, title_status,
                         transmission,
                         car_type, post_time, model, price, map_address, map_link,))
            # TODO Use pandas to optimize all these commits
            count = count + 1
            print(count)
            if count == 50:
                conn.commit()

            conn.commit()
        #cur.close()
