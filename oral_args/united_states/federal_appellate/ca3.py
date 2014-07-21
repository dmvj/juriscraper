#  Scraper for Third Circuit of Appeals
# CourtID: ca3
# Court Short Name: ca3
# Author: Andrei Chelaru
# Reviewer: mlr
# Date created: 18 July 2014

from datetime import datetime
import re

from juriscraper.lib.string_utils import fix_camel_case
from juriscraper.OralArgumentSite import OralArgumentSite


class Site(OralArgumentSite):
    def __init__(self):
        super(Site, self).__init__()
        self.court_id = self.__module__
        self.url = 'http://www2.ca3.uscourts.gov/oralargument/OralArguments.xml'

    def _get_download_urls(self):
        path = '//item/link'
        return map(self._return_download_url, self.html.xpath(path))

    @staticmethod
    def _return_download_url(e):
        return 'www2.ca3.uscourts.gov{end}'.format(end=e.tail)

    def _get_case_names(self):
        path = '//item/title/text()'
        return map(self._return_case_name, self.html.xpath(path))

    @staticmethod
    def _return_case_name(e):
        case_name = re.search('(\d{2}.*\d{3,4})?(.+).wma', e).group(2)
        return fix_camel_case(case_name)

    def _get_case_dates(self):
        path = '//item/description/text()'
        return map(self._return_case_date, self.html.xpath(path))

    @staticmethod
    def _return_case_date(e):
        return datetime.strptime(e, '%m/%d/%Y').date()

    def _get_docket_numbers(self):
        path = '//item/title/text()'
        return map(self._return_docket_number, self.html.xpath(path))

    @staticmethod
    def _return_docket_number(e):
        case_name = re.search('(\d{2}.*\d{3,4})?(.+).wma', e)
        docket_number = case_name.group(1)
        if docket_number:
            # Surround ampersands with spaces and remove dup spaces if created
            docket_number = ' '.join(re.sub('&', ' & ', docket_number).split())
            return docket_number
        else:
            return ''
