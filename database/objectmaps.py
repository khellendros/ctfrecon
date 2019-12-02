# Object Document Mappings for MongoDB
import datetime as dt 
from mongoengine import *

class WordList(Document):
    name = StringField(required=True, unique=True)
    lists = ListField(StringField())
    modifytime = DateTimeField(default=dt.datetime.utcnow())

class Tool(Document):
    alias = StringField(required=True, unique=True)
    command = StringField(required=True, unique=True)

class ToolChain(Document):
    name = StringField(required=True, unique=True)
    tools = ListField(ReferenceField(Tool))

class ToolOutput(EmbeddedDocument):
    command = StringField() 
    output = StringField()
    modifytime = DateTimeField(default=dt.datetime.utcnow())

class Note(EmbeddedDocument):
    name = StringField(unique=True)
    content = StringField()
    modifytime = DateTimeField(default=dt.datetime.utcnow())

class FOI(EmbeddedDocument):
    name = StringField(unique=True)
    content = StringField()
    modifytime = DateTimeField(default=dt.datetime.utcnow())

class Enumeration(Document):
    project = StringField(required=True)
    domain = URLField(required=True, unique=True)
    ipaddress = StringField()
    notes = ListField(EmbeddedDocumentField(Note))
    toolenum = ListField(EmbeddedDocumentField(ToolOutput))
    FOIs = ListField(EmbeddedDocumentField(FOI))
