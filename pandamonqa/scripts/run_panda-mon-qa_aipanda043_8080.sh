#!/bin/bash
# to run on aipanda043
# prerequisities: installed python-twill python-nose python-BeautifulSoup

SITE="aipanda043_8080"
INSTALL_DIR=/data/qa/panda-mon-qa/pandamonqa
export PYTHONPATH=${INSTALL_DIR}:${PYTHONPATH}
cd ${INSTALL_DIR}/run
python run_twill_clicker.py ${SITE}


