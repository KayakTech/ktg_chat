# Creating migration

```
$ alembic revision --autogenerate -m "message"
$ alembic upgrade head

# To downgrade
$ alembic downgrade -1
```
