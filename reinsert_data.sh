date=${1}
echo start delete data of ${date}
mysql -uroot -p123456 -h 127.0.0.1 payment_mgmt -e "delete from payment where time=`date -d ${date} +%s`;"

if [ $? -eq 0 ]; then
    echo OK
    echo start reinsert data of ${date}
    python payment_mgmt_recording.py --filename=${date}.record --time=`date -d ${date} +%s`
    if [ $? -eq 0 ]; then
        echo OK
	mv ${date}.record success
    else
        echo reinsert data failed!!!
    fi
else
    echo delete data failed!!!
fi



