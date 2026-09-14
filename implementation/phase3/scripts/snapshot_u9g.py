#!/usr/bin/env python3
"""Read-only snapshot of a saved GitHub open-PR search; paginate all discussions."""
import argparse, concurrent.futures, datetime, json, pathlib, subprocess, time

def api(endpoint, paginate=False):
    args=['gh','api',endpoint]
    if paginate: args += ['--paginate']
    for attempt in range(3):
        result=subprocess.run(args,capture_output=True,text=True)
        if result.returncode==0:
            if not paginate: return json.loads(result.stdout)
            decoder=json.JSONDecoder(); rest=result.stdout.lstrip(); pages=[]
            while rest:
                page,end=decoder.raw_decode(rest);pages.extend(page);rest=rest[end:].lstrip()
            return pages
        if attempt==2: raise RuntimeError(result.stderr)
        time.sleep(2**attempt)

def main():
    p=argparse.ArgumentParser();p.add_argument('--cache',required=True);p.add_argument('searches',nargs='+');a=p.parse_args()
    root=pathlib.Path(a.cache);root.mkdir(parents=True,exist_ok=True)
    records={}
    for path in a.searches:
        d=json.load(open(path))
        if d['total_count']!=len(d['items']):raise ValueError('Search is not fully paginated: '+path)
        for r in d['items']:
            repo=r['repository_url'].split('/repos/')[-1];records[(repo,r['number'])]=r
    def one(key):
        repo,num=key;stem=repo.replace('/','--')+'--'+str(num);out=root/(stem+'.json')
        if out.exists():return stem+' cached'
        base=f'repos/{repo}/pulls/{num}'
        d={'repo':repo,'number':num,'retrieved_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'pr':api(base),'files':api(base+'/files?per_page=100',True),
           'reviews':api(base+'/reviews?per_page=100',True),
           'inline_comments':api(base+'/comments?per_page=100',True),
           'issue_comments':api(f'repos/{repo}/issues/{num}/comments?per_page=100',True)}
        out.write_text(json.dumps(d,indent=2));return stem+' saved'
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for result in pool.map(one,sorted(records)):print(result,flush=True)
if __name__=='__main__':main()
