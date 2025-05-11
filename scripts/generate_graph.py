#!/usr/bin/env python3
"""metrics JSON から 24h グラフを生成"""
import json, sys, matplotlib.pyplot as plt, datetime as dt

src, out = sys.argv[1:3]
with open(src) as f:
    data = json.load(f)

# TSV型: [{'ts': 1715088000, 'cpu': 12.3, ...}, ...]
xs = [dt.datetime.fromtimestamp(d['ts']) for d in data[-288:]]  # 5分粒度×24h
cpu = [d['cpu'] for d in data[-288:]]
mem = [d['mem'] for d in data[-288:]]

plt.figure(figsize=(12,4))
plt.plot(xs, cpu, label='CPU %')
plt.plot(xs, mem, label='Memory %')
plt.legend()
plt.tight_layout()
plt.savefig(out, dpi=120)