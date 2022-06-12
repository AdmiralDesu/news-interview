FROM python:3.9-slim


COPY . /app




WORKDIR /app

ENV news_sql=sqlite:///database.db

RUN apt-get update && apt-get upgrade -y

RUN pip install -r requirements.txt


ENTRYPOINT ["python"]
CMD ["main.py"]


