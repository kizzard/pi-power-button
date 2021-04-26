#!/usr/bin/env python

import RPi.GPIO as GPIO
import BaseHTTPServer
import SocketServer
import subprocess

SHUTDOWN_PIN = 3
LISTEN_PORT = 8888
WEBHOOK_PATH = 'shutdown'

class shutdownWebhook(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		if (self.path == '/' + WEBHOOK_PATH):
			shutdown()

def shutdown(args=None):
	subprocess.call(['shutdown', '-h', 'now'], shell=False)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.add_event_detect(SHUTDOWN_PIN, GPIO.FALLING, callback=shutdown)

httpd = BaseHTTPServer.HTTPServer(('',LISTEN_PORT), shutdownWebhook)
httpd.serve_forever()
