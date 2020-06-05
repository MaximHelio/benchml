#! /usr/bin/env python
import benchml
import optparse
import json
from benchml.transforms import *
log = benchml.log
benchml.readwrite.configure(use_ase=False)

def main(args):
    # Load datasets (as iterator)
    benchml.splits.synchronize(args.seed)
    data = benchml.data.compile(
        root=args.data_folder,
        filter_fct=benchml.filters[args.filter])
    # Compile models
    models = benchml.models.compile(args.groups)
    # Evaluate
    bench = benchml.benchmark.evaluate(
        data, models, log, verbose=args.verbose)
    json.dump(bench, open(args.output, "w"), indent=1, sort_keys=True)

if __name__ == "__main__":
    log.Connect()
    log.AddArg("data_folder", typ=str, default="", help="Dataset folder")
    log.AddArg("groups", typ=(list,str), default=[], help="Model groups")
    log.AddArg("filter", typ=str, default="none", help="Dataset filter regex")
    log.AddArg("output", typ=str, default="bench.json", help="Output json")
    log.AddArg("seed", typ=int, default=0, help="Global random seed")
    log.AddArg("verbose", typ=bool, default=False, help="Toggle verbose output")
    log.AddArg("list_transforms", typ=bool, default=False, help="List available transforms and quit")
    args = log.Parse()
    print(args.groups)
    if args.list_transforms:
        benchml.transforms.list_all(verbose=args.verbose)
        log.okquit()
    main(args)

