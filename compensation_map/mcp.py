"""Read-only stdio MCP planner. It never dispatches a business compensation."""
import json
import sys

from .planner import plan

DESCRIPTION="FR : préparer un plan conditionnel de compensation sans exécution. EN: prepare a contingent compensation plan without execution. ES: preparar un plan condicional de compensación sin ejecutarlo."


def handle(request):
    if not isinstance(request,dict) or request.get("jsonrpc")!="2.0" or not isinstance(request.get("method"),str):raise ValueError("invalid_request")
    method=request["method"];params=request.get("params",{})
    if method=="initialize":return {"protocolVersion":"2025-11-25","capabilities":{"tools":{"listChanged":False}},"serverInfo":{"name":"agent-compensation-map","version":"0.1.0-alpha.1"},"instructions":DESCRIPTION}
    if method=="ping":return {}
    if method=="tools/list":return {"tools":[{"name":"compensation_plan","description":DESCRIPTION,"inputSchema":{"type":"object","properties":{"case":{"type":"object"}},"required":["case"],"additionalProperties":False},"annotations":{"readOnlyHint":True,"destructiveHint":False,"idempotentHint":True,"openWorldHint":False}}]}
    if method=="tools/call":
        if not isinstance(params,dict) or params.get("name")!="compensation_plan" or not isinstance(params.get("arguments"),dict):raise ValueError("invalid_tool")
        result=plan(params["arguments"]["case"])
        return {"content":[{"type":"text","text":json.dumps(result,ensure_ascii=False)}],"structuredContent":result,"isError":False}
    raise LookupError("unknown_method")


def serve():
    while True:
        line=sys.stdin.readline(200001)
        if not line:return
        request=None
        try:
            if len(line)>200000:raise ValueError("invalid_size")
            request=json.loads(line)
            if isinstance(request,dict) and "id" not in request:continue
            result=handle(request)
            response={"jsonrpc":"2.0","id":request.get("id"),"result":result}
        except (ValueError,KeyError,TypeError,LookupError):
            response={"jsonrpc":"2.0","id":request.get("id") if isinstance(request,dict) else None,"error":{"code":-32602,"message":"Entrée non valide / Invalid input / Entrada no válida"}}
        print(json.dumps(response,ensure_ascii=False),flush=True)
