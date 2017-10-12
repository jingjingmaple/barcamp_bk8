#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataset
import time
from time import gmtime, strftime, localtime
from http.server import BaseHTTPRequestHandler, HTTPServer
from var_dump import var_dump

ptime = strftime("%Y-%m-%d %H:%M:%S", localtime())
db = dataset.connect('sqlite:///tweet.db')
table = db['tweet']


class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

	# GET
	def do_GET(self):
		if self.path[:6] == "/tweet":
			if len((self.path).split('/')) == 3:
				start_id = (self.path).split('/')[2]
			else:
				start_id = 0
			self.send_response(200)
			self.send_header('Content-type','application/json; charset=utf-8')
			self.end_headers()
			
			if start_id == "":
				start_id = 0
			result = db.query('SELECT * FROM tweet WHERE id_str >'+str(start_id))
			py =0
			message = '{"tweet":['
			for row in result:
				kk = row['id_str']
				if py !=0:
					message += ','
				message += '{"id_str":"'+row['id_str']+'","text":"'+row['text']+'" , "username": "'+row['user']+',"user_pic":"'+row['profile']+'"}'
				py+=1
			message +=']}'
			self.wfile.write(bytes(message, "utf8"))
			return
		else:
			self.send_response(404)
			self.send_header('Content-type','application/json; charset=utf-8')
			self.end_headers()
			return
def run():
	print('starting server...')
	server_address = ('127.0.0.1', 8080)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()
run()
