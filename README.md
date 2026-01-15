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

