#!/bin/bash
ssh -vvv -tt atlpan@aipanda043.cern.ch /data/atlpan/update_bigpandamon_twdev.sh
touch /tmp/$USER.jenkins_twdev.continue

