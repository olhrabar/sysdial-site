#!/usr/bin/env python3
"""sitemap.xml: valid XML, every <loc> maps to an existing file, hreflang alternates are reciprocal and match each page's <link rel=alternate>."""
import os,sys,re
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
NS={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
HOST='https://sysdial.app'
errs=[]
try: tree=ET.parse(os.path.join(ROOT,'sitemap.xml'))
except ET.ParseError as e: print('sitemap.xml is not valid XML:',e); sys.exit(1)
def fpath(url):
    if not url.startswith(HOST+'/'): errs.append('not on %s: %s'%(HOST,url)); return None
    p=url[len(HOST):]
    p=p.split('#')[0]
    f=os.path.join(ROOT,p.lstrip('/'))
    if p.endswith('/'): f=os.path.join(f,'index.html')
    return f
urls={}
for u in tree.getroot().findall('s:url',NS):
    loc=u.find('s:loc',NS).text.strip()
    f=fpath(loc)
    if f and not os.path.isfile(f): errs.append('<loc> has no file: %s'%loc)
    alts={a.get('hreflang'):a.get('href') for a in u.findall('x:link',NS) if a.get('rel')=='alternate'}
    urls[loc]=alts
for loc,alts in urls.items():
    if not alts: continue
    if loc not in alts.values(): errs.append('%s is missing from its own alternate set'%loc)
    if 'x-default' not in alts: errs.append('%s: no x-default'%loc)
    for lang,href in alts.items():
        if href not in urls: errs.append('%s: alternate %s (%s) is not a <loc>'%(loc,lang,href)); continue
        back=urls[href]
        if back!=alts: errs.append('%s: alternates differ from %s (%s) -> not reciprocal'%(loc,href,lang))
# each page's own <link rel=alternate hreflang> equals the sitemap set
class H(HTMLParser):
    def __init__(s): super().__init__(); s.alts={}
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='link' and a.get('rel')=='alternate' and a.get('hreflang'): s.alts[a['hreflang']]=a['href']
for loc,alts in urls.items():
    f=fpath(loc)
    if not f or not os.path.isfile(f) or not alts: continue
    h=H(); h.feed(open(f,encoding='utf-8').read())
    if h.alts!=alts: errs.append('%s: <link hreflang> in the page differs from the sitemap'%os.path.relpath(f,ROOT))
print('sitemap: %d urls, %d with hreflang sets'%(len(urls),sum(1 for a in urls.values() if a)))
if errs: print('\n'.join(errs)); sys.exit(1)
print('OK: sitemap valid, files exist, hreflang reciprocal and consistent with pages')
