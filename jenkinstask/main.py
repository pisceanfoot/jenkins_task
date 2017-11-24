# -*- coding:utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals, \
    with_statement

import logging
import argparse

from jenkinstask import taskload
from jenkinstask.api import JenkinsApi
from jenkinstask.confFile import generator, loadConfig

logger = logging.getLogger(__name__)

def main(args):
    logger.debug('arguments %s', args)

    is_upgrade = args.upgrade
    workpath = args.workpath
    env = args.env
    if args.config:
        __get_job_config(args.config, env, workpath)
        return

    if args.name:
        module = taskload.load(args.name, work_path = workpath)
        if not module:
            logger.error('not module "%s" found or execute with error', args.name)
            return
        __create_job([module], is_upgrade, env, workpath)
    elif args.all:
        all_module = taskload.load_all(work_path = workpath)
        __create_job(all_module, is_upgrade, env, workpath)

def __create_job(all_module, is_upgrade, env_name, workpath):
    logger.info('create job')

    all_env = loadConfig(workpath)
    if env_name:
        logger.info('specific env "%s"', env_name)
        all_env = {env_name: all_env[env_name]}
    logger.debug('all envs %s', all_env)

    for currentEnv_name in all_env:
        __create_job_in_env(all_env[currentEnv_name], all_module, is_upgrade, workpath)

def __create_job_in_env(currentEnv, all_module, is_upgrade, workpath):
    logger.info('create job in env "%s"', currentEnv)

    deploySetting = currentEnv['deploy']
    for deploy in deploySetting:
        api = JenkinsApi(currentEnv['jenkins_url'], 
            currentEnv.get('username'), 
            currentEnv.get('token'))

        for module in all_module:
            if not api.has_job(module.name):
                xml_content = generator(deploy, module)
                api.create_job(module.name, xml_content)
            elif is_upgrade:
                xml_content = generator(deploy, module)
                api.update_config(module.name, xml_content)

def __get_job_config(name, env_name, workpath):
    if not env_name:
        raise Exception('env name must be set')
    logger.info('get config in env "%s" for task "%s"', env_name, name)

    all_env = loadConfig(workpath)
    currentEnv = all_env[env_name]
    api = JenkinsApi(currentEnv['jenkins_url'], 
            currentEnv.get('username'), 
            currentEnv.get('token'))

    config = api.get_config(name)
    print('Result ========>>>>>')
    print(config)
    print('=========<<<<<<< END')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--all', action='store_true', help='run all tasks define in task folder')
    parser.add_argument('-n', '--name', help='run specific task')
    parser.add_argument('-u', '--upgrade', action='store_true', help='upgrade task')
    parser.add_argument('-e', '--env', help='only create specific env')
    parser.add_argument('-c', '--config', help='get config of specific task')
    parser.add_argument('-w', '--workpath', help='set work path')
    parser.add_argument('--debug', action='store_true', help='open debug')
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-s: %(message)s')
        logger.debug('open debug')
    else:
        logging.basicConfig(level=logging.INFO,
                        format='%(levelname)-s: %(message)s')

    if not args.all and \
        not args.upgrade and \
        not args.name and \
        not args.config:
        parser.print_help()
    else:
        main(args)
