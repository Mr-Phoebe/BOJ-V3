# -*- coding: utf-8 -*-
import re
import sys
import signal
import os
import resource
import subprocess
import shutil
from sub import Sub
from conf import JudgeConf as jcnf

class Compile(object):

    def __init__(self, run_path = None):
        if run_path:
            self.run_path = run_path
        else:
            self.run_path = jcnf.RUN_PATH

    def _ceFilter(self, ce):
        filter_policy = [(jcnf.RUN_PATH, '/${TOKISAKI_KURUMI}/'),]
        for f in filter_policy:
            ce = re.sub(f[0], f[1], ce)
        return ce

    def compile(self, sub):

        sub.status = jcnf.SUB_STATUS['compiling']

        if os.path.exists(self.run_path):
            shutil.rmtree(self.run_path)

        try:
            os.mkdir(self.run_path, 0755)
        except (OSError): # TODO write log
            sys.stderr.write('could not remake run path')
            raise Exception('could not remake run path')

        if sub.code_path:
            self.code_path = sub.code_path
        else:
            self.code_path = jcnf.getSubPath(sub.sid)
        try:
            shutil.copyfile(self.code_path, self.run_path+jcnf.getSrcName(sub.lang))
        except (shutil.Error, IOError): # TODO write log
            sys.stderr.write('source file does not exist')
            raise Exception('source file does not exist')

        cmpl_pid = os.fork()

        if cmpl_pid == 0:  # child process

            cmpl_cmd = jcnf.CMPL_CMD[sub.lang]
            cmpl_param = jcnf.CMPL_PARAM[sub.lang]

            try:
                cmpl_err = open(self.run_path+'ce', 'w')
            except:
                sys.stderr.write('cannot log compilation info')
                raise Exception('cannot log compilation info')
            os.dup2(cmpl_err.fileno(), 2)

            resource.setrlimit(resource.RLIMIT_CPU, jcnf.CMPL_RLIM['RLIMIT_CPU'])
            os.execvp(cmpl_cmd, cmpl_param)

            cmpl_err.flush()
            cmpl_err.close()
            os._exit(os.EX_OK)

        else:
            
            cmpl_ret = 0
            while True:
                cmpl_status = os.waitpid(cmpl_pid, 0)
                if os.WIFEXITED(cmpl_status[1]):
                    cmpl_ret = 0
                    break
                elif os.WIFSIGNALED(cmpl_status[1]) or os.WIFSTOPPED(cmpl_status[1]):
                    cmpl_ret = 1
                    break
                os.stderr.write('unknown stat')

            if os.WEXITSTATUS(cmpl_status[1]) != 0:
                cmpl_ret = 1

            if cmpl_ret != 0:
                cmpl_err = open(self.run_path+'ce', 'r')
                sub.ce = self._ceFilter(cmpl_err.read())
                sub.status = jcnf.SUB_STATUS['compilation error']
                cmpl_err.close()

            try:
                os.kill(cmpl_pid, signal.SIGKILL)
            except:
                pass

            if sub.status == jcnf.SUB_STATUS['compiling']:
                sub.status = jcnf.SUB_STATUS['judging']
            return sub.status

