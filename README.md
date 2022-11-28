# Weather Collector
### Описание
Собирает данные о погоде 50-ти крупнейших городов мира.
### Технологии
- [Python 3.9](https://docs.python.org/3.9/)
- [Docker 20.10.21](https://docs.docker.com/)
- [SQLAlchemy 1.4](https://docs.sqlalchemy.org/en/14/)
### Запуск коллектора
- В корневой директории проекта создать файл `.env` и установить свои значения по примеру из файла `.env.template`
```bash
WEATHER_API_URL='http://api.openweathermap.org/data/2.5/weather/'
WEATHER_API_KEY='weather-api-key'
RETRY_TIME=3600 # integer sec
POSTGRES_USER='postgres-user'
POSTGRES_PASSWORD='postgres-password'
POSTGRES_HOST='localhost'
POSTGRES_DB='postgres-db'
```
- Поднять `docker-compose`
```bash
$ sudo docker compose up -d --build
```