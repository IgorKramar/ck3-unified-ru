"""Small lossless span reader for Paradox script; comments and quoted braces are ignored."""
from dataclasses import dataclass
import re

TOKEN=re.compile(r'\s+|\#[^\n]*|"(?:\\.|[^"\\])*"|[{}]|[!?<>]?=|[<>]|[^\s{}=<>!?#"]+',re.S)

@dataclass
class Token:
    value:str
    start:int
    end:int

@dataclass
class Entry:
    key:str
    start:int
    end:int
    value_start:int
    value_end:int
    children:list|None
    operator:str='='

def tokens(text):
    result=[];pos=0
    for m in TOKEN.finditer(text):
        if text[pos:m.start()].strip('\ufeff \t\r\n'):
            raise ValueError(f'Unparsed input at {pos}: {text[pos:m.start()]!r}')
        v=m.group();pos=m.end()
        if v.isspace() or v.startswith('#'):continue
        result.append(Token(v,m.start(),m.end()))
    if text[pos:].strip():raise ValueError(f'Trailing unparsed input {text[pos:]!r}')
    return result

def parse(text):
    ts=tokens(text);i=0
    def block(closing=False):
        nonlocal i
        out=[]
        while i<len(ts):
            k=ts[i]
            if k.value=='}':
                if not closing:raise ValueError(f'Unexpected closing brace at {k.start}')
                i+=1;return out,k
            i+=1
            if i<len(ts) and ts[i].value in ('=','?=','!=','<','>','<=','>='):
                op=ts[i].value;i+=1
                if i>=len(ts):raise ValueError(f'Missing value after {k.value}')
                v=ts[i];i+=1
                if v.value=='{':
                    children,last=block(True)
                    out.append(Entry(k.value,k.start,last.end,v.start,last.end,children,op))
                elif v.value in ('rgb','hsv','hsv360') and i<len(ts) and ts[i].value=='{':
                    i+=1;children,last=block(True)
                    out.append(Entry(k.value,k.start,last.end,v.start,last.end,children,op))
                else:out.append(Entry(k.value,k.start,v.end,v.start,v.end,None,op))
            elif k.value=='{':
                children,last=block(True)
                out.append(Entry('',k.start,last.end,k.start,last.end,children,''))
            else:out.append(Entry(k.value,k.start,k.end,k.start,k.end,None,''))
        if closing:raise ValueError('Unclosed brace')
        return out,None
    return block()[0]

def walk(entries):
    for e in entries:
        yield e
        if e.children is not None:yield from walk(e.children)

def fields(entry,key):
    return [e for e in (entry.children or []) if e.key==key]

def apply(text,edits):
    last=len(text)
    for start,end,replacement in sorted(edits,reverse=True):
        if end>last:raise ValueError('Overlapping edits')
        text=text[:start]+replacement+text[end:];last=start
    return text

def canonical(text):
    return tuple(t.value for t in tokens(text))
