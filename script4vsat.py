#!/usr/bin/python
#
# Paramiko
#
import paramiko
import sys
import subprocess

cmd_file = sys.argv[1]

first_jump = paramiko.SSHClient()
first_jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
first_jump.connect('first_host_ip', username='first_host_usr', password='first_host_pwd!', allow_agent=False) #first ssh jump
#
first_jumptransport = first_jump.get_transport()
dest_addr = ('second_host_ip', 22)
local_addr = ('first_host_ip', 22)
first_jumpchannel = first_jumptransport.open_channel("direct-tcpip", dest_addr, local_addr)
#
second_jump = paramiko.SSHClient()
second_jump.set_missing_host_key_policy(paramiko.AutoAddPolicy())
second_jump.connect('second_host_ip ', username='second_host_usr', password='second_host_pwd', allow_agent=False, sock=first_jumpchannel) #second ssh jump
#
selected_cmd_file = open(cmd_file, 'r') #open command.txt and read line by line
selected_cmd_file.seek(0)
for each_line in selected_cmd_file.readlines():
        stdin, stdout, stderr = second_jump.exec_command(each_line + '\n') #push command to modem
#
print stdout.read()
#
second_jump.close()
first_jump.close()
# End
os.system('killall -9 /opt/forticlientsslvpn/64bit/forticlientsslvpn_cli')
