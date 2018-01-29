time=`date -d ${1} +%s`

mysql -uroot -p123456 -h 127.0.0.1 payment_mgmt -e "select round(sum(cost),2) sum_`date -d @${time} +%Y_%m_%d` from payment where time = '${time}';"
mysql -uroot -p123456 -h 127.0.0.1 payment_mgmt -e "select cost,cost_name,seller,pr.description primary_type,s.description secondary_type,pe.description period from payment join pri_type_tbl pr on pr.value=pri_type join sec_type_tbl s on s.value = sec_type join period_tbl pe on pe.value = period where time = '${time}';"
