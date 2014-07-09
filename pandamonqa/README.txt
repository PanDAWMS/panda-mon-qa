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
	Possible additional dependencies: requests, lxml
You can install them either on the system level (yum install <package>), or with pip (pip install <package>).


2] set up the environment
# cd $WORKDIR/panda-mon-qa/pandamonqa
# export PYTHONPATH=$PWD:$PYTHONPATH


3] run the suite
# cd $WORKDIR/panda-mon-qa/pandamonqa/run
# python run_twill_clicker.py   bigpanda_root
	... to run a single site smoke test
or 
# python run_twill_clicker.py
	... to run smoke tests for all registered sites
or 
# python run_twill_clicker.py -hp  bigpanda_root
	... to run a smoke test only against the homepage of this particular site
or 
# python run_twill_clicker.py -hp
	... to run a smoke test only against the homepage of all the sites

###
### Configure the suite
###
All the configuration is done via .cfg files, you do not need to edit .py files. 


1] Register a new site into the list
in $WORKDIR/panda-mon-qa/pandamonqa/settings/settings-qasuite-sites.cfg
Add a section.
Add SITENAME ... string ID which you call with run_twill_clicker.py.
ADD SITEDOMAIN ... string which will be reflected in the list-URLs config file (see below).
Example:
[bigpanda_root]
SITENAME = bigpanda_root
SITEDOMAIN = bigpanda.cern.ch


2] Site instance configuration
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


3] Site URLs list configuration
e.g. in $WORKDIR/panda-mon-qa/pandamonqa/settings/URL-list/list-URLs_bigpanda_root.bigpanda.cern.ch.cfg
file basename has expected pattern 'list-URLS_%(SITENAME)s.%(SITEDOMAIN)s.cfg'
	where SITENAME is an entry in run_twill_clicker.SITES (can be arg for run_twill_clicker),
	      SITEDOMAIN is the website domain
This file contains a list of URLs of the website to visit. One URL per line.
One line can contain one URL and one regex pattern, delimited by a space
character.
e.g.
http://pandawms.org/lsst/
 ... only URL is provided, no regex is provided
http://pandawms.org/lsst/support/maxpandaid/ \d+
 ... one URL (http://pandawms.org/lsst/support/maxpandaid/) and one regex (\d+) is provided
http://pandawms.org/lsst/?mode=quicksearch UA-44940804-1
 ... one URL and one regex (UA-44940804-1) is provided


4] Wrapper scripts
Wrapper scripts to run a particular QAsuite for a particular site can be
provided. Currently only one is available:
$WORKDIR/panda-mon-qa/pandamonqa/scripts/run_panda-mon-qa_aipanda043_8080.sh


