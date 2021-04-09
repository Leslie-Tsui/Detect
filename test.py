from DButil import MyDButil

db=MyDButil()
sql="create table 模板13(label_id varchar(255) not null,x0 varchar(255),y0 varchar(255),x1 varchar(255),y1 varchar(255),origin_data varchar(255));"
flag=db.update(sql)
print(flag)