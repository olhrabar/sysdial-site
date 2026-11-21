#!/usr/bin/env python3
"""Generate pricing.html (English) and {lang}/pricing.html from template.html + strings/*.py.
Run from anywhere: python3 tools/pricing-i18n/build.py [--check]   (see README.md)"""
import re,importlib.util,sys,os,tempfile
sys.dont_write_bytecode=True
HERE=os.path.dirname(os.path.abspath(__file__))
SITE=os.path.abspath(os.path.join(HERE,'..','..'))+'/'
def load(code):
    sp=importlib.util.spec_from_file_location('s_'+code,os.path.join(HERE,'strings',code+'.py')); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m.L
TPL=open(os.path.join(HERE,'template.html'),encoding='utf-8').read()
EN=load('en')
LANGS=[('uk','Українська','uk'),('de','Deutsch','de'),('fr','Français','fr'),('es','Español','es'),('it','Italiano','it'),('nl','Nederlands','nl'),('pt','Português','pt-BR'),('pl','Polski','pl'),('cs','Čeština','cs'),('sk','Slovenčina','sk'),('hr','Hrvatski','hr'),('ro','Română','ro')]
HREF={'en':'https://sysdial.app/pricing.html'}
for c,_,h in LANGS: HREF[c]='https://sysdial.app/%s/pricing.html'%c
HL=[('en','en'),('uk','uk'),('de','de'),('fr','fr'),('es','es'),('it','it'),('nl','nl'),('pt','pt-BR'),('pl','pl'),('cs','cs'),('sk','sk'),('hr','hr'),('ro','ro')]
def hreflang(ind='  '):
    s=''.join('%s<link rel="alternate" hreflang="%s" href="%s">\n'%(ind,h,HREF[c]) for c,h in HL)
    return s+'%s<link rel="alternate" hreflang="x-default" href="%s">\n'%(ind,HREF['en'])
BRAND='<span class="brand-pro">SysDial&nbsp;<span>Pro</span></span>'
def wrap_brand(html):
    """Wrap every visible text 'SysDial Pro' in the brand markup. Skips <title>, <script>, <style>, comments and tag attributes."""
    out=[]; skip=None
    for tok in re.split(r'(<!--.*?-->|<[^>]+>)',html,flags=re.S):
        if tok.startswith('<'):
            m=re.match(r'<(/?)(script|style|title)\b',tok,re.I)
            if m: skip=None if m.group(1) else m.group(2).lower()
            out.append(tok)
        else:
            out.append(tok if skip else tok.replace('SysDial Pro',BRAND))
    return ''.join(out)
def esc_js(s): return s.replace('\\','\\\\').replace("'","\\'")
EN_TERMS_NOTE=' (EN)'
def fill(tpl,vals):
    a=tpl.index('  const D = {'); b=tpl.index('  const N = [1, 2, 5];')
    head,js,tail=tpl[:a],tpl[a:b],tpl[b:]
    def sub(t,esc):
        def r(m):
            k=m.group(1); v=vals[k]; return esc_js(v) if esc else v
        return re.sub(r'\{\{(\w+)\}\}',r,t)
    return sub(head,False)+sub(js,True)+sub(tail,False)
def reuse(code):
    idx=open(SITE+code+'/index.html',encoding='utf-8').read(); pv=open(SITE+code+'/privacy.html',encoding='utf-8').read()
    nav=re.search(r'<nav aria-label="([^"]*)">(.*?)</nav>',pv,re.S)
    labs=re.findall(r'<a href="[^"]*">([^<]*)</a>',nav.group(2))
    tell=re.search(r'<a href="mailto:support@sysdial.app\?subject=Tell[^>]*>([^<]*)</a>',idx).group(1)
    ft=re.search(r'<footer>.*?<span>© 2026 Oleksandr Hrabar\. (.*?)</span>\s*<nav aria-label="([^"]*)">.*?privacy.html">([^<]*)',idx,re.S)
    # feature table from homepage
    a=idx.rindex('<table class="plans">'); b=idx.index('</table>',a)+8
    tbl=idx[a:b]
    rows=re.findall(r'<tr[^>]*>.*?</tr>',tbl,re.S)
    assert len(rows)==15
    # row index 5 = Window row (first "no" row) gets class="line"
    assert rows[5].startswith('<tr><td>') and '<td class="no">' in rows[5] and '<td class="yes">✓</td></tr>' in rows[5] and '<td class="no">' not in rows[4]
    tbl=tbl.replace(rows[5],rows[5].replace('<tr>','<tr class="line">',1),1)
    return dict(nav_aria=nav.group(1),nav_feat=labs[0],nav_price=labs[1],nav_support=labs[2],tellme=tell,req=ft.group(1),foot_aria=ft.group(2),foot_priv=ft.group(3),fine3_priv=ft.group(3),FEATURE_TABLE=tbl)
