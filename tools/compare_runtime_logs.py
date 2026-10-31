"""Conservative comparison of source error fingerprints, not a causal proof."""
import argparse,json,re,collections
from pathlib import Path
HEADER=re.compile(r'^\[[^\]]+\]\[([A-Z])\]\[([^\]]+)\]: ?(.*)$')

def fingerprints(path):
    result=collections.Counter();examples={};block=[];module=None
    def commit():
        if not module:return
        text='\n'.join(block)
        error=re.search(r'^\s*Error:\s*(.+)',text,re.M)
        location=re.search(r'^\s*Script location:\s*(.+)',text,re.M)
        loc_key=re.search(r"Data error in loc string '([^']+)'",text)
        if error and location:key=('script',location[1].strip(),error[1].strip())
        elif loc_key:key=('localization',loc_key[1])
        else:key=('engine',module,block[0].strip() if block else '')
        result[key]+=1;examples.setdefault(key,text[:1600])
    for line in path.read_text(encoding='utf-8-sig',errors='replace').splitlines():
        m=HEADER.match(line)
        if m:
            commit();block=[m[3]];module=m[2] if m[1]=='E' else None
        elif module:block.append(line)
    commit();return result,examples

def compare(baseline,core):
    base,be=fingerprints(baseline);active,ce=fingerprints(core)
    shared=set(base)&set(active)
    def rows(keys):
        return [{'fingerprint':k,'baseline_occurrences':base[k],'core_occurrences':active[k],
                 'example':ce.get(k,be.get(k))} for k in sorted(keys)]
    return {'limits':'Different campaign worlds/durations; exact fingerprints shared with no-mod baseline are reproduced without mods. Unmatched errors are not thereby proven mod-caused.',
       'baseline_unique':len(base),'core_unique':len(active),'shared_unique':len(shared),
       'reproduced_without_mods':rows(shared),'core_unmatched':rows(set(active)-shared),
       'baseline_only':rows(set(base)-shared)}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--baseline',type=Path,required=True);p.add_argument('--core',type=Path,required=True);p.add_argument('--report',type=Path,required=True)
    a=p.parse_args();r=compare(a.baseline,a.core);a.report.write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:r[k] for k in ('baseline_unique','core_unique','shared_unique')},ensure_ascii=False))
