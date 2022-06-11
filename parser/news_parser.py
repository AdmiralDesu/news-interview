from bs4 import BeautifulSoup


def parse_file():
    with open(
            file='./news.html',
            mode='r',
            encoding='utf-8'
    ) as news:

        contents = news.read()

        soup = BeautifulSoup(
            contents,
            'html.parser'
        )

        data = soup.find('div', {'class': 'news news_first-page'}).find_all()

        for item in data:
            try:
                item_string = str(item)
                # Ищем id новости
                if 'href' in item_string:
                    if 'style' in item_string:
                        cleaned_item_string = item_string[:item_string.find('style')]
                        news_id = cleaned_item_string[
                                  cleaned_item_string.find('?news=') + 6:
                                  cleaned_item_string.find('">')
                                  ]
                        print(f'ID новости{news_id=}')
                # Ищем заголовок новости
                title = item.find('div', {'class': 'news-card__caption'}).text
                print(f'Заголовок новости {title=}')
                # Ищем дату новости
                date = item.find('div', {'class': 'news-card__date'}).text
                print(f'Дата новости {date=}')
                image = item.find('div', {'class': 'news-card__image'})['style']
                cleaned_image = image[image.find("https"): image.find(")")]

                print(f'Изображение новости {cleaned_image=}')

                print('\n--------------------------------------------------------\n')

            except Exception as e:
                pass
