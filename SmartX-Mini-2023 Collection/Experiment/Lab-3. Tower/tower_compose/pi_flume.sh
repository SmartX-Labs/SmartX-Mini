#!/bin/bash
#: Title : pi_flume.sh
#: Date : 20230429
#: Author : "Jiho Choi" <17choijiho@gm.gist.ac.kr>
#: Version : 1.0
#: Description : shell script to automate the process of hosts file update and automatic restart of flume agent
#: Usage : bash pi_flume.sh # inside NUC machine

# Set the local file to search and the string to look for
local_file=/etc/hosts
remote_file_path=/etc/hosts
search_string_pi="pi"
search_string_bp="black_pearl"

# Set the remote server's address, user, and password
remote_user="pirate"
remote_host=""
remote_password=hypriot

line_nuc=""
line_pi=""

if grep -q "$search_string_pi" "$local_file"; then
    line_nuc=`grep -w ${HOSTNAME} ${local_file} | tail -n 1`
    line_pi=`grep -w ${search_string_pi} ${local_file} | tail -n 1`
    remote_host=`echo ${line_pi} | awk '{print $1}'`
else
    line_nuc=`grep -w ${HOSTNAME} ${local_file} | tail -n 1`
    line_pi=`grep -w ${search_string_bp} ${local_file} | tail -n 1`
    remote_host=`echo ${line_pi} | awk '{print $1}'`
fi

# code to change /ets/hosts
sshpass -p $remote_password ssh -o StrictHostKeyChecking=no $remote_user@$remote_host "sudo bash -c 'echo ${line_nuc} >> $remote_file_path && echo ${line_pi} >> $remote_file_path && systemctl restart snmpd.service && cat /etc/hosts && docker rm -f flume'"

# flume container initialize and run
sshpass -p ${remote_password} ssh -o StrictHostKeyChecking=no ${remote_user}@${remote_host} "sudo bash -c 'sudo docker run --net=host -w /flume --name flume raspbian-flume sh -c \"sed -i \"s/nuc:9090,nuc:9091,nuc:9092/${HOSTNAME}:9090,${HOSTNAME}:9091,${HOSTNAME}:9092/g\" conf/flume-conf.properties && bin/flume-ng agent --conf conf --conf-file conf/flume-conf.properties --name agent -Dflume.root.logger=INFO,console\"'"


