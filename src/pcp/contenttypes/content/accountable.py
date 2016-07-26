"""Mixin class for content that is accountable (like resources)
"""

SERVER_URL = "http://accounting.eudat.eu/"
USERKEY = "ACCOUNTING_USER"
PWKEY = "ACCOUNTING_PW"

import os
import json
import requests

class Accountable(object):
    """Mixin class for things that are accountable"""

    def addAccount(self, owner=None, test=False):
        """
        Create an account at the accounting server under the object's UID.
        If no owner id is passed the provider hosting the resource will own 
        the account. If 'test' is true the 'test' domain will be used.
        """
        id = self.UID()
        if owner is None:
            owner = self.aq_parent.Title()
        data = "?id=%s&owner=%s" % (id, owner)
        credentials = self.getCredentials()
        if credentials is None:
            return "No credentials found in the environment - doing nothing"
        if test:
            url = SERVER_URL + 'test/addAccount' + data
        else:
            url = SERVER_URL + 'eudat/addAccount' + data
        r = requests.post(url, auth=credentials)
        return r
            

    def getCredentials(self):
        """
        Look up username and password to be used at the accounting server
        in the environment variables ACCOUNTING_USER and ACCOUNTING_PW
        respectively.
        """
        user = os.getenv(USERKEY)
        password = os.getenv(PWKEY)
        if not user or not password:
            return None
        return (user, password)

    def getRecords(self, n=20, test=False):
        """
        Retrieve the last n records in the account. If 'test' is True lookup is 
        done in the 'test' domain
        """
        id = self.UID()
        domain = test and 'test/' or 'eudat/'
        credentails = self.getCredentials()
        if credentials is None:
            return "No credentials found in the environment - doing nothing"
        url = SERVER_URL + domain + id + '/listRecords?n=' + n
        r = requests.get(url, auth=credentials)
        data = json.loads(r.content)
        return data
