#!/usr/bin/python3

import RPi.GPIO as GPIO
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.request import urlopen
import subprocess
import time
import secrets

SHUTDOWN_PIN = 3
LISTEN_PORT = 8888
WEBHOOK_PATH = 'shutdown'

def executeHAShutdown(args=None):
	urlopen(secrets.HAWebhookURL, b'')
	time.sleep(20)
	shutdown()

class shutdownWebhook(BaseHTTPRequestHandler):
	def do_POST(self):
		self.send_response(200)
		if (self.path == '/' + WEBHOOK_PATH):
			shutdown()

def shutdown(args=None):
	subprocess.call(['shutdown', '-h', 'now'], shell=False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SHUTDOWN_PIN, GPIO.FALLING, callback=executeHAShutdown)

httpd = HTTPServer(('',LISTEN_PORT), shutdownWebhook)
httpd.serve_forever()
