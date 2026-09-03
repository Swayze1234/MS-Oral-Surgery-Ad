import openpyxl,glob,json,re
from collections import defaultdict
from datetime import datetime
files=sorted(glob.glob('source/*.xlsx'))
def secs(s):
    m=re.match(r'(\d+)h (\d+)m (\d+)s',s); return int(m[1])*3600+int(m[2])*60+int(m[3])
hosts=defaultdict(lambda:{'plays':0,'secs':0,'first':None,'last':None,'city':'','playlist':'','versions':[]})
versions=[]
for f in files:
    ws=openpyxl.load_workbook(f,data_only=True).worksheets[0]
    rows=list(ws.iter_rows(values_only=True))
    fname=rows[0][1]; ver=int(re.search(r'FS_(\d)',fname)[1])
    tot=rows[2][2]; totdur=rows[2][3]
    vsum={'version':ver,'file':fname,'plays':tot,'secs':secs(totdur),'first':None,'last':None,'demo_plays':0}
    for r in rows[4:]:
        if not r[0] or r[0]=='Host': continue
        host,city,st,zipc,reg,pl,pc,pd,sd,ed=r
        sd=datetime.strptime(sd,'%m/%d/%Y').date(); ed=datetime.strptime(ed,'%m/%d/%Y').date()
        if 'Dealer Demo' in host: vsum['demo_plays']+=pc
        h=hosts[host]; h['plays']+=pc; h['secs']+=secs(pd); h['city']=city; h['playlist']=pl
        h['first']=min(h['first'],sd) if h['first'] else sd
        h['last']=max(h['last'],ed) if h['last'] else ed
        h['versions'].append({'v':ver,'plays':pc,'start':str(sd),'end':str(ed)})
        if 'Dealer Demo' not in host:
            vsum['first']=min(vsum['first'],sd) if vsum['first'] else sd
            vsum['last']=max(vsum['last'],ed) if vsum['last'] else ed
    vsum['first']=str(vsum['first']); vsum['last']=str(vsum['last'])
    versions.append(vsum)
for h in hosts.values(): h['first']=str(h['first']); h['last']=str(h['last'])
out={'versions':versions,'hosts':dict(hosts)}
json.dump(out,open('agg.json','w'),indent=1,default=str)
print(json.dumps(versions,indent=1))
for name,h in sorted(hosts.items(),key=lambda x:-x[1]['plays']):
    print(f"{h['plays']:>7} {h['secs']/3600:7.1f}h {h['first']} -> {h['last']}  {name}  [{h['city']}] {h['playlist']}")
allp=sum(h['plays'] for n,h in hosts.items() if 'Demo' not in n)
alls=sum(h['secs'] for n,h in hosts.items() if 'Demo' not in n)
print('TOTAL excl demo',allp,alls/3600)
print('TOTAL incl demo',sum(h['plays'] for h in hosts.values()))
