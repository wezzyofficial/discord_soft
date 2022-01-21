from peewee import *
from engine.functions.db import DSDatabases


dsb = DSDatabases(program_type='tasker')
db = dsb.init_db()


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Account(BaseModel):
    """Таблицы базы данных "Account" - для примера."""
    name = TextField(default='', null=True)

    class Meta:
        db_table = 'accounts'