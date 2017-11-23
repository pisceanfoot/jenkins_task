# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals, \
    with_statement
import logging
import jenkinsapi
from jenkinsapi.jenkins import Jenkins

logger = logging.getLogger(__name__)

class JenkinsApi(object):
    def __init__(self, url, username, token):
        logger.debug('create jenkins api instance')
        logger.debug('url %s username %s token %s', url, username, token)

        self.jenkins = Jenkins(url, username, token)

    def has_job(self, name):
        logger.info('check task "%s" exists', name)
        result = self.jenkins.has_job(name)

        logger.debug('return result %s', result)
        return result

    def create_job(self, name, xml):
        logger.debug('create task "%s", xml %s', name, xml)
        return self.jenkins.create_job(name, xml)

    def delete_job(self, name):
        logger.debug('upgrade task "%s", delete it', name)
        self.jenkins.delete_job(name) 

    def get_config(self, name):
        logger.debug('get task task "%s"', name)
        return self.jenkins[name].get_config()


if __name__ == '__main__':
    test_jenkins = JenkinsApi('http://10.20.32.20:8080/jenkins', 'jenkins_api', 'HCDhcd@123')
    result = test_jenkins.has_job('x')
    assert result == False

    # result = test_jenkins.create_job()