def langsw(code,name):
    rows=[]
    rows.append(('en','English'))
    for c,n,_ in LANGS: rows.append((c,n))
    out=[]
    for c,n in rows:
        if c==code:
            out.append('        <span class="now"><span class="ico"><svg class="ck" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 6l3 3 5-6" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>%s</span>'%n)
        else:
            href='/pricing.html' if c=='en' else '/%s/pricing.html'%c
            out.append('        <a href="%s"><span class="ico"></span>%s</a>'%(href,n))
    return '\n'.join(out)
def build(code,name,htmllang):
    return wrap_brand(build_raw(code,name,htmllang))
def build_raw(code,name,htmllang):
    vals=dict(EN)
    if code!='en':
        vals.update(load(code))
        vals.update(reuse(code))
        vals['th_monthly']=vals['monthly']; vals['th_yearly']=vals['yearly']; vals['th_once']=vals['once']
        for n in (1,2,5): vals['row%d'%n]=vals['macs%d'%n]
        vals['fine1']=vals['usd_note']
        vals['foot_price']=vals['nav_price']
        vals['fine3_terms']+=EN_TERMS_NOTE; vals['fine3_ref']+=EN_TERMS_NOTE
        vals['foot_terms']+=EN_TERMS_NOTE; vals['foot_ref']+=EN_TERMS_NOTE
        missing=[k for k in re.findall(r'\{\{(\w+)\}\}',TPL) if k not in vals]; assert not missing,(code,missing)
        extra=[k for k in vals if k not in EN]; assert not extra,extra
    s=fill(TPL,vals)
    if code=='en':
        s=s.replace('<link rel="canonical" href="https://sysdial.app/pricing.html">\n','<link rel="canonical" href="https://sysdial.app/pricing.html">\n'+hreflang())
        s=re.sub(r'(      <div class="list">\n)(.*?)(      </div>\n    </details>)',lambda m:m.group(1)+langsw('en','English')+'\n'+m.group(3),s,flags=re.S)
        return s
    # --- structure for locale
    s=s.replace('<html lang="en">','<html lang="%s">'%htmllang)
    s=s.replace('<link rel="canonical" href="https://sysdial.app/pricing.html">\n','<link rel="canonical" href="%s">\n'%HREF[code]+hreflang())
    for p in ('images/icon.png','fonts/instrument-sans-latin-400-normal.woff2','fonts/instrument-sans-latin-700-normal.woff2'):
        s=s.replace('href="%s"'%p,'href="../%s"'%p).replace('src="%s"'%p,'src="../%s"'%p)
    s=s.replace('<link rel="stylesheet" href="style.css">','<link rel="stylesheet" href="../style.css">'+('\n  <style>:root { --font: \'Manrope\', -apple-system, BlinkMacSystemFont, \'Helvetica Neue\', Arial, sans-serif; }</style>' if code=='uk' else ''))
    s=s.replace('<a class="site" href="/">','<a class="site" href="/%s/">'%code)
    s=s.replace('<a href="/">%s</a>'%vals['nav_feat'],'<a href="/%s/">%s</a>'%(code,vals['nav_feat']))
    s=s.replace('<a href="/pricing.html" aria-current="page">','<a href="/%s/pricing.html" aria-current="page">'%code)
    s=s.replace('<span class="label">English</span>','<span class="label">%s</span>'%name)
    s=re.sub(r'(      <div class="list">\n)(.*?)(      </div>\n    </details>)',lambda m:m.group(1)+langsw(code,name)+'\n'+m.group(3),s,flags=re.S)
    s=s.replace('<a href="terms.html">','<a href="../terms.html">').replace('<a href="refunds.html">','<a href="../refunds.html">')
    s=s.replace('<a href="/pricing.html">%s</a>'%vals['foot_price'],'<a href="/%s/pricing.html">%s</a>'%(code,vals['foot_price']))
    s=s.replace('<a href="/privacy.html">%s</a></nav>'%vals['foot_priv'],'<a href="/%s/privacy.html">%s</a></nav>'%(code,vals['foot_priv']))
    return s
ALL=[('en','English','en')]+LANGS
def target(root,code): return root+('pricing.html' if code=='en' else code+'/pricing.html')
def main(argv):
    check='--check' in argv
    if not check:
        for code,name,hl in ALL:
            p=target(SITE,code); open(p,'w',encoding='utf-8').write(build(code,name,hl)); print('wrote',os.path.relpath(p,SITE))
        return 0
    bad=[]
    with tempfile.TemporaryDirectory() as tmp:
        for code,name,hl in ALL:
            out=build(code,name,hl)
            tp=target(tmp+'/',code); os.makedirs(os.path.dirname(tp),exist_ok=True); open(tp,'w',encoding='utf-8').write(out)
            try: cur=open(target(SITE,code),encoding='utf-8').read()
            except FileNotFoundError: cur=None
            if cur!=out: bad.append(os.path.relpath(target(SITE,code),SITE))
    if bad:
        print('pricing-i18n --check FAILED, out of date:',*bad,sep='\n  '); print('Run: python3 tools/pricing-i18n/build.py'); return 1
    print('pricing-i18n --check OK: all %d pricing pages match'%len(ALL)); return 0
if __name__=='__main__': sys.exit(main(sys.argv[1:]))
