#!/usr/bin/env python3
"""metrics CSV から 24h グラフを生成"""
import pandas as pd
import sys
import matplotlib.pyplot as plt
import datetime as dt

# 引数: CSV入力パス, 出力PNGパス
src, out = sys.argv[1:3]

df = pd.read_csv(src, names=["ts", "cpu", "mem", "swap"]).dropna()
if df.empty:
    print("[WARN] CSV is empty. Skipping plot.")
    sys.exit(0)

# タイムスタンプを datetime に変換
df["ts"] = pd.to_datetime(df["ts"], unit="s")

# 最新24h分 (5分間隔×288行) を切り出し
latest = df.tail(288)

plt.figure(figsize=(12, 4))
plt.plot(latest["ts"], latest["cpu"], label="CPU %")
plt.plot(latest["ts"], latest["mem"], label="Memory %")
plt.legend()
plt.tight_layout()
plt.savefig(out, dpi=120)