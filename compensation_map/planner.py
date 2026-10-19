from copy import deepcopy
from functools import lru_cache
import hashlib
import json
import re
import time


def canonical(value):return json.dumps(value,sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)


def condition_valid(condition,domains):
    if not isinstance(condition,dict) or any(k not in domains for k in condition):return False
    for key,rule in condition.items():
        if not isinstance(rule,dict):
            if canonical(rule) not in {canonical(x) for x in domains[key]}:return False
        else:
            if len(rule)!=1:return False
            op,value=next(iter(rule.items()))
            if op in ("gt","ge","lt","le"):
                if type(value) is not int or any(type(v) is not int for v in domains[key]):return False
            elif op in ("eq","ne"):
                if canonical(value) not in {canonical(x) for x in domains[key]}:return False
            elif op=="in":
                if not isinstance(value,list) or not value or any(canonical(v) not in {canonical(x) for x in domains[key]} for v in value):return False
            else:return False
    return True


def holds(state,condition):
    for key,rule in condition.items():
        actual=state[key]
        if not isinstance(rule,dict):
            if canonical(actual)!=canonical(rule):return False
        else:
            op,value=next(iter(rule.items()))
            result={"eq":lambda:canonical(actual)==canonical(value),"ne":lambda:canonical(actual)!=canonical(value),
                    "gt":lambda:actual>value,"ge":lambda:actual>=value,"lt":lambda:actual<value,"le":lambda:actual<=value,
                    "in":lambda:canonical(actual) in {canonical(x) for x in value}}[op]()
            if not result:return False
    return True


def apply(state,operation,domains):
    result=deepcopy(state)
    result.update(operation.get("set",{}))
    for key,delta in operation.get("delta",{}).items():result[key]+=delta
    if any(canonical(result[k]) not in {canonical(x) for x in domains[k]} for k in result):raise ValueError("invalid_effect_outside_domain")
    return result


def dedup(worlds):return [json.loads(w) for w in sorted({canonical(w) for w in worlds})]


def validate(case):
    if not isinstance(case,dict) or not isinstance(case.get("domains"),dict) or not 1<=len(case["domains"])<=12:raise ValueError("invalid_domains")
    domains=case["domains"]
    for key,values in domains.items():
        if not isinstance(key,str) or not re.fullmatch(r"[a-z][a-z0-9_]{0,50}",key) or not isinstance(values,list) or not 1<=len(values)<=20 or any(type(v) not in (str,int,bool) or isinstance(v,str) and len(v)>128 or type(v) is int and abs(v)>1000000 for v in values) or len({canonical(v) for v in values})!=len(values):raise ValueError("invalid_domain")
    initial=case.get("initial")
    if not isinstance(initial,dict) or set(initial)!=set(domains) or any(canonical(v) not in {canonical(x) for x in domains[k]} for k,v in initial.items()):raise ValueError("invalid_initial")
    if not condition_valid(case.get("goal"),domains) or not case["goal"]:raise ValueError("invalid_goal")
    for collection in ("operations","compensations","observations"):
        items=case.get(collection,[])
        if not isinstance(items,list) or len(items)>12 or any(not isinstance(x,dict) for x in items):raise ValueError("invalid_actions")
        ids=[x.get("id") for x in items]
        if any(not isinstance(k,str) or not k for k in ids) or len(set(ids))!=len(ids):raise ValueError("invalid_action_ids")
        for item in items:
            if collection!="operations" and (type(item.get("cost")) is not int or not 1<=item["cost"]<=10000):raise ValueError("invalid_cost")
            if collection=="observations":
                if not isinstance(item.get("fields"),list) or not item["fields"] or any(k not in domains for k in item["fields"]):raise ValueError("invalid_observation_fields")
            else:
                if not condition_valid(item.get("pre",{}),domains):raise ValueError("invalid_precondition")
                if not isinstance(item.get("set",{}),dict) or not isinstance(item.get("delta",{}),dict):raise ValueError("invalid_effect")
                for key,value in item.get("set",{}).items():
                    if key not in domains or canonical(value) not in {canonical(x) for x in domains[key]}:raise ValueError("invalid_set_effect")
                for key,value in item.get("delta",{}).items():
                    if key not in domains or type(value) is not int or not -100<=value<=100 or any(type(x) is not int for x in domains[key]):raise ValueError("invalid_delta_effect")
    trace=case.get("trace",[])
    if not isinstance(trace,list) or len(trace)>12:raise ValueError("invalid_trace")
    ids={a["id"] for a in case.get("operations",[])}
    if any(not isinstance(t,dict) or t.get("operation") not in ids or t.get("status") not in ("confirmed","unknown","not_applied","not_started") for t in trace):raise ValueError("invalid_trace")
    if not condition_valid(case.get("observed",{}),domains):raise ValueError("invalid_observed_facts")
    return domains


def reconstruct(case):
    domains=validate(case)
    operations={a["id"]:a for a in case.get("operations",[])}
    worlds=[case["initial"]]
    for event in case.get("trace",[]):
        operation=operations[event["operation"]]
        next_worlds=[]
        for world in worlds:
            if event["status"] in ("unknown","not_applied","not_started"):next_worlds.append(world)
            if event["status"] in ("confirmed","unknown") and holds(world,operation.get("pre",{})):
                next_worlds.append(apply(world,operation,domains))
        worlds=dedup(next_worlds)
        if not worlds:raise ValueError("invalid_trace_no_possible_world")
        if len(worlds)>64:raise ValueError("invalid_belief_limit")
    worlds=[w for w in worlds if holds(w,case.get("observed",{}))]
    if not worlds:raise ValueError("invalid_observations_exclude_all_worlds")
    return worlds


