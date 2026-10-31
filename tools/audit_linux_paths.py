"""Find statically resolvable path-case problems in a staged CK3 mod.

Reports do not prove native Linux compatibility. DLC virtual files and computed
paths are outside this scan. No game or mod files are modified.
"""
import argparse,json,re
from collections import defaultdict
from pathlib import Path

REFERENCE=re.compile(r'"([^"\r\n]+\.(?:dds|png|tga|mesh|anim|asset|gfx|gui|shader|fx|txt|ogg|wav|mp3|ttf|otf))"',re.I)
TEXT_EXT={'.txt','.asset','.gfx','.gui','.shader','.fx','.yml'}

def audit(game,mod):
    index=defaultdict(set);effective={};directories=defaultdict(set)
    for label,root in [('game',game),('compiled',mod)]:
        for p in root.rglob('*'):
            if not p.is_file():continue
            rel=p.relative_to(root).as_posix()
            index[rel.casefold()].add(rel)
            effective[rel.casefold()]=(label,p,rel)
            if label=='compiled':
                parent=p.relative_to(root).parent
                while parent!=Path('.'):
                    directories[parent.as_posix().casefold()].add(parent.as_posix());parent=parent.parent
    issues=[];unknown=[];checked=0
    for label,p,rel in effective.values():
        if label!='compiled' or p.suffix.lower() not in TEXT_EXT:continue
        source=p.read_text(encoding='utf-8-sig',errors='replace')
        for m in REFERENCE.finditer(source):
            value=m[1].replace('\\','/')
            if '/' not in value or any(c in value for c in '$[]\n'):continue
            checked+=1
            possibilities=index.get(value.casefold())
            entry={'file':rel,'line':source.count('\n',0,m.start())+1,'reference':m[1]}
            if possibilities and value not in possibilities:
                issues.append(dict(entry,existing_spellings=sorted(possibilities)))
            elif not possibilities:unknown.append(entry)
    return {'scope':'Static quoted resource paths only; DLC mounts and dynamic paths excluded',
        'linux_runtime_verified':False,'checked_references':checked,
        'case_mismatches':issues,'unresolved_or_dlc_paths':unknown,
        'split_case_directories':[sorted(v) for v in directories.values() if len(v)>1]}

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--game',type=Path,required=True)
    ap.add_argument('--mod',type=Path,required=True);ap.add_argument('--report',type=Path,required=True)
    a=ap.parse_args();result=audit(a.game,a.mod)
    a.report.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:len(v) if isinstance(v,list) else v for k,v in result.items()},ensure_ascii=False))
