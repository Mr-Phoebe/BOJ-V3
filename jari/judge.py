# -*- coding: utf-8 -*-
import os
import resource
import sys
import signal
import cptrace
import time
import threading
from conf import JudgeConf as jcnf
from monotonic import monotonic_time as jclk
from diff import Diff

JDEBUG = False

class Judge(object):
    
    def __init__(self, run_path = None):
        if run_path:
            self.run_path = run_path
        else:
            self.run_path = jcnf.RUN_PATH

    def judge(self, sub):

        lang = sub.lang
        mem_policy = True if (jcnf.POLICY[lang]=='ALL' or jcnf.POLICY[lang]=='MEM') else False

        page_size = resource.getpagesize()

        case_cnt = min(len(sub.case_lim), sub.case_cnt)
        sub.case_done = 0
        case_id = 0

        for case_id in range(case_cnt):
            sub.case_res.append({
                'res':jcnf.JUDGE_RES['init'],
                'time':0,
                'mem':0,
                })

        exec_cmd = jcnf.EXEC_CMD[lang]
        exec_param = jcnf.EXEC_PARAM[lang]
        if lang == 'java':
            mem_lim = 0
            for case_id in xrange(case_cnt):
                mem_lim = max(mem_lim, sub.case_lim[case_id]['mem'])
            exec_param.insert(1, '-Xmx'+str(mem_lim/1024+1)+'m')

        for case_id in xrange(case_cnt):
            lim = sub.case_lim[case_id]
            res = sub.case_res[case_id]
            exec_pid = os.fork()


            if exec_pid == 0:
                for rk, rv in jcnf.EXEC_RLIM[lang].items():
                    resource.setrlimit(rk, rv)

                try:
                    exec_i = open(jcnf.getCasePathI(sub.pid, case_id), 'r')
                    exec_o = open(jcnf.getExecPathO(), 'w')
                except:
                    #sys.stderr.write('file read error')
                    raise Exception('cannot handle input or output file');

                lim['time'] = max(lim['time'], jcnf.EXEC_MIN_TL[lang])
                lim['time'] = int(lim['time']*jcnf.EXEC_TL_RATIO[lang])
                if lang == 'java':
                    lim['time'] *= 3
                rlimt = (lim['time']-1)//1000+2
                resource.setrlimit(resource.RLIMIT_CPU, (rlimt, rlimt));

                rlimm = jcnf.EXEC_MAX_MEM
                if mem_policy: # java uses virtual machine
                    resource.setrlimit(resource.RLIMIT_AS, (rlimm, rlimm));
            
                os.dup2(exec_i.fileno(), 0)
                os.dup2(exec_o.fileno(), 1)

                #TOTO: ptrace
                pt_ret = cptrace.ptrace(cptrace.PTRACE_TRACEME, 0)
                if (pt_ret == -1):
                    #sys.stderr.write('warning: ptrace error')
                    raise Exception('child process cannot be ptraced');
                    if exec_i:
                        exec_i.close()
                    if exec_o:
                        exec_o.close()
                    os._exit(1)

                os.execvp(exec_cmd, exec_param)

                sys.stderr.write('warning: something wrong')
                if exec_i:
                    exec_i.close()
                if exec_o:
                    exec_o.close()

                os._exit(1)

            else:
                stat_info_file = str(exec_pid).join(['/proc/', '/statm'])
                res['mem'] = 0
                res['time'] = 0
                t_prev = jclk()
                eax_prev = 142857
                insyscall = False
                def killProc():
                    try: 
                        os.kill(exec_pid, signal.SIGKILL)
                    except OSError:
                        pass
                    else:
                        res['res'] = jcnf.JUDGE_RES['re']
                threading.Timer((lim['time']-1)//1000+10, killProc).start()
                try:
                    while res['res']==jcnf.JUDGE_RES['init']:
                    #while True:
                        exec_status = os.wait4(exec_pid, 0)
                        if res['res']!=jcnf.JUDGE_RES['init']:
                            break
                        t_now = jclk()
                        res['time'] += t_now-t_prev
                        t_prev = t_now
                        DEBUG_CNT = 0
                        #res['mem'] = exec_status[2].ru_minflt-360
                        res['mem'] = exec_status[2].ru_maxrss

                        if os.WIFSIGNALED(exec_status[1]):
#strange exited     or tle?
                            if res['time']*1000>lim['time']:
                                res['res'] = jcnf.JUDGE_RES['tle']
                                break
                        elif os.WIFEXITED(exec_status[1]):
#normally exited    , ok
                            break
                        elif os.WIFSTOPPED(exec_status[1]):
#sigtrap by ptra    ce
                            exec_sig = os.WSTOPSIG(exec_status[1])
                            if exec_sig != signal.SIGTRAP:
                                res['res'] = jcnf.JUDGE_RES['re']
                                #print exec_status[0], exec_status[1], 'hehe', exec_sig
                                cptrace.ptrace(cptrace.PTRACE_KILL, exec_pid)
#strange exited?    
                                break
                            eax_now = cptrace.ptrace(cptrace.PTRACE_PEEKUSER, exec_pid, 4*cptrace.ORIG_EAX) #when used in 64bit system, it should be 8*xxxx, so it is recommended to make it a const in conf

                            if jcnf.POLICY[lang]=='ALL':
                                if jcnf.SYSCALL[eax_now][0] == 0: #prohibited syscall
                                    res['res'] = jcnf.JUDGE_RES['re']
                                    cptrace.ptrace(cptrace.PTRACE_KILL, exec_pid) #deprecated! should be implemented in another way
                                    break
                            else:
                                #TODO extend implementation
                                pass

                            if eax_now!=eax_prev and eax_now!=-1:
                                insyscall = False

                            if eax_now!=-1:
                                if insyscall:
                                    DEBUG_CNT+=1
                                    #if eax_now==45 or eax_now==90 or eax_now==91:
                                    try:
                                        stat_info = open(stat_info_file, 'r')
                                        mem_now = int(stat_info.read().split(' ')[5])  #automatically to long when exceed
                                        #res['mem'] = max(res['mem'], mem_now)
                                        stat_info.close()
                                    except:
                                        pass
                                    insyscall = False
                                else:
                                    insyscall = True

                            if mem_policy and res['mem']>lim['mem']: #res['mem']*page_size>lim['mem']*1024:
                                res['res'] = jcnf.JUDGE_RES['mle']
                                cptrace.ptrace(cptrace.PTRACE_KILL, exec_pid) #deprecated! should be implemented in another way
                                break
                            
                            if res['time']*1000>lim['time']:
                                res['res'] = jcnf.JUDGE_RES['tle']
                                cptrace.ptrace(cptrace.PTRACE_KILL, exec_pid) #deprecated! should be implemented in another way
                                break
                            if eax_now!=-1:
                                eax_prev = eax_now

                            t_prev = jclk()

                        else:
                            #sys.stderr.write('unknown status')
                            pass

                        #TODO: also check total time limit?
                        if res['res'] == jcnf.JUDGE_RES['tle']:
                            #TODO: write log
                            cptrace.ptrace(cptrace.PTRACE_KILL, exec_pid) #deprecated! should be implemented in another way
                        else:
                            cptrace.ptrace(cptrace.PTRACE_SYSCALL, exec_pid)
                except:
                    pass
                try:
                    os.wait()
                    os.kill(exec_pid, signal.SIGKILL)
                except Exception, e:
                    if JDEBUG: print 'cannot kill', Exception, e
                    pass
                res['mem'] = int(res['mem'])
                res['time'] = int(res['time']*1000)

                if res['res'] == jcnf.JUDGE_RES['init']:
                    if os.WIFSIGNALED(exec_status[1]):
                        res['res'] = jcnf.JUDGE_RES['re']
                    elif os.WIFSTOPPED(exec_status[1]) and os.WSTOPSIG(exec_status[1])!=signal.SIGTRAP:
                        res['res'] = jcnf.JUDGE_RES['re']

                if res['res'] == jcnf.JUDGE_RES['init']:
                    df = Diff()
                    res['res'] = df.diff(jcnf.getCasePathO(sub.pid, case_id), jcnf.getExecPathO())

                sub.case_done += 1
                #sub.mem += res['mem']
                sub.mem = max(sub.mem, res['mem'])
                sub.time += res['time']

                if res['res'] == jcnf.JUDGE_RES['init']:
                    res['res'] = jcnf.JUDGE_RES['se']

                # Need to calculate the scores of all test data, and thus we cannot break out when judging
                # if sub.block and res['res']!=jcnf.JUDGE_RES['ac']:
                #    break

                t_prev = jclk()
        
                sub.status = jcnf.SUB_STATUS['done']
        return sub.status
