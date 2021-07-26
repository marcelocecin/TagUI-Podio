import os, requests, json, re, urllib.parse
from flask import Flask, request, url_for, jsonify, abort
from functools import wraps
from celery import Celery
from bs4 import BeautifulSoup

ALLOWED_IPS = ['3.248.131.28', '54.171.83.63', '108.128.182.146', '127.0.0.1'] #https://workflow-automation.podio.com/help/whitelist-ip-addresses.php
API_HOST = "0.0.0.0"

app = Flask(__name__)

celery = Celery(app.name, broker='redis://localhost:6379/0')
celery.conf.worker_prefetch_multiplier = 1
celery.conf.task_acks_late = True
celery.conf.broker_url = 'redis://localhost:6379/0'
celery.conf.result_backend = 'redis://localhost:6379/0'

@celery.task(bind=True)
def save_podio_tagui(self, args):
    url = "https://procfu.com/exe/podio_app_item_get_raw.pf"
    payload='app_id=YOUR_PODIO_APP_ID_HERE&app_item_id='+args['script'] #
    headers = {'Authorization': 'Basic YOUR ProcFu Auth Token HERE','Content-Type': 'application/x-www-form-urlencoded','Cache-Control': 'no-cache'}
    response = requests.request("POST", url, headers=headers, data=payload)
    data = response.json()
    for item in data:
        for field in data['fields']:
            if field['external_id'] == 'tag':
                script = field['values'][0]['value']
                soup = BeautifulSoup(script,'html.parser')
                soup = soup.pre.prettify()
                soup = soup.replace("<br/>", "\n")
                soup = soup.replace("<pre>","")
                soup = soup.replace("</pre>","")
                soup = soup.replace("amp;","")
    textfile = open('/home/rpa/tagui/API/podio'+args['script']+'.tag', 'w')
    textfile.write(soup)
    textfile.close()
    return 'Script saved'

@celery.task(bind=True)
def run_podio_tagui(self, args):
    if "param1" in args:
        tagui_cmd = 'tagui /home/rpa/Downloads/TagUI_Linux/tagui/python/podio'+args['script']+'.tag '+args['param1']+' -q -h'
    if "param1" in args and "param2" in args:
        tagui_cmd = 'tagui /home/rpa/Downloads/TagUI_Linux/tagui/python/podio'+args['script']+'.tag '+args['param1']+' '+args['param2']+' -q -h'
    else:
        tagui_cmd = 'tagui /home/rpa/Downloads/TagUI_Linux/tagui/python/podio'+args['script']+'.tag -q -h'
    log = os.system(tagui_cmd+' > tagui.log')
    with open('tagui.log', 'r') as file:
        data = file.read().replace('\n', '')
    os.system("rm tagui.log")
    return data

def require_appkey(view_function):
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        with open('/home/rpa/tagui/API/api.key', 'r') as apikey:
            key=apikey.read().replace('\n', '')
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            abort(401)
    return decorated_function
  
@app.before_request
def limit_remote_addr():
    client_ip = str(request.remote_addr)
    valid = False
    for ip in ALLOWED_IPS:
        if client_ip.startswith(ip) or client_ip == ip:
            valid = True
            break
    if not valid:
        abort(403)

@app.route('/', methods=['POST'])
@require_appkey
def index():
    if request.form['submit'] == 'Save':
        script = request.form['script']
        arg_data = {'script': script}
        task = save_podio_tagui.delay(arg_data)
        return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}
    if request.form['submit'] == 'Run':
        if "script" in request.form and "param1" in request.form and "param2" in request.form:
            script = request.form['script']
            param1 = request.form['param1']
            param2 = request.form['param2']
            arg_data = {'script': script,'param1': param1,'param2': param2}
            task = run_podio_tagui.apply_async(args=[arg_data], countdown=1)
            return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}
        if "script" in request.form and "param1" in request.form:
            script = request.form['script']
            param1 = request.form['param1']
            arg_data = {'script': script,'param1': param1}            
            task = run_podio_tagui.apply_async(args=[arg_data], countdown=1)
            return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}
        if "script" in request.form:
            script = request.form['script']
            arg_data = {'script': script}            
            task = run_podio_tagui.apply_async(args=[arg_data], countdown=1)
            return jsonify({}), 202, {'Location': url_for('taskstatus',task_id=task.id)}
    else:
        abort(400)

@app.route('/status/<task_id>')
@require_appkey
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state,'current': 0,'total': 1,'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state,'current': task.info.get('current', 0),'total': task.info.get('total', 1),'status': task.info.get('status', '')}
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {'state': task.state,'current': 1,'total': 1,'status': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    app.run(host=API_HOST)
