# -*- coding:utf-8 -*-
import traceback
import copy

def format_exc():
	return traceback.format_exc()

def merge(defaultConfig, configs):
    new_config = copy.copy(defaultConfig)
    if not configs:
        return new_config

    return _merge(new_config, configs)

def _merge(new_config, configs):
    for key in configs:
        value = configs[key]
        if new_config.has_key(key):
            if type(value) == dict:
                _merge(new_config[key], value)
            else:
                new_config[key] = configs[key]  
        else:
            new_config[key] = configs[key]

    return new_config


if __name__ == '__main__':
    DEFAULT = {
        "A": 1,
        "B": 2,
        "C": {
            "C1": 1,
            "C3": 3,
            "a": {
                "b": 1
            }
        }
    }

    config = {
        # "A": 2,
        "B": 3,
        "C": {
            "C1": 222222,
            "C2": '333322',
            "a": {
                "c": 1
            }
        }
    }

    print merge(DEFAULT, config)
    
    try:
        caa()
        raise Exception('1231232')
        a = 1/0
    except:
        print format_exc()