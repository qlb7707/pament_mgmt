#coding=utf-8
import argparse
import sys
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

msg_from='770759450@qq.com'                                 #发送方邮箱
#msg_from='18051220245@163.com'                                 #发送方邮箱
passwd='xeizvcblorvgbffc'                                   #填入发送方邮箱的授权码

#passwd='aw18051220245'                                   #填入发送方邮箱的授权码
#msg_to='lbqin@Hillstonenet.com'                                  #收件人邮箱
msg_to=['qin_libin@foxmail.com']                                  #收件人邮箱
SMTP_SERVER = 'smtp.qq.com'
SMTP_PORT = 465
                    
#subject="test multi"                                     #主题     
#content="python 测试程序"
#text = MIMEText(content)
#msg = MIMEMultipart()
#msg['Subject'] = subject
#msg['From'] = msg_from
#msg['To'] = ','.join(msg_to)
#msg.attach(text)
#
#txtpart = MIMEApplication(open('help.txt').read())
#txtpart.add_header('Content-Disposition','attachment',filename='help.txt')
#msg.attach(txtpart)
#try:
#    s = smtplib.SMTP_SSL("smtp.163.com",465)
#    s.login(msg_from, passwd)
#    s.sendmail(msg_from, msg_to, msg.as_string())
#    print "发送成功"
#except s.SMTPException,e:
#    print "发送失败"
#finally:
#    s.quit()
#

def email_send(sub,con = 'None',attach='',name='attach'):
	subject = sub
	text = MIMEText(con.encode('utf8'))
	msg = MIMEMultipart()
	msg ['Subject'] =  subject
	msg['From'] = msg_from
	msg['To'] = ','.join(msg_to)
	msg.attach(text)
	if attach:
		att = MIMEApplication(open(attach).read())
		att.add_header('Content-Disposition','attachment',filename=name)
		msg.attach(att)
	s = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT)
	s.login(msg_from,passwd)
	s.sendmail(msg_from,msg_to,msg.as_string())
    	print "发送成功"
	s.quit()
	
	
if __name__ == '__main__':
	parser = argparse.ArgumentParser("manual to the script")
	parser.add_argument("--header",type=str,default='empty header')
	parser.add_argument("--content",type=str,default="empty content")
	args = parser.parse_args()
	email_send(args.header,args.content)	

