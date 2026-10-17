"""Record the actual tests, Compose stack, and API/database verification."""
from pathlib import Path
import json,sys,urllib.request
from lab_evidence import Evidence,ROOT

e=Evidence('','02-backend-tests','CampusDesk - isolated backend API tests',context='SQLite test database; fresh database per test')
e.run([str(ROOT/'.venv/bin/pytest'),'-v','--junitxml='+str(ROOT/'evidence/backend-tests.xml')],cwd=ROOT/'backend')
e=Evidence('','03-compose-stack','CampusDesk - Docker Compose build and runtime checks',context='Local Docker Compose stack')
e.run(['docker','compose','up','--build','-d'],timeout=300)
e.run(['docker','compose','ps'])
for service in ['backend','frontend']:
 e.run(['docker','compose','exec','-T',service,'id'])
e.run(['curl','--fail','--silent','--include','http://localhost:3000'])
e.run(['curl','--fail','--silent','http://localhost:8000/ready'])
e=Evidence('','04-api-database','CampusDesk - real API lifecycle and PostgreSQL migration',context='Running local FastAPI and PostgreSQL services')
payload=json.dumps({'title':'Verify capstone request lifecycle','category':'IT','priority':'high','requester':'Suhas'})
ticket=json.loads(e.run(['curl','--fail','--silent','-H','Content-Type: application/json','-X','POST','--data',payload,'http://localhost:8000/api/tickets']))
e.run(['curl','--fail','--silent',f'http://localhost:8000/api/tickets/{ticket["id"]}'])
ticket['status']='resolved';ticket['owner']='IT support'
e.run(['curl','--fail','--silent','-H','Content-Type: application/json','-X','PUT','--data',json.dumps(ticket),f'http://localhost:8000/api/tickets/{ticket["id"]}'])
e.run(['curl','--fail','--silent','--include','-X','DELETE',f'http://localhost:8000/api/tickets/{ticket["id"]}'])
e.run([sys.executable,'scripts/seed_demo.py'])
e.run(['curl','--fail','--silent','http://localhost:8000/api/tickets/stats'])
e.run(['docker','compose','exec','-T','postgres','psql','-U','campusdesk','-d','campusdesk','-c','SELECT version_num FROM alembic_version; SELECT id, title, status, owner FROM tickets ORDER BY id;'])
e=Evidence('','05-backend-metrics','CampusDesk - Prometheus-format backend metrics',context='Actual request metrics from the local API')
e.run(['curl','--fail','--silent','http://localhost:8000/metrics'])
