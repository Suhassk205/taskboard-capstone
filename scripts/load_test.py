import concurrent.futures,time,urllib.request
end=time.monotonic()+100
def run(_):
 total=0
 while time.monotonic()<end:
  with urllib.request.urlopen("http://127.0.0.1:8001/api/tickets",timeout=10) as response: response.read()
  total+=1
 return total
with concurrent.futures.ThreadPoolExecutor(max_workers=16) as pool:
 print("Successful API requests:",sum(pool.map(run,range(16))))
