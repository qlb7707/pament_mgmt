date=`date +%Y-%m-%d`
#date=2018-01-30
python /home/qlb/payment_mgmt/myemail.py --header="Daily report ${date}" --content="`payment_lookup ${date}`"
