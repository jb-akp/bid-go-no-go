"""python -m bidgo run data/opportunities/<name> | run-all | approve <name> --by NAME --decision GO --note ..."""
import argparse

from .pipeline import DECISIONS, OPPS, approve, run


def report(package):
    result, _ = run(package)
    print(f"{result['name']}: {result['decision']}  -> out/{result['name']}.md")
    for r in result["reasons"]:
        print(f"  - {r['check']}: {r['detail']}  [{', '.join(c['id'] for c in r['cites'])}]")


def main(argv=None):
    p = argparse.ArgumentParser(prog="bidgo", description="Bid go / no-go review with cited reasons.")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run").add_argument("package")
    sub.add_parser("run-all")
    a = sub.add_parser("approve")
    a.add_argument("name")
    a.add_argument("--by", required=True)
    a.add_argument("--decision", required=True, choices=DECISIONS)
    a.add_argument("--note", default="")
    args = p.parse_args(argv)

    if args.cmd == "run":
        report(args.package)
    elif args.cmd == "run-all":
        for package in sorted(d for d in OPPS.iterdir() if d.is_dir()):
            report(package)
    else:
        e = approve(args.name, args.by, args.decision, args.note)
        tag = f"override of {e['recommended']}" if e["override"] else "approved as recommended"
        print(f"{e['opportunity']}: {e['decision']} ({tag}) by {e['by']} -> out/approvals.jsonl")


if __name__ == "__main__":
    main()
