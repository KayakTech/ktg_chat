# Creating migration

```
$ alembic revision --autogenerate -m "message"
$ alembic upgrade head

# To downgrade
$ alembic downgrade -1


```

# RUN TEST

```
pytest -v app or pytest -v app/module
```
