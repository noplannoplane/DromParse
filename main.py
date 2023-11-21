import requests
from bs4 import BeautifulSoup
import json
import csv
import os

start_url = "https://auto.drom.ru/all/page1/?cid[]=23&cid[]=170&order=price&multiselect[]=9_4_15_all&multiselect[]=9_4_16_all&pts=2&damaged=2&unsold=1"

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}
start_req = requests.get(start_url, headers=headers)
start_src = start_req.text
start_response = requests.get(start_url)
start_soup = BeautifulSoup(start_response.text, 'html.parser')
pages = [start_url]
for pages_urls in start_soup.find_all('a', class_='css-14wh0pm e1lm3vns0'):
    pages.append(pages_urls['href'])

for i in range(2, 5):
    url = f"https://auto.drom.ru/all/page{i}/?cid[]=23&cid[]=170&order=price&multiselect[]=9_4_15_all&multiselect[]=9_4_16_all&pts=2&damaged=2&unsold=1"
    pages.append(url)

all_ads_dict = {}
for i, page in enumerate(pages):
    req = requests.get(page, headers=headers)
    src = req.text
    soup = BeautifulSoup(src, "lxml")
    all_ads_hrefs = soup.find_all(class_=("css-xb5nz8 e1huvdhj1"))
    if not all_ads_hrefs:
        continue
    for class_ in all_ads_hrefs:
        for span in class_.find_all('span'):
            span.append(' ')
        for div in class_.find_all('div'):
            div.append(' ')

    for item in all_ads_hrefs:
        item_text = item.text.replace(' ', '')
        item_href = "h" + item.get("href")[1:]
        all_ads_dict[item_text] = item_href

# записываем данные заголовков в json файл
with open('all_ads_headers.json', 'w', encoding='utf-8') as f:
    json.dump(all_ads_dict, f, ensure_ascii=False, indent=4)


# запись данных заголовков в CSV-файл
with open("all_ads_headers.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Название", "Год",  "Ссылка"])
    for item_text, item_href in all_ads_dict.items():
        writer.writerow([item_text, item_href])

# сбор данных с объявлений и сохранение их в файлы
for title, url in all_ads_dict.items():
    ad_req = requests.get(url, headers=headers)
    ad_src = ad_req.text
    ad_soup = BeautifulSoup(ad_src, 'html.parser')
    ad_number = url.split('/')[-2]
    ad_dir = f"{ad_number}"
    os.makedirs(ad_dir, exist_ok=True)
    ad_data = []
    ad_data.append(ad_number)
    ad_data.append(url)
    ad_data.append(ad_soup.find('h1', class_='css-1fj5rhv e1d9h2kx0').text.strip())
    ad_data.append(ad_soup.find('h1', class_='css-1fj5rhv e1d9h2kx0').text.strip().split()[1])
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').text.strip().replace('\xa0', ''))
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_next_sibling('span').text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_next_sibling('span').find_next_sibling('span').text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_next_sibling('span').find_next_sibling('span').find_next_sibling('span').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').text.strip().replace('\xa0', ''))
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').text.strip().replace('\xa0', ''))
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('div', class_='css-1s8w6zg e1d9h2kx3').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').find_next_sibling('div').text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[1].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[2].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[3].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[4].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[5].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[6].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[7].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[8].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[9].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[10].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[11].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[12].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[13].text.strip())
    ad_data.append(ad_soup.find('span', class_='css-1qxtz39 e1d9h2kx1').find_all('span')[14].text.strip())
