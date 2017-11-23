# -*- coding:utf-8 -*-
from jenkinstask.util import merge

__env_setting = {
    "uat": {
        "jenkins_url": "http://10.20.32.20:8080/jenkins",
        "username": "jenkins_api",
        "token": "b627adc132fc3e49db012e752843c67b",
        "deploy": [{
            "template_format": "uat_{0}.xml",
            "server_name": "01",
            "branch_name": "develop",
            "task_parameter": ["GIT_URL", "PORT", "APP_NAME", 
                    "SERVICE_FARM", "SERVICE_GROUP", "THEME"]
        }]
    }
}

def load():
    return __env_setting