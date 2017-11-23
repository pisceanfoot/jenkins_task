# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals, \
    with_statement

import sys
import os
import logging
import pkgutil

from os.path import dirname, join
from jenkinstask import util

logger = logging.getLogger(__name__)

work_path = os.environ.get('work_path')

class TaskModule(object):
    def __init__(self, task_name, module):
        self.task_name = task_name
        self.module = module
        self.name = self.get("NAME", task_name)

    def __getitem__(self, name):
        return self.get_value(name)

    def get(self, name, default_value = None):
        value = self.get_value(name)
        if value == None and default_value != None:
            value = default_value

        return value

    def has_vale(self, name):
        return hasattr(self.module, name)

    def get_value(self, name):
        if hasattr(self.module, name):
            return getattr(self.module, name)
        else:
            return None

def load(name):
    logger.info('load task name "%s"', name)
    result = load_all(filter_name=name)
    if result:
        return result[0]
    else:
        return None

def load_all(filter_name = None):
    logger.info('load all task')

    if work_path:
        pwd = join(work_path, 'task')
    else:
        pwd = dirname(__file__)
        pwd = join(pwd, 'task')

    all_module = []
    for importer, package_name, _ in pkgutil.iter_modules([pwd]):
        if filter_name and package_name != filter_name:
            continue

        try:
            full_package_name = '%s.%s' % (pwd, package_name)
            if full_package_name not in sys.modules:
                module = importer.find_module(package_name
                            ).load_module(full_package_name)
            else:
                module = sys.modules[full_package_name]

            all_module.append(TaskModule(package_name, module))
        except:
            logger.error('load module name %s error %s', package_name, util.format_exc())

    return all_module


if __name__ == '__main__':
    pass
    # x = load('foo')
    # print(x.get_value('APPNAME'))
    # x = load('bar')
    # print(x.get_value('APPNAME'))
    # item = load_all()[0]
    # print(item.get_value('APPNAME'))

