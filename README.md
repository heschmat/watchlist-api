# watchlist-api

## SETUP

- Dockerfile & docker-compose.yml
- requirements*.txt
Make sure Django, & drf are listed in requirements.txt

```sh
docker compose build --no-cache api
# Verify Django is actually installed
docker compose run --rm api python -c "import django; print(django.get_version())"

docker compose run --rm api django-admin startproject config .

```

now this won't work
```sh
docker compose run --rm api python manage.py runserver 0.0.0.0:8000

# verify:
curl -i http://localhost:8000/
##curl: (7) Failed to connect to localhost port 8000 after 0 ms: Couldn't connect to server

```

The Django server is running, but it's running inside the container only. The key issue is that `docker compose run` does NOT publish ports unless you explicitly tell it to.

```sh
docker ps
## in PORTS section you'd see: 8000/tcp

```

```sh
docker compose run --rm --service-ports api \
  python manage.py runserver 0.0.0.0:8000


docker ps
## PORTS => 0.0.0.0:8000->8000/tcp
```

Ideally, simply remove anything related to db in docker compose and have the command like so `command: python manage.py runserver 0.0.0.0:8000`

```sh
# now this should work:
docker compose up api
```


## core
setup `wait_for_db.py`


## users

```sh
docker compose run --rm api python manage.py makemigrations
```

Now let's test:
```sh
export PAYLOAD='{
  "email": "kat@hotmail.com",
  "password": "Berlin97"
}'

# create a user
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"

# to create a super user:
docker compose run --rm api python manage.py createsuperuser

# gives you refresh & access token:
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD"
```

verify if the users have been created:
```sh
docker exec -it pg18 psql -U user_dev -d db_dev

# or:
# this will requires password
docker compose run --rm db \
  psql -h db -U user_dev -d db_dev

```


```sh

curl http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer $ACC_TOKEN"

```


## API documentation

```sh
# config/settings.py ------------ #
# INSTALLED_APPS += ['drf_spectacular']

# next:
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    # add this 👇
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# confit/urls.py ---------------- #

# For API schema and documentation
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns += [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

```

## movies

```sh
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "kimi@hotmail.com",
    "password": "Berlin97"
  }'

# or simply:
ADMIN_TOKEN=$(curl -s -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "kimi@hotmail.com",
    "password": "Berlin97"
  }' | jq -r .access)

# you may need to run
sudo apt update
sudo apt install -y jq

# curl -X POST http://localhost:8000/api/movies/ \
#   -H "Authorization: Bearer $ADMIN_TOKEN" \
#   -H "Content-Type: application/json" \
#   -d '{
#     "title": "Interstellar",
#     "description": "Space and time",
#     "year": 2014
#   }'


curl http://localhost:8000/api/movies/


curl -L -o inception.jpg "https://i.ebayimg.com/images/g/LlUAAOSwm8VUwoRL/s-l1200.jpg"

HOST_="http://localhost:8000"

curl -X POST "$HOST_/api/movies/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -F "title=Inception" \
  -F "description=A mind-bending thriller about dreams within dreams." \
  -F "release_year=2010" \
  -F "poster=@inception.jpg"


# post a review
curl -X POST http://localhost:8000/api/movies/1/reviews/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "That docking scene is legendary."
  }'

# login with another user and post a review:
curl -X POST http://localhost:8000/api/movies/1/reviews/ \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 3,
    "text": "don'\''t get the hype"
  }'

# get the reviews for a movie
curl http://localhost:8000/api/movies/1/reviews/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# fav a movie
curl -X POST http://localhost:8000/api/movies/1/favorite/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"

# get your favorite movies
curl http://localhost:8000/api/movies/favorites/ \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```
