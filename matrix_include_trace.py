"""Offline, bounded captured-input analysis. Original implementation, MIT."""
import argparse
import json
import re
import sys
from pathlib import Path

class InputError(ValueError):
    pass

def obj(x,required,optional=()):
    if not isinstance(x,dict) or set(x)-set(required)-set(optional) or set(required)-set(x):
        raise InputError("object keys do not match the documented contract")
    return x

def arr(x,limit=512):
    if not isinstance(x,list) or len(x)>limit:raise InputError("expected a bounded array")
    return x

def text(x):
    if not isinstance(x,str) or not 1<=len(x)<=256:raise InputError("expected a nonempty string <=256 characters")
    return x

def integer(x,maximum=9223372036854775807):
    if type(x) is not int or not 0<=x<=maximum:raise InputError("expected bounded nonnegative integer")
    return x

def unique(xs):
    if len(set(xs))!=len(xs):raise InputError("duplicate identity")
    return xs

def pairs(ps):
    d={}
    for k,v in ps:
        if k in d:raise InputError("duplicate JSON key")
        d[k]=v
    return d

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument("snapshot",type=Path);a=p.parse_args()
    try:
        with a.snapshot.open("rb") as f:raw=f.read(2*1024*1024+1)
        if len(raw)>2*1024*1024:raise InputError("snapshot exceeds2 MiB")
        d=json.loads(raw.decode("utf-8"),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(InputError("nonfinite JSON")))
        result=analyze(d);print(json.dumps(result,sort_keys=True,ensure_ascii=True));return 1 if result.get("findings") else 0
    except (InputError,ValueError,TypeError,KeyError,OSError,RecursionError) as e:
        print(json.dumps({"error":str(e)}),file=sys.stderr);return 2

import itertools

def scalar(x):
    if x is None or type(x) is bool:return x
    if type(x) is int and -(2**63)<=x<2**63:return x
    if isinstance(x,str) and len(x)<=256 and "${{" not in x:return x
    raise InputError("only literal null/bool/int/string matrix values supported")

def same(a,b):return type(a) is type(b) and a==b

def config(x):
    if not isinstance(x,dict) or len(x)>32:raise InputError("expected bounded matrix object")
    for k,v in x.items():
        if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_-]{0,63}",k):raise InputError("invalid matrix key")
        scalar(v)
    return x

def analyze(d):
    obj(d,["axes"],["include","exclude"])
    axes=d["axes"]
    if not isinstance(axes,dict) or len(axes)>8:raise InputError("expected at most8 axes")
    size=1
    for k,values in axes.items():
        config({k:None});arr(values,32)
        if not values:raise InputError("empty axes unsupported")
        for v in values:scalar(v)
        if any(same(v,w) for i,v in enumerate(values) for w in values[:i]):raise InputError("duplicate axis values unsupported")
        size*=len(values)
        if size>256:raise InputError("matrix product exceeds256")
    exclude=[config(x) for x in arr(d.get("exclude",[]),256)]
    if any(not x or set(x)-set(axes) for x in exclude):raise InputError("exclude entries must be nonempty and name existing axes")
    include=[config(x) for x in arr(d.get("include",[]),256)]
    if not axes and not include:raise InputError("provide axes or include entries")
    originals=[dict(zip(axes,vs)) for vs in itertools.product(*axes.values())] if axes else []
    jobs=[];excluded=[]
    for i,c in enumerate(originals):
        matching=[j for j,x in enumerate(exclude) if all(k in c and same(c[k],v) for k,v in x.items())]
        if matching:excluded.append({"base_index":i,"configuration":c,"exclude_entries":matching})
        else:jobs.append({"base_index":i,"configuration":dict(c),"include_entries":[]})
    trace=[]
    for i,inc in enumerate(include):
        targets=[]
        for j,job in enumerate(jobs):
            if job["base_index"] is None:continue
            original=originals[job["base_index"]]
            if all(k not in original or same(original[k],v) for k,v in inc.items()):
                job["configuration"].update(inc);job["include_entries"].append(i);targets.append(j)
        if not targets:
            jobs.append({"base_index":None,"configuration":dict(inc),"include_entries":[i]});targets=[len(jobs)-1];action="append"
        else:action="merge_originals"
        if len(jobs)>256:raise InputError("expanded matrix exceeds256 jobs")
        trace.append({"include_entry":i,"action":action,"job_indexes":targets})
    return {"jobs":jobs,"job_count":len(jobs),"excluded":excluded,"include_trace":trace,"original_count":len(originals),"findings":[],"workflow_execution_performed":False}

if __name__ == "__main__":
    raise SystemExit(main())
