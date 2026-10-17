"""Populate a new demonstration workspace with sample campus requests."""
import argparse,json,urllib.request
parser=argparse.ArgumentParser()
parser.add_argument('--base-url',default='http://localhost:8000')
args=parser.parse_args()
rows=[
 ('Library Wi-Fi keeps disconnecting','IT','urgent','open','Network team','Suhas'),
 ('Projector in Seminar Hall 2 needs attention','Facilities','high','in_progress','Facilities team','Ananya'),
 ('Access to the assessment portal','Academics','medium','open','Academic office','Rohan'),
 ('Replace the reading-room desk lamp','Facilities','low','resolved','Facilities team','Meera'),
 ('Student ID card is not opening the lab','IT','high','in_progress','IT support','Aditya'),
 ('Need a transcript for the internship application','Academics','medium','open','Academic office','Kavya'),
 ('Water dispenser on the second floor is offline','Facilities','urgent','open','Facilities team','Arjun'),
 ('Connect a laptop to the presentation screen','IT','low','resolved','IT support','Nisha')]
existing=json.load(urllib.request.urlopen(args.base_url+'/api/tickets'))
if existing:
 print('Workspace already has requests; preserving existing data.')
else:
 for title,category,priority,status,owner,requester in rows:
  payload=json.dumps(dict(title=title,description='Sample request for the campus helpdesk demonstration.',category=category,priority=priority,status=status,owner=owner,requester=requester)).encode()
  request=urllib.request.Request(args.base_url+'/api/tickets',data=payload,headers={'Content-Type':'application/json'},method='POST')
  with urllib.request.urlopen(request) as response:print(response.status,json.load(response)['title'])
