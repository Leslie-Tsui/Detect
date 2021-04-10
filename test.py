from DButil import MyDButil
db=MyDButil()
sql="select * from 模板1;"
flag=db.fetch_all(sql)
print(flag)