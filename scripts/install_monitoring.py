"""Install the classroom monitoring stack without writing passwords to Git."""
from pathlib import Path
import argparse,json,secrets,subprocess

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--context',default='kind-session13')
args=parser.parse_args()
def run(command,**kwargs):
    subprocess.run(command,cwd=ROOT,check=True,**kwargs)
def k(*command,**kwargs):
    run(['kubectl','--context',args.context,*command],**kwargs)

namespace={'apiVersion':'v1','kind':'Namespace','metadata':{'name':'monitoring'}}
k('apply','-f','-',input=json.dumps(namespace),text=True)
existing=subprocess.run(['kubectl','--context',args.context,'-n','monitoring','get','secret','campusdesk-grafana-admin'],capture_output=True)
if existing.returncode:
    password=secrets.token_hex(24)
    secret={'apiVersion':'v1','kind':'Secret','metadata':{'name':'campusdesk-grafana-admin','namespace':'monitoring'},'stringData':{'username':'admin','password':password}}
    k('apply','-f','-',input=json.dumps(secret),text=True)
    with (ROOT/'.env').open('a') as local:
        local.write('GRAFANA_PASSWORD='+password+'\n')

run(['helm','repo','add','prometheus-community','https://prometheus-community.github.io/helm-charts'])
run(['helm','repo','add','grafana','https://grafana.github.io/helm-charts'])
run(['helm','repo','update'])
for release,chart,values in [('prometheus','prometheus-community/prometheus','monitoring/prometheus-values.yaml'),('grafana','grafana/grafana','monitoring/grafana-values.yaml')]:
    run(['helm','--kube-context',args.context,'upgrade','--install',release,chart,'-n','monitoring','-f',values,'--wait','--timeout','5m'])
dashboard=json.loads((ROOT/'monitoring/campusdesk-dashboard.json').read_text())
config={'apiVersion':'v1','kind':'ConfigMap','metadata':{'name':'campusdesk-dashboard','namespace':'monitoring','labels':{'grafana_dashboard':'1'}},'data':{'campusdesk.json':json.dumps(dashboard)}}
k('apply','-f','-',input=json.dumps(config),text=True)
k('-n','monitoring','get','pods,svc')
