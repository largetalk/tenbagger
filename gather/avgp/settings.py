#tushare_token = "adsfadfa"
tushare_token = "336156685e93e322618582d2f4f54c72ea024dfdd3be6e9b7763341c"

#db_url = 'sqlite:///:memory:'
db_url = 'mysql+mysqldb://avgp:avgp@localhost:3306/avgp?charset=utf8'
DB_ECHO = False
DB_ECHO_POOL = False

try:
    from localsettings import *
except:
    pass
