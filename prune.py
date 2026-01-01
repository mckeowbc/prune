#!/usr/bin/env python3

import argparse
import pathlib
import datetime
import pprint


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--days', type=int, default=7)
    p.add_argument('--weeks',type=int, default=3)
    p.add_argument('--months',type=int, default=11)
    p.add_argument('--years',type=int, default=1)
    p.add_argument('--dry-run', default=False,action='store_true')
    p.add_argument('directory',type=pathlib.Path)

    args = p.parse_args()

    d = args.directory

    f_list = []

    for f in d.iterdir():
        if not f.is_file():
            continue
        f_list.append((f.stat().st_ctime, f))


    keep = {
        'days'   : {},
        'weeks'  : {},
        'months' : {},
        'years'  : {},
    }

    for f in sorted(f_list, key=lambda x : x[0], reverse=True):
        dt = datetime.datetime.fromtimestamp(f[0])
        if len(keep['days']) < args.days:
            day = dt.strftime("%Y%j")
            if day not in keep['days']:
                keep['days'][day] = f[1]    
        elif len(keep['weeks']) < args.weeks:
            week = dt.strftime("%Y%U")
            if week not in keep['weeks']:
                keep['weeks'][week] = f[1]    
        elif len(keep['months']) < args.months:
            month = dt.strftime("%Y%m")
            if month not in keep['months']:
                keep['months'][month] = f[1]    
        elif len(keep['years']) < args.years:
            year = dt.strftime("%Y")
            if year not in keep['years']:
                keep['years'][year] = f[1]

    keep_set = set(p for td in keep.keys()
                        for p in keep[td].values())
    for f in f_list:
        if f[1] not in keep_set:
            print(f"Removing {f[1]}")
            if not args.dry_run:
                f[1].unlink()