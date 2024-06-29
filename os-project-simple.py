import os
import cloudscraper
import csv
import re
from bs4 import BeautifulSoup

url = 'https://unsplash.com'

scrapper = cloudscraper.create_scraper()
request = scrapper.get(url)

with open('sad.csv', 'wb') as b:
    b.write(request.content)

print(request)

# Read the file in binary mode
with open("sad.csv", 'rb') as f:
    content = f.read()

soup = BeautifulSoup(content, 'html.parser')

list_save = []
y_author = []

if re.findall(r'https://images.unsplash.com/photo-.+?;', soup.prettify()):
    list_save.extend(re.findall(r'https://images.unsplash.com/photo-.+?;', soup.prettify()))

if re.findall(r'https://plus.unsplash.com/premium_photo-.+?;', soup.prettify()):
    list_save.extend(re.findall(r'https://plus.unsplash.com/premium_photo-.+?;', soup.prettify()))

# Remove duplicates
list_save = list(set(list_save))

if re.findall(r'>.+?</a>', soup.prettify()):
    y_author.extend(re.findall(r'>.+?</a>', soup.prettify()))

# Ensure y_author has the same length as list_save
while len(y_author) < len(list_save):
    y_author.append("unknown")

# Make directories for each author and save their photos
for q in y_author:
    q_dir = q.strip('>< /a')
    os.makedirs(q_dir, exist_ok=True)
    with open(f"{q_dir}/photo_urls.txt", 'w', encoding='utf-8') as save5:
        for qq in list_save:
            save5.write(qq + '\n')

header = ['author', 'url']
flag = 1
for item1 in range(len(list_save)):
    data = [y_author[item1], list_save[item1]]
    with open('inform.csv', 'a', encoding='utf-8') as f5:
        writer = csv.writer(f5)
        if flag == 1:
            writer.writerow(header)
            flag += 1
        writer.writerow(data)
