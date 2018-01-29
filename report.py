#coding=utf-8
import MySQLdb
import argparse
import time as t
import calendar as ca
import myemail
import xlwt

TM_LOC = t.localtime()
MON_DAY = ca.monthrange(TM_LOC.tm_year,TM_LOC.tm_mon)[1]
TIME_FORWARD_WEEK = 86400 * 7
TIME_FORWARD_MONTH = 86400 * MON_DAY
TIME_FORWARD_YEAR = 86400 * (366 if ca.isleap(TM_LOC.tm_year) else  365) 

ITEM_FIELDS = "time,cost,cost_name,pr.description,se.description,pe.description"
FREQ_SELLER_FIELDS = "count(*) c,sum(cost),seller"
FREQ_GOODS_FIELDS = "count(*) c,sum(cost),cost_name"
HEADER = 144*'-'
DEFAULT_USER_ID = 1
COL_WIDTH = 256 * 20

##style of title
borders = xlwt.Borders()
borders.left = xlwt.Borders.MEDIUM
borders.right = xlwt.Borders.MEDIUM
borders.top = xlwt.Borders.MEDIUM
borders.bottom = xlwt.Borders.MEDIUM
pattern = xlwt.Pattern()
pattern.pattern = xlwt.Pattern.SOLID_PATTERN
pattern.pattern_fore_colour = 5
ali = xlwt.Alignment()
ali.horz = xlwt.Alignment().HORZ_CENTER
ali.vert = xlwt.Alignment().VERT_CENTER
font = xlwt.Font()
font.name = 'Times New Roman'
font.bold = True
font.italic = True
style = xlwt.XFStyle()
style.font = font
style.alignment = ali
style.pattern = pattern
style.borders = borders

##style of items
#borders1 = xlwt.Borders()
#borders1.left = xlwt.Borders.MEDIUM
#borders1.right = xlwt.Borders.MEDIUM
#borders1.top = xlwt.Borders.MEDIUM
#borders1.bottom = xlwt.Borders.MEDIUM
pattern1 = xlwt.Pattern()
pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
pattern1.pattern_fore_colour = 1
ali1 = xlwt.Alignment()
ali1.horz = xlwt.Alignment().HORZ_LEFT
ali1.vert = xlwt.Alignment().VERT_CENTER
#font1 = xlwt.Font()
#font1.name = 'Times New Roman'
#font1.bold = True
#font1.italic = True
style1 = xlwt.XFStyle()
#style1.font = font1
style1.alignment = ali1
style1.pattern = pattern1
#style.borders = borders1

def write_excel(book,title,fields,data):
    #book = xlwt.Workbook()            #创建excel对象
    sheet = book.add_sheet(title)  #添加一个表
    c = 0  #保存当前列
    for i in range(len(fields)):
	sheet.write(0,i,fields[i],style)
	sheet.col(i).width = COL_WIDTH
    c += 1
    for d in data: #取出data中的每一个元组存到表格的每一行
        for index in range(len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index],style1)
        c += 1
#    book.save(filename)

def myAlign(string,length=0):
	string = str(string)
	if length == 0:
		return string
	slen = len(string)
	ret = string
	if isinstance(string,str):
		placeholder = ' '
	else:
		plcaeholder = u'  '
	while slen < length:
		ret += placeholder
		slen += 1
	return ret

def get_week_sum(book,time,db):
	try:
		title = "Total cost"
		fields=["Total cost"]
		SQL_GET_WEEK_SUM = "select round(sum(cost),2) from payment where time > %d"%time
		cursor = db.cursor()
		cursor.execute(SQL_GET_WEEK_SUM)
		row = cursor.fetchall()
		write_excel(book,title,fields,row)
		if row[0][0]:
			week_sum = float(row[0][0])
		else:
			week_sum = 0
		week_sum_str = "Your total cost is %f\n"%week_sum
		print week_sum_str
	except Exception,Why:
		print(Why)
		exit(-1)

def to_time_str(timestamp):
	time_int = int(timestamp)
	time_local = t.localtime(time_int)
	dt = t.strftime('%Y-%m-%d',time_local)
	return dt

def sql_rows_to_time_str(rows,length,str_index):
	rows_ret = []
	for row in rows:
		row_tmp = ()
		for i in range(length):
			if i == str_index:
				row_tmp += (to_time_str(row[i]),)
			else:
				row_tmp += (row[i],)
		rows_ret.append(row_tmp)
	return rows_ret
			
	
def get_week_payment_items(book,time,user,db):
	try:
		SQL_GET_WEEK_SUM = ("select %s from payment join pri_type_tbl pr on pr.value=pri_type " 
					"join sec_type_tbl se on se.value=sec_type "
					"join period_tbl pe on pe.value=period " 
					"where user_id = %d and time > %d order by cost desc limit 50")%(ITEM_FIELDS,user,time)
		cursor = db.cursor()
		cursor.execute(SQL_GET_WEEK_SUM)
		rows = cursor.fetchall()
		rows_to_write = sql_rows_to_time_str(rows,6,0)
#		rows_to_write = []
		title = "Payment items"
		fields = ["DATE","COST","COST NAME","PRIMARY TYPE","SECONDARY TYPE","PERIOD"]
		write_excel(book,title,fields,rows_to_write)
		print_title = "%sWEEK PAYMENT%s"%(67*'#',67*'#')
		print_fields = "%-15s\t%-10s\t%-40s\t%-30s\t%-30s\t%-30s"%('DATE','COST','COST_NAME','PRIMATY TYPE','SECONDARY TYPE','PERIOD')
		header = print_title + '\n' + print_fields+ '\n'+ HEADER
		print header
		for row in rows:
			payment_item = "%-15s\t%-10s\t%-40s\t%-30s\t%-30s\t%-30s"%(to_time_str(row[0]),row[1],row[2],row[3],row[4],row[5])
			#rows_to_write.append((to_time_str(row[0]),row[1],row[2],row[3],row[4],row[5]))
			print(payment_item)
	except Exception,Why:
		print(Why)
		exit(-1)

##
##get most frequently pay sellers
##
def get_most_freq_seller(book, time, user, db):
	try:
		SQL_GET_FREQ_SELLER = "select %s from payment where user_id = %d and time > %d group by seller order by c desc limit 20"%(FREQ_SELLER_FIELDS,user,time)
		title = "MOST FREQUENTLY SELLERS"
		fields = ["FREQUENCY","COST","SELLER"]
		cursor = db.cursor()
		cursor.execute(SQL_GET_FREQ_SELLER)
		rows = cursor.fetchall()
		write_excel(book,title,fields,rows)
		print_title = "%sMOST FREQUENTLY SELLERS%s"%(60*'#',60*'#')
		print_fields = "%-30s%-30s%-50s"%('frequency','cost','seller')
		header = print_title + '\n' + print_fields + '\n' + HEADER
		print(header)
		for row in rows:
			item = "%-30s%-30s%-50s"%(row[0],row[1],row[2])
			print(item)
	except Exception,Why:
		print(Why)
		exit(-1)

##
##get most frequently goods
##
def get_most_freq_goods(f, time, user, db):
	try:
		SQL_GET_FREQ_SELLER = "select %s from payment where user_id = %d and time > %d group by cost_name order by c desc limit 20"%(FREQ_GOODS_FIELDS,user,time)
		title = "Most frequently goods"
		fields = ["FREQUENCY","COST","GOODS"]
		cursor = db.cursor()
		cursor.execute(SQL_GET_FREQ_SELLER)
		rows = cursor.fetchall()
		write_excel(book,title,fields,rows)
		print_title = "%sMOST FREQUENTLY GOODS%s"%(60*'#',60*'#')
		print_fields = "%-30s%-30s%-50s"%('FREQUENCY','COST','GOODS')
		header = print_title + '\n' + print_fields + '\n' + HEADER
		print(header)
		for row in rows:
			item = "%-30s%-30s%-50s"%(row[0],row[1],row[2])
			print(item)
	except Exception,Why:
		print(Why)
		exit(-1)


