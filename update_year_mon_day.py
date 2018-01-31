from utils import *
import MySQLdb
DEFAULT_YEAR = 2018
DEFAULT_MON = 1
DEFAULT_DAY = 1

def get_items(db):
	SQL = "select id,time from payment where year = %d and mon = %d and day = %d;"%(DEFAULT_YEAR,DEFAULT_MON,DEFAULT_DAY)
	try:
		cursor = db.cursor()
		cursor.execute(SQL)
		rows = cursor.fetchall()
		items = rows
	except Exception,Why:
		print(Why)
		exit(-1)
	return items

def update_y_m_d(items,db):
	try:
		for item in items:
			y,m,d = parse_timestamp(item[1])
			SQL = "update payment set year=%d,mon=%d,day=%d where id=%d"%(y,m,d,item[0])
			cursor = db.cursor()
			cursor.execute(SQL)
		db.commit()
	except Exception,Why:
		print(Why)
		exit(-1)
	

if __name__ == '__main__':
	db = MySQLdb.connect("127.0.0.1","root","123456","payment_mgmt")	
	db.cursor().execute('set names utf8')
	items = get_items(db)
	update_y_m_d(items,db)
	db.close()
	

