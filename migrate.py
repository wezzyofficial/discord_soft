from engine.models.client import db, Chats, Accounts, Nicks, Proxys, Avatars

db.create_tables([Chats, Accounts, Nicks, Proxys, Avatars])

print('Готово!')