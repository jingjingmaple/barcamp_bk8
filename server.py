#!/usr/bin/env python
# -*- coding: utf-8 -*-
import dataset
import json
import time
from time import gmtime, strftime, localtime
from http.server import BaseHTTPRequestHandler, HTTPServer
from var_dump import var_dump

ptime = strftime("%Y-%m-%d %H:%M:%S", localtime())
db = dataset.connect('sqlite:///mydatabase.db')
table = db['tweet']
#table.insert(dict(name='Jane Doe', age=37, country='France', gender='female', time=ptime))


# HTTPRequestHandler class
class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):

	# GET
	def do_GET(self):
		if self.path[:6] == "/tweet":
			if len((self.path).split('/')) == 3:
				start_id = (self.path).split('/')[2]
			else:
				start_id = 0
			# Send response status code
			self.send_response(200)
			# Send headers
			self.send_header('Content-type','application/json; charset=utf-8')
			self.send_header('Access-Control-Allow-Origin','*')
			#self.send_header('Content-Type','text/html; charset=utf-8')
			self.end_headers()

			# Send message back to client
			print(start_id)
			
			if start_id == "":
				start_id = 0
			result = db.query('SELECT * FROM tweet WHERE id_str >'+str(start_id)+' ORDER by id_str DESC LIMIT 5')
			py =0
			last_tweet=0
			message = '{"tweet":['
			for row in result:
				kk = row['id_str']
				if py !=0:
					message += ','
				message += '{"id_str":"'+row['id_str']+'","text":'+json.dumps(row['text'])+' , "name": "'+row['username']+'", "username": "'+row['user']+'","user_pic":"'+row['profile']+'","created":"'+row['created']+'"}'
				py+=1
				last_tweet = row['id_str']
			message +='],"last_tweet":'+str(last_tweet)+'}'
		
			# Write content as utf-8 data
			self.wfile.write(bytes(message, "utf8"))
			return
		elif self.path[:7] == "/random":
			# Send response status code
			self.send_response(200)
			# Send headers
			self.send_header('Content-type','application/json; charset=utf-8')
			self.send_header('Access-Control-Allow-Origin','*')
			self.end_headers()

			# Send message back to client

			

			result = db.query('SELECT * FROM tweet ORDER by Random() LIMIT 1')
			py =0
			last_tweet=0
			message = '{"tweet":['
			for row in result:
				kk = row['id_str']
				if py !=0:
					message += ','
				message += '{"id_str":"'+row['id_str']+'","text":'+json.dumps(row['text'])+' , "name": "'+row['username']+'", "username": "'+row['user']+'","user_pic":"'+row['profile']+'","created":"'+row['created']+'"}'
				py+=1
				last_tweet = row['id_str']
			message +='],"last_tweet":'+str(last_tweet)+'}'
		
			# Write content as utf-8 data
			self.wfile.write(bytes(message, "utf8"))
			return
		else:
			self.send_response(404)
			self.send_header('Content-type','application/json; charset=utf-8')
			self.end_headers()
			return
def run():
	print('starting server...')
	
	# Server settings
	# Choose port 8080, for port 80, which is normally used for a http server, you need root access
	server_address = ('127.0.0.1', 8081)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()
run()
