date=`date +%Y-%m-%d`
day=`date +%w`
tomorrow_date=`date -d tomorrow +%d`
tomorrow_mon=`date -d tomorrow +%m`

cd /home/qlb/payment_mgmt/

#weekly report
if [ ${day} -eq 0 ]; then
	echo `date` ${date} is weekend, start doing weekly report
	python report.py --filename=weekly_report/${date}_weekly.xls --time=`date -d ${date} +%s` --mode=week
	if [ $? -eq 0 ]; then
		echo `date` weekly report finish
	else
		echo `date` weekly report failed
	fi
fi

#monthly report
if [ ${tomorrow_date} -eq 1 ]; then
	echo `date` ${date} is month end, start doing monthly report
	python report.py --filename=monthly_report/${date}_monthly.xls --time=`date -d ${date} +%s` --mode=month
	if [ $? -eq 0 ]; then
		echo `date` monthly report finish
	else
		echo `date` monthly report failed
	fi
fi
#yearly report
if [ ${tomorrow_date} -eq 1 -a ${tomorrow_mon} -eq 1 ]; then
	echo `date` ${date} is year end, start doing yearly report
	python report.py --filename=yearly_report/${date}_yearly.xls --time=`date -d ${date} +%s` --mode=year
	if [ $? -eq 0 ]; then
		echo `date` yearly report finish
	else
		echo `date` yearly report failed
	fi
fi





