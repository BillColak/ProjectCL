import re
import ssl
from lxml import etree, html
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup


ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

location_codes = {'Alberta ': '9003', 'All of Alberta ': '9003', 'Banff  Canmore ': '1700234', 'Calgary ': '1700199',
                  'Edmonton Area ': '1700202', 'All of Edmonton Area ': '1700202', 'Edmonton ': '1700203',
                  'St Albert ': '1700205', 'Strathcona County ': '1700204', 'Fort McMurray ': '1700232',
                  'Grande Prairie ': '1700233', 'Lethbridge ': '1700230', 'Lloydminster ': '1700095',
                  'Medicine Hat ': '1700231', 'Red Deer ': '1700136', 'British Columbia ': '9007',
                  'All of British Columbia ': '9007', 'Cariboo Area ': '1700296', 'All of Cariboo Area ': '1700296',
                  '100 Mile House ': '1700307', 'Quesnel ': '1700306', 'Williams Lake ': '1700305',
                  'Comox Valley Area ': '1700298', 'All of Comox Valley Area ': '1700298', 'Campbell River ': '1700316',
                  'Comox  Courtenay  Cumberland ': '1700315', 'Cowichan Valley  Duncan ': '1700300',
                  'Cranbrook ': '1700224', 'Fraser Valley ': '1700139', 'All of Fraser Valley ': '1700139',
                  'Abbotsford ': '1700140', 'Chilliwack ': '1700141', 'Hope  Kent ': '1700320', 'Mission ': '1700319',
                  'Greater Vancouver Area ': '80003', 'All of Greater Vancouver Area ': '80003',
                  'BurnabyNew Westminster ': '1700286', 'DeltaSurreyLangley ': '1700285',
                  'DowntownWest End ': '1700292', 'North Shore ': '1700289', 'Richmond ': '1700288',
                  'TricitiesPittMaple ': '1700290', 'UBC ': '1700291', 'Vancouver ': '1700287', 'Kamloops ': '1700227',
                  'Kelowna ': '1700228', 'All of Kelowna ': '1700228', 'Penticton ': '1700246', 'Nanaimo ': '1700263',
                  'Nelson ': '1700226', 'Peace River Area ': '1700295', 'All of Peace River Area ': '1700295',
                  'Dawson Creek ': '1700304', 'Fort St John ': '1700303', 'Port Alberni  Oceanside ': '1700299',
                  'All of Port Alberni  Oceanside ': '1700299', 'Parksville  Qualicum Beach ': '1700317',
                  'Port Alberni ': '1700318', 'Port Hardy  Port McNeill ': '1700301',
                  'Powell River District ': '1700294', 'Prince George ': '1700143', 'Revelstoke ': '1700302',
                  'SkeenaBulkley Area ': '1700297', 'All of SkeenaBulkley Area ': '1700297', 'Burns Lake ': '1700314',
                  'Houston ': '1700313', 'Kitimat ': '1700310', 'Prince Rupert ': '1700308', 'Smithers ': '1700311',
                  'Terrace ': '1700309', 'Vanderhoof ': '1700312', 'Sunshine Coast ': '1700293', 'Vernon ': '1700229',
                  'Victoria ': '1700173', 'Whistler ': '1700100', 'Manitoba ': '9006', 'All of Manitoba ': '9006',
                  'Brandon Area ': '1700085', 'All of Brandon Area ': '1700085', 'Brandon ': '1700086',
                  'Portage la Prairie ': '1700087', 'Flin Flon ': '1700236', 'Thompson ': '1700235',
                  'Winnipeg ': '1700192', 'New Brunswick ': '9005', 'All of New Brunswick ': '9005',
                  'Bathurst ': '1700260', 'Edmundston ': '1700261', 'Fredericton ': '1700018', 'Miramichi ': '1700262',
                  'Moncton ': '1700001', 'Saint John ': '80017', 'Newfoundland ': '9008',
                  'All of Newfoundland ': '9008', 'Corner Brook ': '1700254', 'Gander ': '1700255',
                  'Labrador ': '1700044', 'All of Labrador ': '1700044', 'Goose Bay ': '1700045',
                  'Labrador City ': '1700046', 'St Johns ': '1700113', 'Nova Scotia ': '9002',
                  'All of Nova Scotia ': '9002', 'Annapolis Valley ': '1700256', 'Bridgewater ': '1700257',
                  'Cape Breton ': '1700011', 'Halifax ': '80010', 'All of Halifax ': '80010', 'Bedford ': '1700107',
                  'City of Halifax ': '1700321', 'Cole Harbour ': '1700108', 'Dartmouth ': '1700109',
                  'New Glasgow ': '1700258', 'Truro ': '1700047', 'Yarmouth ': '1700259', 'Ontario A  L ': '9004',
                  'All of Ontario ': '100009004', 'Barrie ': '1700006', 'Belleville Area ': '1700129',
                  'All of Belleville Area ': '1700129', 'Belleville ': '1700130', 'Trenton ': '1700132',
                  'Brantford ': '1700206', 'Brockville ': '1700247', 'ChathamKent ': '1700239', 'Cornwall ': '1700133',
                  'Guelph ': '1700242', 'Hamilton ': '80014', 'Kapuskasing ': '1700237', 'Kenora ': '1700249',
                  'Kingston Area ': '1700181', 'All of Kingston Area ': '1700181', 'Kingston ': '1700183',
                  'Napanee ': '1700182', 'Kitchener Area ': '1700209', 'All of Kitchener Area ': '1700209',
                  'Cambridge ': '1700210', 'Kitchener  Waterloo ': '1700212', 'Stratford ': '1700213',
                  'Leamington ': '1700240', 'London ': '1700214', 'Ontario M  Z ': '100009004', 'Muskoka ': '1700078',
                  'Norfolk County ': '1700248', 'North Bay ': '1700243', 'Ottawa  Gatineau Area ': '1700184',
                  'All of Ottawa  Gatineau Area ': '1700184', 'Gatineau ': '1700186', 'Ottawa ': '1700185',
                  'Owen Sound ': '1700187', 'Peterborough Area ': '1700217', 'All of Peterborough Area ': '1700217',
                  'Kawartha Lakes ': '1700219', 'Peterborough ': '1700218', 'Renfrew County Area ': '1700074',
                  'All of Renfrew County Area ': '1700074', 'Pembroke ': '1700075', 'Petawawa ': '1700076',
                  'Renfrew ': '1700077', 'Sarnia Area ': '1700189', 'All of Sarnia Area ': '1700189',
                  'Grand Bend ': '1700190', 'Sarnia ': '1700191', 'Sault Ste Marie ': '1700244',
                  'St Catharines ': '80016', 'Sudbury ': '1700245', 'Thunder Bay ': '1700126', 'Timmins ': '1700238',
                  'Toronto GTA ': '1700272', 'All of Toronto GTA ': '1700272', 'City of Toronto ': '1700273',
                  'Markham  York Region ': '1700274', 'Mississauga  Peel Region ': '1700276',
                  'Oakville  Halton Region ': '1700277', 'Oshawa  Durham Region ': '1700275',
                  'Windsor Region ': '1700220', 'Woodstock ': '1700241', 'Prince Edward Island ': '1700118',
                  'All of Prince Edward Island ': '1700118', 'Charlottetown ': '1700119', 'Summerside ': '1700120',
                  'QuÃbec ': '9001', 'All of QuÃbec ': '9001', 'AbitibiTÃmiscamingue ': '1700059',
                  'All of AbitibiTÃmiscamingue ': '1700059', 'RouynNoranda ': '1700060', 'ValdOr ': '1700061',
                  'BaieComeau ': '1700251', 'CentreduQuÃbec ': '1700121', 'All of CentreduQuÃbec ': '1700121',
                  'Drummondville ': '1700122', 'Victoriaville ': '1700123', 'ChaudiÃreAppalaches ': '1700062',
                  'All of ChaudiÃreAppalaches ': '1700062', 'LÃvis ': '1700063', 'StGeorgesdeBeauce ': '1700065',
                  'Thetford Mines ': '1700064', 'Chibougamau  Northern QuÃbec ': '1700284', 'GaspÃ ': '1700066',
                  'Granby ': '1700253', 'Greater MontrÃal ': '80002', 'All of Greater MontrÃal ': '80002',
                  'City of MontrÃal ': '1700281', 'Laval  North Shore ': '1700278',
                  'Longueuil  South Shore ': '1700279', 'West Island ': '1700280', 'LanaudiÃre ': '1700283',
                  'Laurentides ': '1700282', 'Mauricie ': '1700147', 'All of Mauricie ': '1700147',
                  'Shawinigan ': '1700148', 'TroisRiviÃres ': '1700150', 'QuÃbec City ': '1700124',
                  'Rimouski  BasStLaurent ': '1700250', 'SaguenayLacSaintJean ': '1700178',
                  'All of SaguenayLacSaintJean ': '1700178', 'LacSaintJean ': '1700180', 'Saguenay ': '1700179',
                  'SaintHyacinthe ': '1700151', 'SaintJeansurRichelieu ': '1700252', 'SeptÃŽles ': '1700071',
                  'Sherbrooke ': '1700156', 'Saskatchewan ': '9009', 'All of Saskatchewan ': '9009',
                  'La Ronge ': '1700265', 'Meadow Lake ': '1700264', 'Nipawin ': '1700266', 'Prince Albert ': '1700088',
                  'Regina Area ': '1700194', 'All of Regina Area ': '1700194', 'Moose Jaw ': '1700195',
                  'Regina ': '1700196', 'Saskatoon ': '1700197', 'Swift Current ': '1700093', 'Territories ': '9010',
                  'All of Territories ': '9010', 'Northwest Territories ': '1700103',
                  'All of Northwest Territories ': '1700103', 'Yellowknife ': '1700104', 'Nunavut ': '1700105',
                  'All of Nunavut ': '1700105', 'Iqaluit ': '1700106', 'Yukon ': '1700101', 'All of Yukon ': '1700101',
                  'Whitehorse ': '1700102'}

