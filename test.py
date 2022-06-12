# import csv
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup
#
#
# response = requests.get('http://mosday.ru/news/tags.php?metro')
#
# soup = BeautifulSoup(
#     response.content,
#     'html.parser'
# )
#
#
# table = soup.find_all('table')[2]
#
# #print(table)
#
# news_tables = table.find_all('table', border=0)
# # 4, 5, 6
# # for index, table in enumerate(news_tables):
# #     print(index)
# #     print(table)
# #     print('\n\n')
#
#
# table_4 = news_tables[4]
#
# #print(table_4.find_all('table', border=0)[1])
#
# real_news = table_4.find_all('table', border=0)[1]
#
# print(real_news)
#
# images = real_news.find_all('img')
#
# print(images)
# images_src = list()
#
# for image in images:
#     print(image['src'])
#     images_src.append(image['src'])
#
#
# print(type(real_news))
#
#
# print(real_news.find_all('tr'))
#
# titles = list()
#
#
# for row in real_news.find_all('tr'):
#     try:
#         print(row.get_text())
#         titles.append(row.get_text())
#     except Exception as e:
#         print(e)
#
# print(len(titles))
# print(len(images_src))
#
# # df = pd.read_html('http://mosday.ru/news/tags.php?metro')
# #
# # # 8 и 9 фреймы
# #
# # news_block_1 = df[8]
# #
# # for item in df:
# #     print(f'{item=}')
# #
# # # print(news_block_1.get(1)[0])
# # #
# # # print(type(news_block_1.get(1)[0]))
# # #
# # # first_news = news_block_1.get(1)[0]
# # # print(first_news[-1])
# # #
# # # print(repr(first_news))
#
#
#
import sqlite3

con = sqlite3.connect('database.db')
