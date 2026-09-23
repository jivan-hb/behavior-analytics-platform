from peewee import SqliteDatabase, Model, PrimaryKeyField, CharField, IntegerField

db = SqliteDatabase('data.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = PrimaryKeyField()
    name = CharField()
    surname = CharField()
    age = IntegerField()

if __name__ == '__main__':
    db.create_tables([User])





