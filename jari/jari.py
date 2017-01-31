#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pika
import json
from conf import JudgeConf as jcnf
from compile import Compile
from sub import Sub
from judge import Judge

def daemon():
    def callback(ch, method, properties, body):
        print " [x] Received judge request %r" % (body,) # for debug
        s = Sub()
        try:
            s.getSub(body)
            c = Compile()
            c.compile(s)
        except Exception, e:
            print 'compile err| ', Exception, ':', e # for debug

        if s.status == jcnf.SUB_STATUS['judging']:
            try:
                j = Judge()
                j.judge(s)
            except Exception, e:
                print 'judge err| ', Exception, ':', e # for debug
        elif s.status != jcnf.SUB_STATUS['compilation error']:
            print 'compile done but unknown status=', s.status # for debug
        
        try:
            retStr = s.retSub()
            print retStr
        except Exception, e:
            with open('/home/buptacm/ce.log') as f:
                print >> f, 'Exception: ', e

        chnlOut.basic_publish(
                exchange='',
                routing_key='ret',
                body=retStr,
                properties=pika.BasicProperties(delivery_mode = 2,)
                )
        print " [x] Done judge result %r" % (retStr,) # for debug
        ch.basic_ack(delivery_tag=method.delivery_tag)

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=jcnf.QUEUE_HOST))
        chnlIn = connection.channel()
        chnlOut = connection.channel()

        chnlIn.queue_declare(queue=jcnf.QUEUE_NAME, durable=True)
        chnlOut.queue_declare(queue='ret', durable=True)
        print ' [*] Waiting for submissions. To exit press CTRL+C' # for debug


        chnlIn.basic_qos(prefetch_count=1)
        chnlIn.basic_consume(callback, queue=jcnf.QUEUE_NAME,)

        chnlIn.start_consuming()
    except KeyboardInterrupt:
        print 'jari deamon exit'
        connection.close()

if __name__ == '__main__':
    daemon()

