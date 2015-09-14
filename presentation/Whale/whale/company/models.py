from mongoengine import *


class Company(Document):
    code = StringField(unique=True, required=True)
    name = StringField(required=True)
    overview = StringField()
    found_time = DateTimeField()


class Quote(Document):
    company = ReferenceField(Company)
    day = DateTimeField()
    open = DecimalField(precision=2)
    high = DecimalField(precision=2)
    low = DecimalField(precision=2)
    close = DecimalField(precision=2)
    volume = LongField()
    adj_close = DecimalField(precision=2)
