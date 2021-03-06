# Food Order API

## Getting started

To start project, run:

```
docker-compose up
```

The API will then be available at [http://0.0.0.0:8000](http://0.0.0.0:8000).


To run the tests, run:

```
docker-compose run app sh -c "python manage.py test"
```

To create an admin user, open shell inside the container and run:

```
python manage.py createsuperuser
```


### API List:
| Method     | URL                       | Description                                                                                                                  |
|------------|---------------------------|------------------------------------------------------------------------------------------------------------------------------|
| GET        | admin/                    | Admin Login                                                                                                                  |
| POST       | api/user/                 | Create User                                                                                                                  |
| POST       | api/auth/login/           | User Login                                                                                                                   |
| POST       | api/auth/logout/          | User Logout                                                                                                                  |
| GET/UPDATE | api/user/me/              | User Account View                                                                                                            |
| GET/POST   | api/restaurant/           | Create and retrieve restaurants                                                                                              |
| GET/POST   | api/restaurant/<id>       | Retrieve restaurant by id                                                                                                    |
| GET/POST   | api/restaurant/menu/      | Create and retrieve restaurant menus. Add serve_date or restaurant_id params to fetch menus of a specific date or restaurant |
| GET/POST   | api/restaurant/menu/<id>  | Retrieve restaurant menu by id                                                                                               |
| POST       | api/restaurant/vote/      | Create vote for menus                                                                                                        |
| GET        | api/restaurant/winner/    | Retrive winner restaurant                                                                                                    |