# ur = open(r"C:\Users\Owner\PycharmProjects\ProjectCL\New_Tkinker_folder\Concept_Tests\textfiles\kijijilocations.html", encoding="utf8")
# ur = "https://vancouver.craigslist.org/bnc/cto/d/burnaby-benz-c63amg/6967710243.html"
ur = "https://www.kijiji.ca/b-cars-trucks/calgary/c174l1700199?for-sale-by=ownr"
ur_page = "https://www.kijiji.ca/b-cars-trucks/calgary/page-26/c174l1700199?for-sale-by=ownr"
# ur = "https://www.kijiji.ca/b-cars-trucks/saskatoon/c174l1700197?for-sale-by=ownr"
# https://www.kijiji.ca/b-calgary/honda-crv/k0l1700199

headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
url = urllib.request.Request(ur, headers=headers)
response = urllib.request.urlopen(url, context=ctx).read()
tree = html.fromstring(html=response)
soup = BeautifulSoup(response, "html.parser")

elements = tree.xpath("//*[@id='mainPageContent']/div[4]/div[3]/div/div[*]")
class_id = 'data-vip-url'

# Page Number Index
soupcount = soup.find("div", {"class": "showing"})
count = re.findall('(?<=of).*?(?=Ads)', str(soupcount))
page_num = str(count).replace(" ", "")
pagecount = re.sub(r'[^\w\s]', '', str(page_num))
piggy = int(int(pagecount)/20)
#
link_list = []
for i in range(1, piggy):
    links = "https://www.kijiji.ca/b-cars-trucks/calgary/page-" + str(i) + "/c174l1700199?for-sale-by=ownr"
    link_list.append(links)
