from peewee import *
from engine.functions.db import DSDatabases


dsb = DSDatabases(program_type='client')
db = dsb.init_db()


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class Chats(BaseModel):
    name = TextField(default='', null=True)
    link = TextField(default='', null=True)
    status = BooleanField(default=True)
    captcha = TextField(default='', null=True)
    reaction = TextField(default='', null=True)

    class Meta:
        db_table = 'chats'


class Accounts(BaseModel):
    login = TextField(default='', null=True)
    password = TextField(default='', null=True)
    token = TextField(default='', null=True)

    chat = ForeignKeyField(Chats, to_field="id")

    class Meta:
        db_table = 'accounts'


class Avatars(BaseModel):
    name = TextField(default='', null=True)
    hash = TextField(default='', null=True)

    chat = ForeignKeyField(Chats, to_field="id")

    class Meta:
        db_table = 'avatars'


class Nicks(BaseModel):
    name = TextField(default='', null=True)
    chat = ForeignKeyField(Chats, to_field="id")

    class Meta:
        db_table = 'nicks'


class Proxys(BaseModel):
    login = TextField(default='', null=True)
    password = TextField(default='', null=True)
    ip = TextField(default='', null=True)
    port = TextField(default='', null=True)

    p_type = TextField(default='', null=True)
    chat = ForeignKeyField(Chats, to_field="id")

    class Meta:
        db_table = 'proxys'