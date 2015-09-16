from mongoengine import *


class Company(Document):
    code = StringField(unique=True, required=True)
    stockName = StringField(required=True)
    name = StringField()
    e_name = StringField()
    found_time = DateTimeField()
    overview = StringField()
    business ＝ StringField()
    main_business = StringField()
    industry = StringField()

class Quote(Document):
    company = ReferenceField(Company)
    day = DateTimeField()
    open = DecimalField(precision=2)
    high = DecimalField(precision=2)
    low = DecimalField(precision=2)
    close = DecimalField(precision=2)
    volume = LongField()
    adj_close = DecimalField(precision=2)
