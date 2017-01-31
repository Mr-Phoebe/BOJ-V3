# -*- coding: utf-8 -*-
import json
from conf import JudgeConf as jcnf

class Sub(object):

    def __init__(self):
        self.sid = 0
        self.lang = '' 
        self.pid = 0
        self.case_cnt = 0  #totol number of cases
        self.case_done = 0  #number of cases judged
        self.spj = False
        self.block = True  #when true, judge will terminate after the first no ac, otherwise it will
        self.status = 0  #0: init, 1: done, 2: compiling, 3: compilation error, 4: judging
        self.ce = ''
        self.time_lim = 0  #total time limit
        self.time = 0  #total time usage
        self.mem_lim = 0  #total memory limit
        self.mem = 0  #total memory usage
        self.case_lim = []
        self.case_res = []

    #get a submission from judge queue
    def getSub(self, msg):
        getDict = json.loads(msg)
        self.sid = getDict['sid']
        self.lang = getDict['lang']
        self.pid = getDict['pid']
        self.case_cnt = getDict['case_cnt']
        self.spj = getDict['spj']
        self.block = getDict['block']
        self.time_lim = getDict['time_lim']
        self.mem_lim = getDict['mem_lim']
        self.case_lim = getDict['case_lim']
        #optional params
        if 'mode' in getDict:
            self.mode = getDict['mode'] # general submission | contest submission
        if 'code_path' in getDict:
            self.code_path = getDict['code_path'] # explicit code path
        if 'data_path' in getDict:
            self.code_path = getDict['data_path'] # explicit data directory path

        # debug
        f = open( '/home/buptacm/test.in', 'w')
        f.write( 'aaaa')
        f.close()

        return self

    #send a submission to judge queue
    def retSub(self):
        retDict = {
                'sid':self.sid,
                'case_cnt':self.case_cnt,
                'case_done':self.case_done,
                'status':self.status,
                'block':self.block,
                'ce':self.ce,
                'time':self.time,
                'mem':self.mem,
                'case_res':self.case_res,
                }
        #optional params
        if self.mode:
            retDict['mode'] = self.mode
       
        try:
            return json.dumps(retDict)
        except:
            retDict['ce'] = ''
            return json.dumps(retDict)
