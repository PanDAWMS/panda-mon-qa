###
###   Do not run this script!
###
import ConfigParser
import os
from qasuite.suite import QASuite
from run.version import QUICK_PAGE_VERSION
import run


DIR_SETTINGS_CLICKER = os.path.abspath(\
    os.path.join(os.path.dirname(os.path.dirname(run.__file__)), "settings"))

SITESDICT = {}
WEBSITE_BASE_URL = u'bigpanda.cern.ch'

def configure_qasuite(config_file):
    """
        configure: Read configuration from config_file.
        :param config_file: config file in the ini format
    """
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    ### read list of sites from the config file
    sections = config.sections()
#    print 'sections', sections
    for section in sections:
        SITENAME = config.get(section, 'SITENAME')
        SITEDOMAIN = config.get(section, 'SITEDOMAIN')
        SITESDICT[SITENAME] = SITEDOMAIN
#    print 'sitesdict=', SITESDICT
    return SITESDICT


def clicker_generic(config_file):
    a=QASuite()
    a.configure(config_file)
    a.PAGE_VERSION = QUICK_PAGE_VERSION
    a.check_version()


def clicker_generic_override_PAGE_ADDRESS(config_file, page_address):
    a=QASuite()
    a.configure(config_file)
    page_address_list = page_address.split(' ')
    if len(page_address_list) > 1:
        a.PAGE_ADDRESS = page_address_list[0]
        a.PAGE_VERSION = page_address_list[1]
    else:
        a.PAGE_ADDRESS = page_address
        if a.PAGE_VERSION == '':
            a.PAGE_VERSION = QUICK_PAGE_VERSION
    errorlist, warninglist = a.check_version()
    return errorlist, warninglist


def get_list_URL(category_list_config):
    config=open(category_list_config, 'r')
    list_category_URL=config.read().split('\n')
    config.close()
    return list_category_URL


def clicker_generic_override_PAGE_ADDRESS_loop_categories(clicker_site_config, category_list_config):
    category_list_URL = get_list_URL(category_list_config)
    errors = []
    warnings = []
    for category_page in category_list_URL:
        error, warning = clicker_generic_override_PAGE_ADDRESS(clicker_site_config, category_page)
        #print category_page, error
        if error != []:
            errors.append(error)
        if warning != []:
            warnings.append(warning)
    ### summary;
    if len(warnings):
        print
        print
        print
        print "Warnings:", warnings
    if len(errors):
        print
        print
        print
        errors_string = ''
        ### TODO FIXME: make ignored_errors configurable via settings!
        ignored_errors = ['ORA-01013: user requested cancel of current operation']
        ignored_errors_string = ''
        for err in errors:
            try:
                page_address, page_version, page_result, page_dump, startT, endT, \
                error_title, error_description = err[0]
            except:
                page_address = err
                page_version = page_result = page_dump = startT = endT = \
                error_title = error_description = ''
            err_str = """
Page: %(page_address)s
Time range (UTC):  from %(startT)s to %(endT)s
Version string:    %(page_version)s
Error:             %(page_result)s
Page dump:         %(page_dump)s
Django error:      %(error_title)s
                   %(error_description)s

""" % {'page_address': page_address, 'page_version': page_version, \
       'page_result': page_result, 'page_dump': page_dump, \
       'startT': startT, 'endT': endT, \
       'error_title': error_title, 'error_description': error_description \
        }
#            print err_str
            if error_description in ignored_errors:
                ignored_errors_string += err_str
                errors.pop(errors.index(err))
            else:
                errors_string += err_str
        ### print Ignored Errors
        if len(ignored_errors_string):
            print "Ignored Errors:"  # , errors
            print ignored_errors_string
            print
            print
            print
        ### print Ignored Errors
        if len(errors_string):
            print "Errors:"  # , errors
            print errors_string

    return errors, warnings


def clicker_generic_SITENAME_HP(SITENAME):
    clicker_generic('%s/settings-%s.cfg' % (DIR_SETTINGS_CLICKER, SITENAME))


def clicker_generic_SITENAME_WHOLE(SITENAME, SITEDOMAIN):
    errors, warnings = clicker_generic_override_PAGE_ADDRESS_loop_categories(\
        '%s/settings-%s.cfg' % (DIR_SETTINGS_CLICKER, SITENAME), \
        '%s/URL-list/list-URLs_%s.cfg' % (DIR_SETTINGS_CLICKER, SITEDOMAIN))
    return errors, warnings


def get_WEBSITE_BASE_URL(site):
    config_file = '%s/settings-qasuite-sites.cfg' % (DIR_SETTINGS_CLICKER)
    sites_config = configure_qasuite(config_file)
    print sites_config
    return sites_config[site]


test_hp_only = clicker_generic_SITENAME_HP
test_whole_site = clicker_generic_SITENAME_WHOLE
site_base_url = get_WEBSITE_BASE_URL
SITES = configure_qasuite('%s/settings-qasuite-sites.cfg' % (DIR_SETTINGS_CLICKER))

