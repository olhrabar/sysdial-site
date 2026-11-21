#!/usr/bin/env python3
"""Offline check of internal links/assets in all *.html and style.css: files must exist, #anchors must exist in the target page."""
import re,sys,os
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
pages=[os.path.join(d,f) for d,_,fs in os.walk(ROOT) for f in fs if f.endswith('.html') and '/.git' not in d and '/node_modules' not in d and '/tools/' not in d+'/']
class P(HTMLParser):
    def __init__(s): super().__init__(); s.refs=[]; s.ids=set()
    def handle_starttag(s,tag,a):
        a=dict(a)
        if a.get('id'): s.ids.add(a['id'])
        if tag=='a' and a.get('name'): s.ids.add(a['name'])
        for k in ('href','src','poster'):
            if a.get(k): s.refs.append((tag,k,a[k]))
        if a.get('srcset'):
            for part in a['srcset'].split(','): s.refs.append((tag,'srcset',part.strip().split()[0]))
data={}
for p in pages:
    ps=P(); ps.feed(open(p,encoding='utf-8').read()); data[p]=ps
def resolve(page,url):
    u=urlsplit(url)
    path=unquote(u.path)
    if not path: return page,u.fragment
    base=ROOT if path.startswith('/') else os.path.dirname(page)
    t=os.path.normpath(os.path.join(base,path.lstrip('/') if path.startswith('/') else path))
    if os.path.isdir(t): t=os.path.join(t,'index.html')
    return t,u.fragment
bad=[]; n=0
def check(page,tag,k,url):
    global n
    if re.match(r'^(https?:|//|mailto:|tel:|data:|javascript:)',url) or url=='' : return
    n+=1
    t,frag=resolve(page,url)
    rel=os.path.relpath(page,ROOT)
    if not os.path.isfile(t): bad.append('%s: <%s %s="%s"> -> missing %s'%(rel,tag,k,url,os.path.relpath(t,ROOT))); return
    if frag and t.endswith('.html'):
        ids=data[t].ids if t in data else None
        if ids is not None and frag not in ids and frag!='top': bad.append('%s: <%s %s="%s"> -> no #%s in %s'%(rel,tag,k,url,frag,os.path.relpath(t,ROOT)))
for p,ps in data.items():
    for tag,k,url in ps.refs: check(p,tag,k,url)
css=os.path.join(ROOT,'style.css')
for m in re.finditer(r'url\(\s*[\'"]?([^\'")]+)[\'"]?\s*\)',open(css,encoding='utf-8').read()):
    u=m.group(1)
    if not u.startswith(('data:','http')): check(css,'css','url',u)
print('checked %d internal references in %d pages + style.css'%(n,len(pages)))
if bad:
    print('\n'.join(bad)); sys.exit(1)
print('OK: no broken internal links, assets or anchors')
