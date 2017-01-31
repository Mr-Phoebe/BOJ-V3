#!/usr/bin/env python
import pika
import sys
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='judge', durable=True)

#message = ' '.join(sys.argv[1:]) or "Hello World!"
data = {
        'sid':1,
        'lang':'g++',
        'pid':15,
        'case_cnt':1,
        'spj':False,
        'block':True,
        'time_lim':1000,
        'mem_lim':4000,
        'case_lim':[
            {'time':1000, 'mem':4000},
            ],
        }
channel.basic_publish(exchange='',
        routing_key='judge',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode = 2,
            #content_type = application/json,
            )
        )
print " [x] Sent %r" % (json.dumps(data),)
channel.basic_publish(exchange='',
        routing_key='judge',
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode = 2,
            #content_type = application/json,
            )
        )
print " [x] Sent %r" % (json.dumps(data),)
connection.close()
