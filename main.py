import datetime
import os
import time

from flask import Flask, jsonify
from flask_restful import Resource, Api, abort
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from flask_sqlalchemy import SQLAlchemy
from schemas.news_schemas import \
    NewsRequestSchema, \
    NewsResponseSchema, \
    News
from sqlalchemy import func
from datetime import date
from redis import Redis
from rq import Queue
from rq_scheduler import Scheduler
from parser.mosday import MosDay
from typing import List


app = Flask(__name__)
api = Api(app)

app.config[
    'SQLALCHEMY_DATABASE_URI'
] = os.environ.get('news_sql')

db = SQLAlchemy(app)

app.config.update(
    {
        'APISPEC_SPEC': APISpec(
            title='news-interview',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI для доступа к swagger JSON
        'APISPEC_SWAGGER_UI_URL': '/docs/'  # URI для доступа к swagger GUI
    }
)
docs = FlaskApiSpec(app)


def add_news_to_db_threading():
    """
    Запускает парсер в бесконечном цикле для обработки сайта в Threading
    :return:
    """
    parser = MosDay()

    while True:
        news = parser.get_all_news()

        for headline in news:
            model = NewsModel(
                news_id=headline.id,
                news_title=headline.title,
                news_image=headline.cover,
                news_date=headline.publish_date
            )
            db.session.add(model)
            db.session.commit()
            print(f'Новость с id {headline.id} записана в базу')
        print('Обработка окончена')
        time.sleep(600)


def add_news_to_db():
    """
    Запускает парсер в бесконечном цикле для обработки сайта в Redis
    :return:
    """
    parser = MosDay()

    news = parser.get_all_news()

    for headline in news:
        model = NewsModel(
            news_id=headline.id,
            news_title=headline.title,
            news_image=headline.cover,
            news_date=headline.publish_date
        )
        db.session.add(model)
        db.session.commit()
        print(f'Новость с id {headline.id} записана в базу')
    print('Обработка окончена')



class NewsModel(db.Model):
    __tablename__ = 'news'
    news_id = db.Column(
        db.Integer,
        primary_key=True,
        unique=True
    )
    title = db.Column(
        db.Text,
        nullable=False
    )
    news_image = db.Column(
        db.Text,
        nullable=True
    )
    news_date = db.Column(
        db.Text,
        nullable=False
    )


class NewsAPI(MethodResource, Resource):
    @doc(
        description='GET method',
        tags=['News']
    )
    def get(
            self,
            days: int
    ) -> dict:
        """
        days - количество дней, за которые нужно получить новости
        Get method represents a GET API method
        """

        start_date = datetime.datetime.now() - datetime.timedelta(days=days)

        end_date = datetime.datetime.now() + datetime.timedelta(days=365+1)

        news: List[NewsModel] = NewsModel.query.filter(
            NewsModel.news_date.between(
                start_date,
                end_date
            )
        ).all()

        models = dict()

        if news:
            print(news)
            for index, headline in enumerate(news):
                models[str(index)] = {
                    'news_id': headline.news_id,
                    'titile': headline.title,
                    'news_date': headline.news_date,
                    'news_image': headline.news_image
                }
        else:
            abort(
                http_status_code=404,
                message=f'В этом промежутке нет новостей'
            )

        return models

    # Ненужный POST запрос
    # @doc(description='POST method', tags=['News'])
    # @use_kwargs(NewsRequestSchema, location='json')
    # @marshal_with(NewsResponseSchema)
    # def post(self):
    #     """
    #     Get method represents a GET API method
    #     """
    #     return {
    #         'message': 'PUT endpoint'
    #     }


api.add_resource(NewsAPI, '/test/<int:days>')
docs.register(NewsAPI)

if __name__ == '__main__':
    """
    Настройка RQ Scheduler
    Не работает в докере
    """

    # scheduler = Scheduler(
    #     connection=Redis(
    #         host='redis',
    #         port=6379
    #     )
    # )
    #
    # today = datetime.datetime.utcnow()
    #
    # scheduler.schedule(
    #     scheduled_time=datetime.datetime.utcnow(),
    #     func=add_news_to_db,
    #     interval=30,
    #     repeat=20
    # )
    # print(f'{today=}')

    """
    Если не докер, то 
    """
    #threading.Thread(target=add_news_to_db_threading).start()


    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )
