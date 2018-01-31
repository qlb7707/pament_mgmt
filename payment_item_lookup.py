#!/bin/python
import argparse
import os
from utils import *

select_field = "year,mon,day,cost,cost_name,seller "
concat = " and "
where = " where "
time_filter_b = "time >= %s "
time_filter_t = "time <= %s "
name_filter = "cost_name ='%s' "
pri_filter = "pri_type_tbl.description = '%s'"
sec_filter = "sec_type_tbl.description = '%s'"
period_filter = "period_tbl.description = '%s'"



SQL = "select " + select_field + "from payment join pri_type_tbl on pri_type = pri_type_tbl.value join sec_type_tbl on sec_type_tbl.value = sec_type join period_tbl on period_tbl.value=period" + where

if __name__ == "__main__":
	parser = argparse.ArgumentParser("manul to the script")
	parser.add_argument("-l","--tl",type=str,default='',help="time lower bound")
	parser.add_argument("-u","--tu",type=str,default='',help="time upper bound")
	parser.add_argument("-n","--name",type=str,default='',help="goods name")
	parser.add_argument("-p","--pri_type",type=str,default='',help="primary type description(name)")
	parser.add_argument("-s","--sec_type",type=str,default='',help="secondary type description(name)")
	parser.add_argument("-e","--period",type=str,default='',help="period description(name)")
	args = parser.parse_args()
	paras = ()
	is_first = True
	if args.tl:
		if not is_first:
			SQL = SQL + concat
		else:
			is_first = False
		SQL = SQL + time_filter_b
		paras = paras + (time_str_to_int(args.tl),)

	if args.tu:
		if not is_first:
			SQL = SQL + concat
		else:
			is_first = False
		SQL = SQL + time_filter_t
		paras = paras + (time_str_to_int(args.tu),)
	
	if args.name:
		if not is_first:
			SQL = SQL + concat
		else:
			is_first = False
		SQL = SQL + name_filter
		paras = paras + (args.name,)

	if args.pri_type:
		if not is_first:
			SQL = SQL + concat
		else:
			is_first = False
		SQL = SQL + pri_filter
		paras = paras + (args.pri_type,)

	if args.sec_type:
		if not is_first:
			SQL = SQL + concat
		else:
			is_first = False
		SQL = SQL + sec_filter
		paras = paras + (args.sec_type,)

	if args.period:
		if not is_first:
			SQL = SQL + concat
		else:
			is_first = False
		SQL = SQL + period_filter
		paras = paras + (args.period,)

	SQL_FINAL = SQL%paras
	#print SQL_FINAL
	sql_ret = os.popen('mysql -uroot -p123456 -h 127.0.0.1 payment_mgmt -e "%s";'%SQL_FINAL).read()
	print sql_ret
