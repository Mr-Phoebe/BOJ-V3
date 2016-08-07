from django.db import models
import time
import json
import pika
from Problem.models import Problem
import Submission.models
import logging

logger = logging.getLogger('django')

# Create your models here.
class JudgeQueue(object):
    conn = None

    @classmethod
    def _getConn(cls):
        if cls.conn == None:
            cls.conn = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        elif cls.conn.is_closed:
            cls.conn = pika.BlockingConnection(pika.ConnectionParameters(
                host='localhost'))
        return cls.conn

    @classmethod
    def sendJudge(cls, _sid, _pid, _lang, _mode='contest', _code_path=''):

        s = {'sid':_sid, 'lang':_lang, 'pid':_pid,}
            
        # different modes diff---- General & Contest
        s['mode'] = _mode
        s['code_path'] = _code_path

        p = Problem.objects.get(pid = _pid)
        if p.is_spj == 0:
            s['spj'] = False
        else:
            s['spj'] = True
        s['block'] = True
        s['mem_lim'] = p.prob_memory
        s['time_lim'] = p.prob_time
        s['case_cnt'] = p.data_count
        s['case_lim'] = []
        for i in range(p.data_count):
            s['case_lim'].append({'time':p.prob_time, 'mem':p.prob_memory})

        sJson = json.dumps(s)

        conn = cls._getConn()
        chnl = conn.channel()
        chnl.queue_declare(queue='judge', durable=True)
        chnl.basic_publish(
                exchange='',
                routing_key='judge',
                body=sJson,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    )
                )
        chnl.close()

        print 'Submission has been sent to judge: %r' % (sJson,)


    @classmethod
    def getJudge(cls):
        print 'judge fetching start'
        conn = cls._getConn()
        chnl = conn.channel()
        chnl.queue_declare(queue='ret', durable=True)
        def callback(ch, method, properties, body):
            print " [x] result received %r" % (body,)
            #print json.loads(body, encoding)
            s = json.loads(body)
            #print s
            #time.sleep(1);
            #print 'sub#', s['sid']
            try:
                if s['mode'] == 'general':
                    Submission.models.GeneralSubmission.updateGeneralSubmission(s['sid'], s)
                else:
                    Submission.models.Submission.updateSubmission(s['sid'], s)
            except Exception as e:
                logger.error(str(e).replace("\n","\t"))
                print e
            ch.basic_ack(delivery_tag=method.delivery_tag)
        chnl.basic_qos(prefetch_count=1)
        chnl.basic_consume(
                callback,
                queue='ret',
                )
        chnl.start_consuming()

    @classmethod
    def release(cls):
        cls.conn.close()

