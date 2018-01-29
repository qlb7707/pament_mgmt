date=`date +%Y-%m-%d`
filename=${date}.record
success_folder=success
share_folder=/media/sf_payment_record/
program_folder=/home/qlb/payment_mgmt/
if [ ! -d ${program_folder} ]; then
	echo `date` ${program_folder} does not exist,exit
	exit -1
fi
cd ${program_folder}
if [ ! -d ${success_folder} ]; then
	mkdir -p ${success_folder}
fi

echo `date` sync file from share folder
mv ${share_folder}/*.record . 
echo `date` The file name today is ${filename}

if [ ! -f ${filename} ]; then
	echo `date` Can not find file ${filename}
	exit -1
fi
echo `date` starting recording file ${filename}
python payment_mgmt_recording.py --filename=${filename} --time=`date -d ${date} +%s`
ret=${?}
if [ ${ret} -eq  0 ]; then
	echo `date` Record success, rename file ${filename} to success fold
	mv ${filename} ${success_folder}
else
	echo `date` Record failed.
fi
