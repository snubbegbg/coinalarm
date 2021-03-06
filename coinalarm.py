#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib2, json, smtplib, time, sys

def getPrice(coin):
	response = urllib2.urlopen("https://api.coinmarketcap.com/v1/ticker/"+coin+"/?convert=SEK")
	data = json.load(response)
	price = data[0]['price_usd'][0:-4]
	print "The price of "+coin+" is "+price+"$."
	return price

def sendMail(msg):
	server = smtplib.SMTP('smtp.gmail.com:587')
	server.starttls()
	server.login(username,password)
	server.sendmail(fromaddr, toaddrs, msg)
	server.quit()
	sys.exit("Mail has been sent, shuting down script.")

def checkAlarm(method):
	price = getPrice(coin)
	msg = "Subject: "+subject+"\n"
	if method == "falling":
		if int(price) < price_alarm:
			msg = msg+"The price of "+coin+" has fallen to "+price+"$ !!!"
			sendMail(msg)
	elif method == "rising":
		if int(price) > price_alarm:
			msg = msg+"The price of "+coin+" has risen to "+price+"$ !!!"
			sendMail(msg)
	time.sleep(sleep_timer)

# Settings.
fromaddr = 'from@gmail.com'
toaddrs  = 'to@gmail.com'
username = 'username'
password = 'password'
subject  = 'PRICE ALERT!!!'
sleep_timer = 3600 # Checks price every hour.

try:
	coin 		= sys.argv[1]
	price_alarm = int(sys.argv[2])
	method		= sys.argv[3]
except:
	sys.exit("Not enought arguments. Specify name of cryptocoin, the price in dollars that will trigger the alert, and method (rising/falling).\n\
example: coinalarm.py bitcoin 1500 rising")

while True:
	checkAlarm(method)
