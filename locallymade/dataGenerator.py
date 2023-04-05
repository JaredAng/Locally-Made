import sqlite3 as sql
import os,traceback, random

images = os.listdir("assets/items")
iname = []

def close_conn():
    try:
        sql_conn.close()
    except Exception as e:
        pass

def generate_data():
    usr = 0
    item = 0
    total=0
    qty=0
    for i in range (0,20):
        usr = random.randint(12, 17)
        item = random.randint(1, 16)
        qty=random.randint(1,5)
        try:
            sql_conn = sql.connect("db/shopdb.db")
            sql_cur = sql_conn.cursor()
            sql_cur.execute(f"select itemID,itemName,itemPrice,itemIMG from catalogTbl where itemID={item};")
            item = sql_cur.fetchone()
            sql_cur.execute(f"select uname from usrTbl where uid={usr};")
            total = item[2]*qty
            usr = sql_cur.fetchone()
            sq = f"insert into cartTbl (itemID, uname,itemName, itemPrice,itemQty,itemTotal,itemIMG) values ({item[0]},\"{usr[0]}\",\"{item[1]}\",{item[2]},{qty},{total},\'{item[3]}\')"
            print(sq)
            sql_cur.execute(sq)
            sql_conn.commit()
        except Exception as e:
            print(traceback.print_exc())
        sql_conn.close()

def createData():
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
    except Exception as e:
        pass
    for item in images:
        iname.append(os.path.splitext(item)[0])
        
    with open("assets/items/itemDesc.txt","r") as file:
        for item in file.readlines():
            item = item.split(':')
            item[2]=item[2].replace('\n','')
            sql_cur.execute(f"insert into catalogTbl (itemName,itemDesc,itemPrice,itemIMG) values (\"{item[0]}\",\"{item[1]}\",{item[2]},\"assets/items/{images[iname.index(item[0])]}\")")
            sql_conn.commit()
    close_conn()

def get_login(usr,pwd):
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
    except Exception as e:
        pass
    sql_cur.execute(f"select * from usrTbl where uname=\"{usr}\" and upwd = \"{pwd}\";")
    data = sql_cur.fetchall()
    close_conn()
    return data
       
def getCard_Catdata():
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
    except Exception as e:
        pass
    sql_cur.execute("select * from catalogTbl")
    data = sql_cur.fetchall()
    close_conn()
    return data

def getCard_Cartdata(usr):
    data = []
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
        sql_cur.execute(f"select * from cartTbl where uid=\"{usr}\"")
        data = sql_cur.fetchall()
    except Exception as e:
        pass
    finally:
        close_conn()
    return data

def getCard_Cartdata():
    data = []
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
        sql_cur.execute(f"select * from cartTbl")
        data = sql_cur.fetchall()
    except Exception as e:
        pass
    finally:
        close_conn()
    return data

def getCard_data(param:str):
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
        sql_cur.execute(param)
        data = sql_cur.fetchall()
    except Exception as e:
        pass
    finally:
        close_conn()
    return data

def insertData(table,column,data):
    try:
        sql_conn = sql.connect("db/shopdb.db")
        sql_cur = sql_conn.cursor()
    except Exception as e:
        pass
    string = f"insert into {table} ({column}) values ({data})"
    print(string)
    sql_cur.execute(string)
    sql_conn.commit()
    sql_conn.close()
    
