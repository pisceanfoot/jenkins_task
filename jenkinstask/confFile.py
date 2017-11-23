# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals, \
    with_statement
import logging
import os
import json
from os.path import dirname, join

logger = logging.getLogger(__name__)
work_path = os.environ.get('work_path')

def loadConfig():
    file_name = "config/environment.json"
    if work_path:
        pwd = join(work_path, file_name)
    else:
        pwd = join(dirname(__file__), file_name)

    logger.debug('load config from %s', pwd)
    with open(pwd) as f:
        return json.load(f, encoding='utf-8')

def generator(deploy, task):
    logger.info('generator xml config for job "%s"', task.name)

    if work_path:
        pwd = join(work_path, 'template')
    else:
        pwd = join(dirname(__file__), 'template')

    template_format = deploy['template_format']
    template_name = task.get('TEMPLATE')
    if not template_name:
        raise Exception('no template_name found in task %s', task.task_name)

    template_name = template_format.format(template_name)
    file_path = join(pwd, template_name)

    logger.debug('template file path "%s"', file_path)
    return __format_xml(file_path, deploy, task)

def __format_xml(file_path, deploy, task):
    server_name = deploy.get('server_name')
    branch_name = deploy.get('branch_name')
    task_parameter = deploy.get('task_parameter')

    xml_content = None
    with open(file_path, 'r') as content_file:
        xml_content = content_file.read()

    if server_name:
        cmd_server_name = __buildParameterName("SERVER_NAME")
        xml_content = xml_content.replace(cmd_server_name, server_name)
    if task_parameter:
        for name in task_parameter:
            value = str(task.get(name, ""))

            cmd_name = __buildParameterName(name)
            xml_content = xml_content.replace(cmd_name, value)
    if not task.has_vale('BRANCH_NAME') and branch_name:
        cmd_branch_name = __buildParameterName("BRANCH_NAME")
        xml_content = xml_content.replace(cmd_branch_name, branch_name)

    return xml_content


def __buildParameterName(name):
    return "${{{0}}}".format(name)


