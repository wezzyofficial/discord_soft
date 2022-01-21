from engine.models.tasker import db, Account

db.create_tables([Account])

print('Готово!')