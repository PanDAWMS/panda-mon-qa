# -*- coding: utf-8 -*-

"""
    QASuite
"""
import ConfigParser
import inspect
import os
import re
import twill.commands
import twill.extensions.check_links
import urllib
import urllib2
import urlparse
from BeautifulSoup import BeautifulSoup


VERB_SILENT = 0
VERB_STANDARD = 1
VERB_HIGH = 2
verbosity = 2


def printv(text, verb=VERB_HIGH):
    if verb <= verbosity:
        print text


class QASuite(object):
    """
        Set of methods to click through the pages
    """
    ALL_ANCHORS = []
    ALL_CLICKABLE_ANCHORS = []
    PAGE_ADDRESS = ''
    PAGE_BROWSER = ''
    PAGE_VERSION = ''
#    STATIC_LIST_ADDRESS = ''
#    STATIC_LIST_FILE = ''
#    STATIC_PREFIX = ''
#    STATICS = []
#    STATIC_SERVER = ''


    def configure(self, config_file):
        """
            configure: Read configuration from config_file.
            :param config_file: config file in the ini format
        """
#        printv(u'###### %s() IN' % (inspect.stack()[0][3]), VERB_STANDARD)

        config = ConfigParser.SafeConfigParser()
        config.read(config_file)

        self.PAGE_ADDRESS = config.get('AddressInfo', 'page_address')
        self.PAGE_BROWSER = config.get('BrowserInfo', 'page_browser')
        self.PAGE_VERSION = config.get('VersionInfo', 'page_version')
        self.ALL_ANCHORS = []
        self.ALL_CLICKABLE_ANCHORS = []
#        self.STATIC_LIST_ADDRESS = config.get('Statics', 'static_list_address')
#        self.STATIC_LIST_FILE = config.get('Statics', 'static_list_filename')
#        self.STATIC_PREFIX = config.get('Statics', 'static_address_prefix')
#        self.STATIC_SERVER = config.get('Statics', 'static_server')
#        self.STATICS = []

#        printv(u'###### %s() OUT' % (inspect.stack()[0][3]), VERB_STANDARD)

        return config


    def check_version(self):
        """
            Check the page source, look for the version number.
        """
        list_errors=[]
        list_warnings = []
        if not len(self.PAGE_ADDRESS):
            return ([], [])
        printv(u'###### %s() IN [for %s]' % (inspect.stack()[0][3], self.PAGE_ADDRESS), VERB_STANDARD)
        try:
            twill.commands.agent(self.PAGE_BROWSER)
            twill.commands.go(self.PAGE_ADDRESS)
        except twill.errors.TwillException:
            printv(u'First attempt to visit %s failed. Will retry once.' % (self.PAGE_ADDRESS), VERB_STANDARD)
            ### retry if the PAGE_ADDRESS times out
            try:
                twill.commands.agent(self.PAGE_BROWSER)
                twill.commands.go(self.PAGE_ADDRESS)
            except twill.errors.TwillException:
                printv(u'Even the second attempt to visit %s failed. Marking as warning.' % (self.PAGE_ADDRESS), VERB_STANDARD)
                result = "Page " + self.PAGE_ADDRESS + " timed out."
                list_warnings.append((self.PAGE_ADDRESS, self.PAGE_VERSION, result))
            
#        isOK = False
        try:
            twill.commands.code('200')
#            isOK = True
        except twill.errors.TwillAssertionError:
            result = 'Page status code ' + self.PAGE_ADDRESS + ' was ' + str(twill.commands.browser.get_code()) + '.'
            #raise twill.errors.TwillAssertionError(result)
            list_errors.append((self.PAGE_ADDRESS, self.PAGE_VERSION, result))

        try:
            twill.commands.find(self.PAGE_VERSION)
        except twill.errors.TwillAssertionError:
            result = 'Expected string ' + self.PAGE_VERSION + ' which is not there.'
#            raise twill.errors.TwillAssertionError(result)
            list_errors.append((self.PAGE_ADDRESS, self.PAGE_VERSION, result))

        if list_errors:
            printv('errors found: %s' % (list_errors))
        else:
            printv('OK (%s)' % (self.PAGE_ADDRESS))
        printv(u'###### %s() OUT' % (inspect.stack()[0][3]), VERB_STANDARD)
        return (list_errors, list_warnings)

