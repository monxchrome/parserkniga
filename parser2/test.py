# import requests
import re

# from bs4 import BeautifulSoup
#
# page_number = 1
# link = f'https://knigavuhe.org/new/?page='
#
# for page in range(3921):
#     response = requests.get(f'{link}{page_number}').text
#     soup = BeautifulSoup(response, 'lxml')
#     block = soup.find('div', id='books_updates_list')
#     links = [item['src'] for item in block.select('img')]
#
#     page_number += 1
#     print(links)

import requests
from bs4 import BeautifulSoup

page_letter = 1

link = f'http://loveread.ec/letter_author.php?let={page_letter}'

for page in range(27):
    response = requests.get(f'{link}').text
    soup = BeautifulSoup(response, 'lxml')
    # block = soup.find_all('a', class_='author_item_name')
    for block in soup.find_all('a', class_='letter_author'):

        print(block.get_text().encode('cp1251', 'ignore'))
    page_letter += 1