#print(link_list)
#print(piggy)
#print(len(link_list))



# Find all the Hyperlink Extentions
mydivs = soup.findAll("a", {"class": "title"})
cool = []
for links in mydivs:
    ref = re.findall('href=([^ ]*?(?=>))', str(links))
    href = re.findall('(?<=").*?(?=")', str(ref))
    for i in href:
        cool.append(i)

car_list = []
base_url = "https://www.kijiji.ca"
for car in cool:
    cool_cars = base_url + car
    car_list.append(cool_cars)
#print(car_list)






#"(?<=title).*?(?=href)",
#l = []
#for li in elements:
#    text = [i for i in map(str.strip, li.xpath(".//text()")) if i]
#    print(text)
#    j = li.attrib[class_id]
#    l.append(j)
#print(l)

# lst = [d[class_id] for d in l if class_id in d]
#
# base_url = "https://www.kijiji.ca"
# for i in lst:
#    link = base_url + i
#    print(link)


# items = tree.xpath("//p")   # Fucking Amazing
# for li in items:
#    text = map(str.strip, li.xpath(".//text()"))
#    print(list(text))

# for li in items:
#    text = list(map(str.strip, li.xpath(".//text()")))
#    lst = clean_list = [i for i in text if i]
#    print(lst)

###################Location Codes#######################
# ur = open(r"C:\Users\Owner\PycharmProjects\ProjectCL\New_Tkinker_folder\Concept_Tests\textfiles\kloco.txt")
# namelist = []
# codelist = []
# for data in ur:
#    d = re.sub(r'[^\w\s]', '', str(data))
#    y = re.findall("(?<=title).*?(?=href)", str(d))
#    x = re.findall('#([^ ]*[0-9]+)', str(data))
#    dic = dict(zip(y, x))
#    print(dic)
#    for i, j in dic.items():
#        print(i + ':' + j)

