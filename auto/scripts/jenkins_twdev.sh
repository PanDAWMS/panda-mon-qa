#!/bin/bash
# jenkins cron script to update RPMs
# to be run as jenkins job
# Contact Jaroslava.Schovancova@cern.ch with questions. 


echo "Running job $JOB_NAME for package $packagename."
echo "env:"
env
echo "whoami:"
whoami


### get new RPM version
export new_version_packagename=$( dirname $( find /data/build/QA_incoming/ -name $packagename'*' | sort -nr | head -n1) | sed -e "s#.rpm##g")
### install new RPM on aipanda043
#ssh -o StrictHostKeyChecking=no -vvv -t atlpan@aipanda043.cern.ch /data/atlpan/update_bigpandamon_twdev.sh
#/data/atlpan/scripts/run_update_bigpandamon_twdev_on_aipanda043.sh
flag_file=/tmp/$USER.jenkins_twdev.flag
touch $flag_file
continue_flag_file=/tmp/$USER.jenkins_twdev.continue
max_duration=300
step=10
i=0
while [ $i -lt $max_duration ]; 
do
    if [ -f $continue_flag_file ]; then
        i=$max_duration
    else
        sleep $step
        i=$((i+step))
    fi
done
### fetch installed RPM version
new_version_file=$PWD/$packagename.version
curl "http://aipanda043.cern.ch/version/$packagename" -o $new_version_file 2>/dev/null
new_version_packagename=$(cat $new_version_file)
### download smoke test suite
qa_suite_dir=$PWD/panda-mon-qa
if [ ! -d $qa_suite_dir ]; then
    git clone https://github.com/PanDAWMS/panda-mon-qa.git
fi
cd $qa_suite_dir
git pull
### configure smoke test suite
cd $qa_suite_dir/pandamonqa
export PYTHONPATH=$PWD:$PYTHONPATH
### run smoke test suite
python run/run_twill_clicker.py aipanda043_root
export test_result=$?
if [ "$test_result" -eq "0"  ]; then
### if smoke test successful -> move RPM from QA_incoming to QA_passed
    mv /data/build/QA_incoming/$new_version_packagename.rpm /data/build/QA_passed
#	/data/build-not-public/repo_QA_passed
else
### if smoke test failed -> move RPM from QA_incoming to QA_failed
    mv /data/build/QA_incoming/$new_version_packagename.rpm /data/build/QA_failed
#	/data/build-not-public/repo_QA_failed
fi
### cleanup
#rm -rf $qa_suite_dir 2>/dev/null
### TODO: refresh QA_passed/QA_failed repository
echo "Finished running job $JOB_NAME for package $packagename."