##
##get percentage of primary type of cost
##
def get_pri_percent(f, time, user, db):
	try:
		SQL_GET_PRI_PERCENT = "select round(a.sc * 100/b.tot,2),a.sc,a.de from (select sum(cost) sc,pr.description de from payment join pri_type_tbl pr on pr.value = pri_type where user_id = %d and time > %d group by pri_type order by sc desc) a,(select sum(cost) tot from payment where user_id = %d and time > %d) b"%(user,time,user,time)
		title = "Primary type percentage"
		fields = ["COST PERCENTAGE","COST","PRIMARY TYPE"]
		cursor = db.cursor()
		cursor.execute(SQL_GET_PRI_PERCENT)
		rows = cursor.fetchall()
		write_excel(book,title,fields,rows)
		print_title = "%sPRIMARY TYPE PERCENTAGE%s"%(60*'#',60*'#')
		print_fields = "%-20s%-20s%-40s"%('COST PERCENTAGE','COST','PRIMARY TYPE')
		header = print_title + '\n' + print_fields + '\n' + HEADER
		print(header)
		for row in rows:
			item = "%-20s%-20s%-40s"%(row[0],row[1],row[2])
			print(item)
		
	except Exception,Why:
		print(Why)
		exit(-1)
	
	
def do_weekly_report(report_file, time, user, db):
	get_week_sum(report_file,time,db)
	get_week_payment_items(report_file, time, args.user, db)
	get_most_freq_seller(report_file, time, args.user, db)
	get_most_freq_goods(report_file, time, args.user, db)
	get_pri_percent(report_file, time, args.user, db)

def do_monthly_report(report_file, time, user, db):
	get_week_sum(report_file,time,db)
	get_week_payment_items(report_file, time, args.user, db)
	get_most_freq_seller(report_file, time, args.user, db)
	get_most_freq_goods(report_file, time, args.user, db)
	get_pri_percent(report_file, time, args.user, db)

def do_yearly_report(report_file, time, user, db):
	get_week_sum(report_file,time,db)
	get_week_payment_items(report_file, time, args.user, db)
	get_most_freq_seller(report_file, time, args.user, db)
	get_most_freq_goods(report_file, time, args.user, db)
	get_pri_percent(report_file, time, args.user, db)

def do_totally_report(report_file, time, user, db):
	get_week_sum(report_file,time,db)
	get_week_payment_items(report_file, time, args.user, db)
	get_most_freq_seller(report_file, time, args.user, db)
	get_most_freq_goods(report_file, time, args.user, db)
	get_pri_percent(report_file, time, args.user, db)
		
	

if __name__=="__main__":
	parser = argparse.ArgumentParser("manual to the script")
	parser.add_argument("--time",type=int,default=0)
	parser.add_argument("--filename",type=str,default="latest.xls")
	parser.add_argument("--user",type=int,default=1)
	parser.add_argument("--mode",type=str,default="week")
	args = parser.parse_args()
	if args.mode == 'week':
		time = 	args.time - TIME_FORWARD_WEEK
		do_report = do_weekly_report
		head = 'Weekly payment report'
	elif args.mode == 'month':
		time = args.time - TIME_FORWARD_MONTH
		do_report = do_monthly_report
		head = 'Monthly payment report'
	elif args.mode == 'year':
		time = args.time - TIME_FORWARD_YEAR
		do_report = do_yearly_report
		head = 'Yearly payment report'
	else:
		time = 0
		do_report = do_totally_report
		head = 'Totally payment report'
		

	attach_name = args.filename.split('/')[-1]	
	book = xlwt.Workbook(encoding='utf-8')
	db = MySQLdb.connect("127.0.0.1",'root','123456','payment_mgmt')
	cursor = db.cursor()
	cursor.execute('set charset utf8')
	do_report(book, time, args.user,db)
	book.save(args.filename)
	myemail.email_send(head,attach=args.filename,name=attach_name)
	db.close()
	

