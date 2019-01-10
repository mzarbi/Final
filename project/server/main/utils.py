import json

import requests
from flask import current_app

from app.models import Task


def upload_images(param,credentials):
    if(len(param) != 0):
        return launch_task(param,credentials).get_id()
    else:
        return None

def request_job_status(jobId):
    return current_app.task_queue.fetch_job(jobId).meta["progress"]

def request_uploaded_links(credentials):
    token = credentials["access_token"]
    authentication = {'Authorization': 'Bearer {0}'.format(token)}
    verify = True
    resp = requests.get("https://api.imgur.com/3/account/" + credentials["account_username"] + "/images/", {}, headers=authentication,
                        verify=verify)
    uploaded = []
    for i in json.loads(resp.content)["data"]:
        uploaded.append(i["link"])

    return {"uploaded": uploaded}

def launch_task(param,credentials,*args, **kwargs):
    tsk = Task()
    tsk.initialize(param,credentials)
    return current_app.task_queue.enqueue('app.tasks.long_process',tsk,*args, **kwargs)


