# Weather Remider

---

* DRF
* Postgres
* Celery | worker | beat
* UnitTest
* Doker
* NGINX


 ## Current features
<hr>

* Auto documentation drf_yasg
* auth
  * JWT token
  * CRUD
* weather
  * API OpenWeatherMap
  * add city
  * city subscription
  * periodicity send email
  * CRUD


# Instructions

---

Clone repository
<br>
`https://github.com/OleksiiMartseniuk/weather_remider.git`

#### Create file .env

```
export SECRET_KEY='set data'

export SECRET_KEY_OPEN_WEATHER_MAP='set data'

export POSTGRES_DB='set data'
export POSTGRES_USER='set data'
export POSTGRES_PASSWORD='set data'
export HOST_DB='weather_database'
export PORT_DB='5432'

export REDIS_CLOUD_URL='redis://weather_redis:6379/0'

export EMAIL_HOST='smtp.gmail.com'
export EMAIL_HOST_USER='set data'
export EMAIL_HOST_PASSWORD='set data'
export EMAIL_PORT='587'
export EMAIL_USE_TLS='True'

export DJANGO_SETTINGS_MODULE=config.settings
```
#### Docker

`docker-compose up --build`
<br>

#### Create superuser
`docker exec weather_web python manage.py createsuperuser`

#### Run test
`docker exec weather_web python manage.py test src/tests`
