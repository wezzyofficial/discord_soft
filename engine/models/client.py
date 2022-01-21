from peewee import *
from engine.functions.db import DSDatabases


dsb = DSDatabases(program_type='client')
db = dsb.init_db()


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'