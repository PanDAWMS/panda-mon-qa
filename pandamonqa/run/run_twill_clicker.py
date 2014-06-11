###   
###   Run as          python run_twill_clicker.py
###   
import re
import string
import sys
import traceback
from qasuite.suite import QASuite
from run.utils_twill import test_hp_only, test_whole_site
from run.version import QUICK_PAGE_VERSION

SITES = [
         'bigpanda_root', \
         ]


WEBSITE_BASE_URL = u'bigpanda.cern.ch'


def list_sites():
    sites_string=u''
    for site in SITES:
        sites_string = u'%s, %s' % (sites_string, site)
    return sites_string


def print_help():
    print u'Run as: \t\t\tprint python %s ARG' % sys.argv[0]
    print u'\t... ARG is a set of space-separated items from %s' % (SITES)


def clicker_bigpandamon():
    print u'bigpanda_root:'
    test_whole_site('bigpanda_root', 'bigpanda.cern.ch')


def clicker_bigpandamon_HP():
    print u'bigpanda_root HP:'
    test_hp_only('bigpanda_root')


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if re.search('help', arg):
            print_help()
            exit(0)
    
    ARGV=[]
    if len(sys.argv) == 1:
        print u'### WARNING ###\n\t\tNo site specified, will run over all of them: %s' % list_sites()
        ARGV = SITES
    else:
        ARGV=sys.argv[1:]
    
    
    for arg in ARGV:
        print u'Processing site:', arg
        arg1 = arg
        ### ensure selected site is on the list, or exit
        try:
            SITES.index(arg1)
        except ValueError:
            print u'\n### ERROR REPORT ###\n'
            print u'\t\tYou chose to test site "%s" which is not on list. Please feel free to reconsider your choice.' % (arg1)
            print_help()
            print u'\n### ERROR REPORT ###\n'
            traceback.format_exc()
            raise
        ### test either only the HP, or the whole site
        try:
            if re.search('hp', arg):
                arg1 = string.replace(arg, '-hp', '')
                test_hp_only(arg1)
            else:
                arg1 = arg
                _prepro = '%s.%s' % (arg1, WEBSITE_BASE_URL)
                test_whole_site(arg1, _prepro)
        except:
            traceback.format_exc()
            raise
    
    print u'Done!'


