import time
import MySQLdb
import re
import argparse

INSERT_FORMAT = "insert into payment(cost,cost_name,seller,pri_type,sec_type,period,time) values(%f,'%s','%s',%u,%u,%u,%u)"
payment_items = []

def insert_record(cost,name,sel,pri,sec,period,time,db):
	SQL = INSERT_FORMAT % (cost,name,sel,pri,sec,period,time)
	try:
		cursor = db.cursor()
		cursor.execute(SQL);
		db.commit()
	except Exception,Why:
		print(Why)
		exit(-1)

def insert_payment_items_to_db(db):
	try:
		cursor = db.cursor()
		for item in payment_items:
			SQL = INSERT_FORMAT %(item[0],item[1],item[2],item[3],item[4],item[5],item[6])
			cursor.execute(SQL)
		db.commit()
	except Exception,Why:
		print(Why)
		exit(-1)
		
			
	
	
	
def read_items(file):
	items = []
	with open(file) as f:
		lines = f.readlines()
		for line in lines:
			items.append(re.split('\s+',line.strip('\n').strip(' ')))
	return items

if __name__=='__main__':
	parser = argparse.ArgumentParser("manul to the script")
	parser.add_argument('--filename',type=str,default=None)
	parser.add_argument('--time',type=int,default=0)
	args = parser.parse_args()
	name = args.filename
	db = MySQLdb.connect("127.0.0.1",'root','123456','payment_mgmt')
	db.cursor().execute('set names utf8')
	if args.time:
		ti = args.time
	else:
		ti = int(time.time())
	items = read_items(name)
	for item in items:
		print item
		co,cn,sel,pr,se,pe = item
		#insert_record(float(co),cn,sel,int(pr),int(se),int(pe),ti,db)
		payment_items.append((float(co),cn,sel,int(pr),int(se),int(pe),ti))
	insert_payment_items_to_db(db)
	db.close()

	
			
		
