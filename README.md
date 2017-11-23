


Jenkins Task
=======================

jenkins task is use to help create job faster via jenkins xml config. It's very useful when you are using microservice or microservice like, while a lot of service need create in jenkins.

And if you want you chang all jenkins config, just simply run `upgrade`.


Two steps using Jenkins_Task
--------------------------------------

1. folk this repo and change jenkinstask/config/environment.py

```
__env_setting = {
    "uat": {
        "jenkins_url": "http://10.20.32.20:8080/jenkins",
        "username": "jenkins_api",
        "token": "b627adc132fc3e49db012e752843c67b",
        "deploy": [{
            "template_format": "uat_{0}.xml",   # will look up in folder 'template'
            "server_name": "01",                # optional, will repace ${SERVER_NAME} in template
            "branch_name": "develop",           # optional, will repace ${BRANCH_NAME} in template
            "task_parameter": ["GIT_URL", "PORT", "APP_NAME", 
                    "SERVICE_FARM", "SERVICE_GROUP", "THEME"]
        }]
    }
}
```


- jenkins_url - jenkins access url
- username - username
- token - which can be token or user password
- deploy - Array, so it can create multi task in jenkins with different template file.

  - template_format - file name format , the program will look up in folder 'jenkinstask/template'
  - server_name - optional, will repace ${SERVER_NAME} in template
  - Branch_name - optional, will repace ${BRANCH_NAME} in template
  - task_parameter - Array, will dynamci get attribute value in 'jenkinstask/task', and replace the template useing ${PARAMA_NAME} this kind of format.

2. Add task in folder jenkinstask/task

   Please take a look at Jenkinstask/task/foo.py for a example

   ```
   TEMPLATE = "service"

   APP_NAME="foo"
   GIT_URL="https://github.com/pisceanfoot/jenkins_task.git"
   PORT=3001
   ```

- TEMPLATE - which will use in template name, for this example in uat environment show above, it will use be 'uat_service.xml'. You can find it replace reserved word '%s' in deploy/template_format
- APP_NAME,GIT_URL and others - will use for replace template xml file, you can define what you want.

Get config from jenkins
-------------------------------------

```
python jenkinstask/main.py -c ${name} -e ${ENV}
```


Command
-------------------------------------

```
optional arguments:
  -h, --help            show this help message and exit
  -a, --all             run all tasks define in task folder
  -n NAME, --name NAME  run specific task
  -u, --upgrade         upgrade task
  -e ENV, --env ENV     only create specific env
  -c CONFIG, --config CONFIG
                        get config of specific task
  --debug               open debug
  ```
  
  for detail please run `python jenkinstask/main.py --help`
  
LICENSE
------------------------------------
This software is licensed under the Apache-2.0 License. See the LICENSE file in the top distribution directory for the full license text.
