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
    print 'sections', sections
    for section in sections:
        SITENAME = config.get(section, 'SITENAME')
        SITEDOMAIN = config.get(section, 'SITEDOMAIN')
        SITESDICT[SITENAME] = SITEDOMAIN
    print 'sitesdict=', SITESDICT
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
        a.PAGE_VERSION = QUICK_PAGE_VERSION
    errorlist = a.check_version()
    return errorlist




def get_list_URL(category_list_config):
    config=open(category_list_config, 'r')
    list_category_URL=config.read().split('\n')
    config.close()
    return list_category_URL


def clicker_generic_override_PAGE_ADDRESS_loop_categories(clicker_site_config, category_list_config):
    category_list_URL = get_list_URL(category_list_config)
    errors = []
    for category_page in category_list_URL:
        error = clicker_generic_override_PAGE_ADDRESS(clicker_site_config, category_page)
        #print category_page, error
        errors.append(error)
    ### summary;
    print 'Summary:', errors



def clicker_generic_SITENAME_HP(SITENAME):
    clicker_generic('%s/settings-%s.cfg' % (DIR_SETTINGS_CLICKER, SITENAME))


def clicker_generic_SITENAME_WHOLE(SITENAME, SITEDOMAIN):
    clicker_generic_override_PAGE_ADDRESS_loop_categories(\
        '%s/settings-%s.cfg' % (DIR_SETTINGS_CLICKER, SITENAME), \
        '%s/URL-list/list-URLs_%s.cfg' % (DIR_SETTINGS_CLICKER, SITEDOMAIN))


def get_WEBSITE_BASE_URL(site):
    config_file = '%s/settings-qasuite-sites.cfg' % (DIR_SETTINGS_CLICKER)
    sites_config = configure_qasuite(config_file)
    print sites_config
    return sites_config[site]


test_hp_only = clicker_generic_SITENAME_HP
test_whole_site = clicker_generic_SITENAME_WHOLE
site_base_url = get_WEBSITE_BASE_URL
SITES = configure_qasuite('%s/settings-qasuite-sites.cfg' % (DIR_SETTINGS_CLICKER))

