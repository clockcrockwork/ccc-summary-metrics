#!/usr/bin/env python3
import pandas as pd, gzip, shutil, pathlib, datetime as dt

ROOT = pathlib.Path.cwd() / "metrics"

# 対象月 = 当日から見て3か月前
month = (dt.date.today().replace(day=1) - dt.timedelta(days=1)).replace(day=1)
name = f"{month:%Y-%m}.csv"
raw = ROOT / name
if not raw.exists():
    print("No target CSV", raw)
    exit(0)

# 日平均へ
print("Rolling", raw)
df = pd.read_csv(raw, names=["ts","cpu","mem","swap"], parse_dates=["ts"], date_unit="s")
daily = df.set_index("ts").resample("1D").mean().dropna()

daily_file = ROOT / "daily" / f"{month:%Y}.csv"
daily.to_csv(daily_file, mode="a", header=not daily_file.exists())

# gzip 元CSV
with open(raw, "rb") as f_in, gzip.open(f"{raw}.gz", "wb", compresslevel=9) as f_out:
    shutil.copyfileobj(f_in, f_out)
raw.unlink()
print("Rotated & gzipped", raw)