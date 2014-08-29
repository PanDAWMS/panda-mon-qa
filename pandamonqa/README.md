# QA Suite for PanDA monitor

## Running the suite


1. Download the QA suite.
$WORKDIR is a directory of your choice, e.g. your $HOME.

        # cd $WORKDIR
        # git clone https://github.com/PanDAWMS/panda-mon-qa.git

2. Install dependency libraries. <br />
You can install them either on the system level (yum install \<package\>), or with pip (pip install \<package\>).

        python-twill
        python-nose
        python-beautifulsoup (Ubuntu 12.04 LTS) or python-BeautifulSoup (SLC6)
        Possible additional dependencies: requests=2.2.1, lxml, cssselect

3. Set up the environment.

        # cd $WORKDIR/panda-mon-qa/pandamonqa
        # export PYTHONPATH=$PWD:$PYTHONPATH

4. Run the suite.

    * to run a single site smoke test

            # cd $WORKDIR/panda-mon-qa/pandamonqa/run
            # python run_twill_clicker.py   bigpanda_root

    * to run smoke tests for all registered sites

            # python run_twill_clicker.py

    * to run a smoke test only against the homepage of this particular site

            # python run_twill_clicker.py -hp  bigpanda_root

    * to run a smoke test only against the homepage of all the sites 

            # python run_twill_clicker.py -hp

Configure the suite
--------------
All the configuration is done via .cfg files, you do not need to edit .py files. 


1. Register a new site into the list. <br />
in $WORKDIR/panda-mon-qa/pandamonqa/settings/settings-qasuite-sites.cfg do the
following:
    * Add a section.
    * Add SITENAME ... string ID which you call with run\_twill\_clicker.py.
    * ADD SITEDOMAIN ... string which will be reflected in the list-URLs config file (see below).
    * Example:

            [bigpanda_root]
            SITENAME = bigpanda_root
            SITEDOMAIN = bigpanda.cern.ch

2. Site instance configuration. <br />
e.g. in $WORKDIR/panda-mon-qa/pandamonqa/settings/settings-bigpanda\_root.cfg
file basename has expected pattern 'settings-%(SITENAME)s.cfg'
    * where SITENAME is an entry in run\_twill\_clicker.SITES (can be arg for
	run\_twill\_clicker). <br />
This file contains several sections:
    
            [AddressInfo]
            PAGE_ADDRESS ... string with the website hostname, e.g. http://bigpanda.cern.ch/
            [VersionInfo]
            PAGE_VERSION ... version string as a part of the page source, e.g. 0.0.1. As of 2014-06-11 we set it to the Google Analytics code.
            [BrowserInfo]
            PAGE_BROWSER ... User-Agent browser, e.g. Chrome or Firefox
            [Debugging]
            page_content_directory ... local directory to which page dump will be stored
            page_url_prefix ... URL location to page_content_directory
            [Errors]
            ignored_errors ... list of error patterns to ignore (force the test to succeed when such error occurs)


3. Site URLs list configuration. <br />
e.g. in $WORKDIR/panda-mon-qa/pandamonqa/settings/URL-list/list-URLs\_bigpanda\_root.bigpanda.cern.ch.cfg <br />
file basename has expected pattern 'list-URLS\_%(SITENAME)s.%(SITEDOMAIN)s.cfg'
    * SITENAME is an entry in run\_twill\_clicker.SITES (can be arg for run\_twill\_clicker),
    * SITEDOMAIN is the website domain.
This file contains a list of URLs of the website to visit. One URL per line.
One line can contain one URL and one regex pattern, delimited by a space
character.<br />
e.g.<br />

            http://pandawms.org/lsst/
             ... only URL is provided, no regex is provided
            http://pandawms.org/lsst/support/maxpandaid/ \d+
             ... one URL (http://pandawms.org/lsst/support/maxpandaid/) and one regex (\d+) is provided
            http://pandawms.org/lsst/?mode=quicksearch UA-44940804-1
             ... one URL and one regex (UA-44940804-1) is provided

4. Wrapper scripts.<br />
Wrapper scripts to run a particular QAsuite for a particular site can be
provided. Currently only one is available: $WORKDIR/panda-mon-qa/pandamonqa/scripts/run\_panda-mon-qa\_aipanda043\_8080.sh.


