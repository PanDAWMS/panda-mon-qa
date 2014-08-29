###
###   Run as          python run_twill_clicker.py
###   or              python run_twill_clicker.py <SITENAME>
###                        e.g. SITENAME=bigpanda_root
###                        or   SITENAME=bigpanda_prodsys
###

import re
import string
import sys
import traceback
from run.utils_twill import test_hp_only, test_whole_site, SITES, \
    WEBSITE_BASE_URL, site_base_url


def list_sites():
    sites_string = ', '.join(SITES.keys())
    return sites_string


def print_help():
    print u'Run as: \t\t\tprint python %s ARG' % sys.argv[0]
    print u'\t... ARG is a set of space-separated items from %s' % (SITES.keys())


def clicker_bigpandamon():
    for site in SITES.keys():
        print site
        test_whole_site(site, SITES[site])


def clicker_bigpandamon_HP():
    for site in SITES.keys():
        print site
        test_hp_only(site)


def main():
    for arg in sys.argv[1:]:
        if re.search('help', arg):
            print_help()
            exit(0)

    ARGV=[]
    if len(sys.argv) == 1:
        print u'### WARNING ###\n\t\tNo site specified, will run over all of them: %s' % list_sites()
        ARGV = SITES.keys()
    else:
        ARGV=sys.argv[1:]

    isHPtest = False
    HPstring = ''
    if re.search('-hp', ' '.join(ARGV)):
        isHPtest = True
        HPstring = '(HP only)'
        try:
            ARGV.pop(ARGV.index('-hp'))
        except:
            traceback.format_exc()
            raise

    if isHPtest and not len(ARGV):
        ARGV = SITES.keys()
        print u'### WARNING ###\n\t\tNo site specified, will run over all of them: %s' % list_sites()

    errors = []
    warnings = []
    for arg in ARGV:
        print u'Processing site:', arg, HPstring
        arg1 = arg
        ### ensure selected site is on the list, or exit
        try:
            SITES.keys().index(arg1)
        except ValueError:
            print u'\n### ERROR REPORT ###\n'
            print u'\t\tYou chose to test site "%s" which is not on list. Please feel free to reconsider your choice.' % (arg1)
            print_help()
            print u'\n### ERROR REPORT ###\n'
            traceback.format_exc()
            raise
        ### test either only the HP, or the whole site
        try:
            if isHPtest:
                test_hp_only(arg)
            else:
                try:
                    site_url = site_base_url(arg)
                except:
                    site_url = WEBSITE_BASE_URL
                urlstring = '%s.%s' % (arg, site_url)
                errors_new = []
                warnings_new = []
                errors_new, warnings_new = test_whole_site(arg, urlstring)
                if len(errors_new):
                    errors.extend(errors_new)
                del errors_new
                if len(warnings_new):
                    warnings.extend(warnings_new)
                del warnings_new
        except:
            traceback.format_exc()
            raise
        print
        print
        print

    if len(errors):
        print u'Failed.'
        exit(1)

    print u'Done!'
    exit(0)


if __name__ == "__main__":
    main()


