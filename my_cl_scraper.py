#!/usr/bin/python

"""
Written by: Eugene Brodsky
Last Update 6/25/2021
"""


import urllib
import datetime
from bs4 import BeautifulSoup
import time
import smtplib
import ssl
import json
import sys
try: from urllib.request import urlopen
except ImportError: from urllib2 import urlopen
import random
from configparser import ConfigParser
from threading import Thread, Event

class Scraper(Thread):

	CHECK_OLD_LISTINGS = True # If True, don't resend listings that have been reposted

	def __init__(self, stop_event, interrupt_event, recipient_emails, urls, owner_ip):
		self.stop_event = stop_event
		self.interrupt_event = interrupt_event
		Thread.__init__(self)

		config = ConfigParser()
		config.read('config.ini')
		self.smtp_server = config.get("CLscraper", "smtp_server").strip()
		self.smtp_username = config.get("CLscraper", "smtp_username").strip()
		self.smtp_password = config.get("CLscraper", "smtp_password").strip()
		self.fromaddr = config.get("CLscraper", "fromaddr").strip()
		self.toaddr = recipient_emails
		self.urls = urls
		self.timer = json.loads(config.get("CLscraper", "sleeptime").strip())
		self.owner = owner_ip

		self.gcontext = ssl.SSLContext()

	def run(self):
		if self.timer[1] < self.timer[0]:
			print("Timer interval, %s, isn't well formed. The second time cannot be smaller than the first.")
			exit(1)
		self.old_posts = []
		msg = "Hi, this is a Craigslist Scraper program that will send you emails listing any new posts matching a search url. This is an initialization email, here are the current posts.\n\n"
		self.Iterate(msg)
		endTime = time.time() + random.randint(60*self.timer[0],60*self.timer[1])

		while not self.stop_event.is_set():
			if time.time() < endTime:
				time.sleep(3)
				print("no new requests, sleeping 3 seconds")
				continue
			else:
				print("Here we go again! The time is " + str(datetime.datetime.now()) + "\n\n")
				self.Iterate(msg)
				endTime = time.time() + random.randint(60*self.timer[0],60*self.timer[1])
				if self.interrupt_event.is_set():
					self.interrupt_event.clear()
			

	def Get_Posts(self):
		new_posts = {}
		for link in self.urls:
			f = urlopen(link, context = self.gcontext)
			soup = BeautifulSoup(f,"html.parser")
			for listing in soup.find_all("li", {"class": "result-row"}):
				pid = listing.attrs["data-pid"]
				old_pid = pid
				url = listing.find("a", {"class": "result-title"}).attrs["href"]
				title = listing.find("a", {"class": "result-title"}).text
				if "data-repost-of" in listing.attrs.keys():
					old_pid = listing.attrs["data-repost-of"]
				if (pid not in self.old_posts) and (old_pid not in self.old_posts):
					new_posts[pid] = (url, title)
					self.old_posts.append(pid)
					self.old_posts.append(old_pid)
				elif (pid not in self.old_posts):
					self.old_posts.append(pid)
			return new_posts

	def Construct_Message(self, msg, new_posts):
		msg = "Subject: New Matches on CL Search \n\n"
		for pid in new_posts.keys():
			msg = msg + new_posts[pid][0] + " : " + new_posts[pid][1] + "\n"
		return msg

	def Iterate(self, msg):
		new_posts = self.Get_Posts()
		if new_posts:
			msg = self.Construct_Message(msg, new_posts)
			server = smtplib.SMTP(self.smtp_server)
			server.starttls()
			server.login(self.smtp_username, self.smtp_password)
			server.sendmail(self.fromaddr, self.toaddr, msg.encode('utf-8'))
			server.quit()
		else:
			print("No new posts.\n\n")
