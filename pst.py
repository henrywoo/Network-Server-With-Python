#!/usr/bin/env python
"""
A wrapper for displaying thread using ps
Print thread, thread number, the cpu where the thread is running
fuheng@2013
"""
import sys
import os

cmd1='ps -eo ruser,pid,ppid,lwp,nlwp,psr,args -L'
fname=os.path.basename(__file__)
cmd2='grep -v '+ fname
cmd3='grep --color=always -e "RUSE[R]"'

cmd = cmd1 + "|" +cmd2 + "|" +cmd3

def reg(s):
  return s[:-1] + '['+s[-1:]+']'

for i in sys.argv[1:]:
  cmd += ' -e "'+reg(i)+'"'

os.system(cmd)
print "-"*90
print(cmd)
"""
$./pst.py echo
ps -eo ruser,pid,ppid,lwp,nlwp,psr,args -L| grep -v pst.py| grep --color=always -e "RUSE[R]" -e  "ech[o]"
RUSER      PID  PPID   LWP NLWP PSR COMMAND
root     15069 13596 15069    1   0 vim -u /root/.simon.vimrc echo-poll.py
root     15980 13596 15980    1   0 vim -u /root/.simon.vimrc echo-thread.py
root     16767 13596 16767    2   1 /usr/bin/env python ./echo-thread.py
root     16767 13596 16771    2   1 /usr/bin/env python ./echo-thread.py

Besides, you can use
1. pstree -p
2. top + H
"""

