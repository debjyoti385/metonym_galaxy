# coding=utf8


from CURD import Database, Model, Field, PrimaryKey
from populate_dictionary import app


# class Message(Model):
#     title = Field()
#     content = Field()
#     create_at = Field()


class Nodes(Model):
    word = Field()
    meaning = Field()
    sentence = Field()
    x = Field()
    y = Field()
    z = Field()



Database.config(**app.config['DB_CONN_CFG'])
