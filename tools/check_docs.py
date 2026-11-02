#!/usr/bin/env python3
"""Offline documentation integrity checks; no execution or network deployment."""
from pathlib import Path
from urllib.parse import unquote
import hashlib,json,re,subprocess,sys,unicodedata
ROOT=Path(__file__).resolve().parents[1]
LINK=re.compile(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+["\'][^)]*)?\)')
def slug(s):
 s=re.sub('<[^>]+>','',s).lower().strip()
 return ''.join(c for c in s if c in ' _-' or unicodedata.category(c)[0] in 'LN').replace(' ','-')
def targets(p):
 text=p.read_text(encoding='utf-8-sig');text=re.sub(r'```[\s\S]*?```|~~~[\s\S]*?~~~','',text)
 return [(n,m.group(1).strip('<>')) for n,l in enumerate(text.splitlines(),1) for m in LINK.finditer(l)]
def main():
 manifest=json.loads((ROOT/'docs/sources/import-manifest.json').read_text(encoding='utf-8'))['records']
 known=json.loads((ROOT/'docs/sources/historical-link-resolver.json').read_text(encoding='utf-8'))['entries']
 exemptions={(x['file'],x['originalLink']) for x in known}
 errors=[];links=0;graph={};historical={x['path'] for x in manifest}
 for row in manifest:
  p=ROOT/row['path']
  if not p.exists():errors.append('Missing original: '+row['path']);continue
  actual=subprocess.check_output(['git','-C',str(ROOT),'hash-object',row['path']],text=True).strip()
  if actual!=row['gitBlob']:errors.append('Historical Git blob changed: '+row['path'])
 files=sorted(p for p in ROOT.rglob('*.md') if '.git' not in p.relative_to(ROOT).parts)
 for p in files:
  rel=p.relative_to(ROOT).as_posix();graph[rel]=set()
  for n,url in targets(p):
   if re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',url) or url.startswith('//'):continue
   f,sep,a=unquote(url).partition('#');dest=(p.parent/f).resolve() if f else p
   links+=1
   if not dest.exists():
    if rel not in historical or (rel,url) not in exemptions:errors.append(f'{rel}:{n}: missing {url}')
    continue
   try:d=dest.relative_to(ROOT).as_posix()
   except ValueError:errors.append(f'{rel}:{n}: outside repository {url}');continue
   graph[rel].add(d)
   if sep and a and dest.suffix=='.md' and rel not in historical:
    text=dest.read_text(encoding='utf-8-sig');heads=[slug(x) for x in re.findall(r'^#{1,6}\s+(.+)$',text,re.M)]
    ids=set(re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)',text))
    if a not in heads and a not in ids:errors.append(f'{rel}:{n}: missing anchor {url}')
 reached=set();todo=['README.md','AGENTS.md']
 while todo:
  v=todo.pop()
  if v in reached:continue
  reached.add(v);todo.extend(graph.get(v,set())-reached)
 for p in files:
  rel=p.relative_to(ROOT).as_posix()
  if rel not in historical and rel not in reached:errors.append('Unreachable current document: '+rel)
 adrs=[p.name.split('-')[1] for p in (ROOT/'docs/decisions').glob('ADR-*.md')]
 if len(adrs)!=len(set(adrs)):errors.append('Duplicate ADR number')
 if errors:
  print('\n'.join(errors));return 1
 print(json.dumps({'result':'PASS','markdown':len(files),'historicalBlobsVerified':len(manifest),'relativeLinks':links,'historicalExceptions':len(known),'unreachableCurrentDocuments':0},ensure_ascii=False));return 0
if __name__=='__main__':sys.exit(main())
