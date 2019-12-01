# Object Mappings for MongoDB
from mongoengine import *

class WordList(Document):
    name = StringField(unique=True)
    list = StringField()

class Tool(Document):
    name = StringField(unique=True)
    path = StringField(unique=True)

class ToolChain(Document):
    name = StringField(unique=True)
    tools = ListField(EmbeddedDocumentField(Tool))

class ToolOutput(EmbeddedDocument):
    owner = ReferenceField(Tool)
    output = StringField()

class Note(EmbeddedDocument):
    name = StringField(unique=True)
    content = StringField()

class FOI(EmbeddedDocument):
    name = StringField(unique=True)
    content = StringField()

class Enumeration(Document):
    domain = URLField(required=True, unique=True)
    ipaddress = StringField()
    notes = ListField(EmbeddedDocumentField(Note))
    toolenum = ListField(EmbeddedDocumentField(ToolOutput))
    FOIs = ListField(EmbeddedDocumentField(FOI))
