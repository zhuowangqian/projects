import pymysql
import pandas as pd
from sqlalchemy import create_engine, text

db = pymysql.connect(
    user='root',
    password='Qian1314',
    database='test'
)
cursor = db.cursor()
sql_insert = 'insert into baidu_translate2(' \
             'a,b,c,d,e,f' \
             ') values (' \
             '%s,%s,%s,%s,%s,%s' \
             ');'
sql_create_table = '''
                create table 品类分析2(
                   category_leaf_name text,
                   category_level1_name text,
                   category_level2_name text,
                   category_level3_name text,
                   category_level4_name text,
                   category_level5_name text,
                   ord_num text,
                   byr_num text,
                   sel_num text,
                   gmv text, 
                   post_fee text,
                   coupon_fee text
                   )DEFAULT CHARSET=utf8;'''
# 用于sql
'''   
create table 品类分析2(
                   category_leaf_name text,
                   category_level1_name text,
                   category_level2_name text,
                   category_level3_name text,
                   category_level4_name text,
                   category_level5_name text,
                   ord_num text,
                   byr_num text,
                   sel_num text,
                   gmv text, 
                   post_fee text,
                   coupon_fee text
                   )DEFAULT CHARSET=utf8;
'''
sql_delete = 'truncate table baidu_translate2;'
cursor.execute(sql_delete)

# 读取excel
# a, b, c, d, e, f = '1', '2', '3', '4', '5', '6'
# cursor.execute(sql_insert, (a, b, c, d, e, f))
# db.commit()
# df = pd.read_excel(r'C:\Users\Administrator\Desktop\aliexpress\品类分析.xlsx', sheet_name='选品（大类）')
# columns = df.columns
# print(columns)
# print(df.index)

# 读取mysql
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'Qian1314'
MYSQL_DB = 'test'
engine = create_engine('mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8'
                       % (MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_PORT, MYSQL_DB))
conn = engine.connect()

sql = text('SELECT * FROM baidu_translate2')

df2 = pd.read_sql(sql, conn)
# pd.set_option('display.unicode.ambiguous_as_wide', True)
# pd.set_option('display.unicode.east_asian_width', True)
# print(df2.columns)
df2 = df2.to_dict()
print(df2)
# for column in df2.columns:
#     # print(df2[column])
#     data = df2[column].values
#     for i in data:
#         print(column, i)

# 返回列表数据
sql_query = 'select * from 品类分析1;'
cursor.execute(sql_query)
result = cursor.fetchall()
# print(result)
