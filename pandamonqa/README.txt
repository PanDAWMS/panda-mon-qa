QA Suite for PanDA monitor

###
### Running the suite
###
1] Download the QA suite
$WORKDIR is a directory of your choice, e.g. your $HOME.
# cd $WORKDIR
# git clone https://github.com/PanDAWMS/panda-mon-qa.git

1a] Install dependency libraries
	python-twill
	python-nose
	python-beautifulsoup (Ubuntu 12.04 LTS)
	python-BeautifulSoup (SLC6)
You can install them either on the system level (yum install <package>), or with pip (pip install <package>).


2] set up the environment
# cd $WORKDIR/panda-mon-qa/pandamonqa
# export PYTHONPATH=$PWD:$PYTHONPATH


3] run the suite
# cd $WORKDIR/panda-mon-qa/pandamonqa/run
# python run_twill_clicker.py bigpanda_root
or 
# python run_twill_clicker.py


###
### Configure the suite
###
1] Site instance configuration
e.g. in $WORKDIR/panda-mon-qa/pandamonqa/settings/settings-bigpanda_root.cfg
file basename has expected pattern 'settings-%(SITENAME)s.cfg'
	where SITENAME is an entry in run_twill_clicker.SITES (can be arg for run_twill_clicker).
This file contains several sections:
[AddressInfo]
PAGE_ADDRESS ... string with the website hostname, e.g. http://bigpanda.cern.ch/
[VersionInfo]
PAGE_VERSION ... version string as a part of the page source, e.g. 0.0.1. As of 2014-06-11 we set it to the Google Analytics code.
[BrowserInfo]
PAGE_BROWSER ... User-Agent browser, e.g. Chrome or Firefox


2] Site URLs list configuration
e.g. in $WORKDIR/panda-mon-qa/pandamonqa/settings/URL-list/list-URLs_bigpanda_root.bigpanda.cern.ch.cfg
file basename has expected pattern 'list-URLS_%(SITENAME)s.%(SITEDOMAIN)s.cfg'
	where SITENAME is an entry in run_twill_clicker.SITES (can be arg for run_twill_clicker),
	      SITEDOMAIN is the website domain
This file contains a list of URLs of the website to visit. One URL per line.