def verify_plan(case,tree,worlds=None):
    """Independent path execution in each possible world, without planner memo data."""
    domains=validate(case)
    worlds=reconstruct(case) if worlds is None else worlds
    actions={a["id"]:a for a in case.get("compensations",[])}
    observations={a["id"]:a for a in case.get("observations",[])}
    paths=[]
    for original in worlds:
        state=deepcopy(original);node=tree;cost=0;steps=[]
        for _ in range(20):
            if node["kind"]=="done":
                if not holds(state,case["goal"]):raise ValueError("invalid_goal_not_reached")
                paths.append({"initial_world":original,"final_world":state,"cost":cost,"steps":steps})
                break
            if node["kind"]=="action":
                action=actions[node["id"]]
                if not holds(state,action.get("pre",{})):raise ValueError("invalid_action_precondition")
                state=apply(state,action,domains);cost+=action["cost"];steps.append({"action":action["id"]});node=node["next"]
            elif node["kind"]=="observe":
                observation=observations[node["id"]];value={k:state[k] for k in observation["fields"]};cost+=observation["cost"];steps.append({"observe":observation["id"],"value":value})
                branches=[b for b in node["branches"] if canonical(b["value"])==canonical(value)]
                if len(branches)!=1:raise ValueError("invalid_observation_branch")
                node=branches[0]["plan"]
            else:raise ValueError("invalid_plan_node")
        else:raise ValueError("invalid_plan_depth")
    return {"valid":True,"worlds_checked":len(paths),"worst_case_cost":max(p["cost"] for p in paths),"paths":paths,"external_actions_executed":False}


def plan(case,max_depth=7,seconds=3):
    domains=validate(case)
    if type(max_depth) is not int or not 0<=max_depth<=9 or type(seconds) not in (int,float) or not 0<seconds<=10:raise ValueError("invalid_search_budget")
    worlds=reconstruct(case)
    fingerprint=hashlib.sha256(canonical(case).encode()).hexdigest()
    touched={k for a in case.get("compensations",[]) for k in list(a.get("set",{}))+list(a.get("delta",{}))}
    for world in worlds:
        for key,rule in case["goal"].items():
            if key not in touched and not holds(world,{key:rule}):
                return {"status":"requires_human_review","reason":"unreachable_immutable_goal","witness":{"field":key,"value":world[key],"goal":rule},"worlds":worlds,"snapshot_sha256":fingerprint,"source_case":deepcopy(case),"plan":None,"external_actions_executed":False}
    deadline=time.monotonic()+seconds;exhausted=False;visited=0

    @lru_cache(maxsize=50000)
    def search(signature,depth):
        nonlocal exhausted,visited
        visited+=1
        if time.monotonic()>=deadline or visited>50000:exhausted=True;return None
        belief=json.loads(signature)
        if all(holds(w,case["goal"]) for w in belief):return {"kind":"done","cost":0}
        if depth==0:return None
        options=[]
        for action in case.get("compensations",[]):
            if not all(holds(w,action.get("pre",{})) for w in belief):continue
            try:next_worlds=dedup([apply(w,action,domains) for w in belief])
            except ValueError:continue
            next_signature=canonical(next_worlds)
            if next_signature==signature:continue
            tail=search(next_signature,depth-1)
            if tail is not None:options.append({"kind":"action","id":action["id"],"cost":action["cost"]+tail["cost"],"next":tail})
        for observation in case.get("observations",[]):
            groups={}
            for world in belief:
                value={k:world[k] for k in observation["fields"]};groups.setdefault(canonical(value),[]).append(world)
            if len(groups)<=1:continue
            branches=[]
            for key,group in sorted(groups.items()):
                tail=search(canonical(dedup(group)),depth-1)
                if tail is None:break
                branches.append({"value":json.loads(key),"plan":tail})
            if len(branches)==len(groups):options.append({"kind":"observe","id":observation["id"],"cost":observation["cost"]+max(b["plan"]["cost"] for b in branches),"branches":branches})
        return min(options,key=lambda p:(p["cost"],canonical(p))) if options else None

    tree=search(canonical(dedup(worlds)),max_depth)
    if tree is None:return {"status":"requires_human_review","reason":"search_budget_exhausted" if exhausted else "no_plan_within_depth_bound","plan":None,"worlds":worlds,"snapshot_sha256":fingerprint,"source_case":deepcopy(case),"max_depth":max_depth,"states_checked":visited,"external_actions_executed":False}
    verification=verify_plan(case,tree,worlds)
    if verification["worst_case_cost"]!=tree["cost"]:raise RuntimeError("independent_cost_replay_failed")
    return {"status":"plan_for_review","plan":tree,"worlds":worlds,"snapshot_sha256":fingerprint,"source_case":deepcopy(case),
            "worst_case_cost":tree["cost"],"minimum_cost_within_depth_proven":not exhausted,
            "max_depth":max_depth,"states_checked":visited,"verification":verification,"external_actions_executed":False}
