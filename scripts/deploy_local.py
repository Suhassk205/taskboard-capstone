"""Deploy the actual application to the existing local Kubernetes cluster."""
import json,subprocess
from pathlib import Path
from lab_evidence import Evidence,ROOT
NS='campusdesk'
e=Evidence('','06-helm-deployment','CampusDesk - Helm installation and healthy Kubernetes resources')
e.run(['kind','load','docker-image','campusdesk-backend:local','campusdesk-frontend:local','--name','session13'],timeout=180)
e.run(['kubectl','--context','kind-session13','apply','-f','k8s/namespace.yaml'])
password=next(line.split('=',1)[1] for line in (ROOT/'.env').read_text().splitlines() if line.startswith('DATABASE_PASSWORD='))
secret={'apiVersion':'v1','kind':'Secret','metadata':{'name':'campusdesk-db','namespace':NS},'type':'Opaque','stringData':{'DATABASE_PASSWORD':password}}
e.k(NS,'apply','-f','-',input=json.dumps(secret))
e.run(['helm','--kube-context','kind-session13','upgrade','--install','campusdesk','helm/campusdesk','-n',NS,'--set','ingress.host=campusdesk.localhost','--wait','--timeout','5m'],timeout=360)
e.k(NS,'get','pods','-o','wide')
e.k(NS,'get','svc')
e.k(NS,'get','ingress')
e.run(['helm','--kube-context','kind-session13','list','-n',NS])
e.k(NS,'exec','deployment/backend','--','python','-c','import urllib.request; print(urllib.request.urlopen("http://backend:8000/ready").read().decode())')
