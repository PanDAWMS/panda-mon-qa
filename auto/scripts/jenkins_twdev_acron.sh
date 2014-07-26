#!/bin/bash

flag_file=/tmp/$USER.jenkins_twdev.flag
lock_file=/tmp/$USER.jenkins_twdev.lock
msg_file=/tmp/$USER.jenkins_twdev.msg
max_duration=300
step=10
ADMIN="jschovan@gmail.com"
SUBJ_PREFIX="[jenkins_twdev_acron] "
MAILDATESTRING=$(date -u +%F.%H%M%S)

i=0
while [ $i -lt $max_duration ]; 
do
    if [ -f $flag_file ]; then
        touch $lock_file
        if [ ! -f /data/atlpan/scripts/run_update_bigpandamon_twdev_on_aipanda043.sh ]; then
            echo "Missing file /data/atlpan/scripts/run_update_bigpandamon_twdev_on_aipanda043.sh on $(hostname). Running as $(whoami)." | mail -s "${SUBJ_PREFIX} ${MAILDATESTRING}" ${ADMIN}
        fi
        /data/atlpan/scripts/run_update_bigpandamon_twdev_on_aipanda043.sh
        rm -fv $flag_file $lock_file
    fi
    sleep $step
    i=$((i+step))
done

if [ -n "$(find $lock_file -mmin +5 2>/dev/null)" ]; then 
    echo "Found stalled lock file $lock_file: $(ls -l $lock_file). Will remove it. Running as $(whoami)@$(hostname)." > $msg_file
    rm -fv $lock_file 2>&1 >>$msg_file
    mail -s "${SUBJ_PREFIX} ${MAILDATESTRING}" ${ADMIN} < $msg_file
    rm -rf $msg_file 2>/dev/null
fi



