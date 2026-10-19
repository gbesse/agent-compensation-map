import json
from pathlib import Path
import sys

from .planner import plan

ROOT=Path(__file__).resolve().parent
MESSAGES={"fr":{"help":"Utilisation : python -m compensation_map demo|plan dossier.json|mcp|serve [port] [--lang fr|en|es]","error":"Entrée non valide","ready":"Laboratoire de compensation local"},"en":{"help":"Usage: python -m compensation_map demo|plan case.json|mcp|serve [port] [--lang fr|en|es]","error":"Invalid input","ready":"Local compensation laboratory"},"es":{"help":"Uso: python -m compensation_map demo|plan caso.json|mcp|serve [puerto] [--lang fr|en|es]","error":"Entrada no válida","ready":"Laboratorio de compensación local"}}


def example():return json.loads((ROOT/"examples/ambiguous-charge.json").read_text())


def main(argv=None):
    args=list(sys.argv[1:] if argv is None else argv);lang="en"
    try:
        if "--lang" in args:
            i=args.index("--lang");lang=args[i+1];del args[i:i+2]
        if lang not in MESSAGES:raise ValueError("invalid_language")
        if not args or args[0] in ("help","--help"):print(MESSAGES[lang]["help"]);return 0
        command=args.pop(0)
        if command=="demo":result=plan(example())
        elif command=="plan" and len(args)==1:result=plan(json.loads(Path(args[0]).read_text()))
        elif command=="mcp":
            from .mcp import serve
            serve();return 0
        elif command=="serve":
            from .server import serve
            port=int(args[0]) if args else 8769;print(f'{MESSAGES[lang]["ready"]}: http://127.0.0.1:{port}/?lang={lang}',flush=True);serve(port);return 0
        else:raise ValueError("invalid_command")
        print(json.dumps(result,ensure_ascii=False,indent=2));return 1 if result["status"]=="requires_human_review" else 0
    except (ValueError,TypeError,KeyError,IndexError,OSError):
        print(json.dumps({"error":"invalid_input","message":MESSAGES.get(lang,MESSAGES["en"])["error"]}),file=sys.stderr);return 2


if __name__=="__main__":raise SystemExit(main())
