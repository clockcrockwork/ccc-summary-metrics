#!/usr/bin/env python3
"""CSV metrics から 24h グラフを生成"""
import csv
import sys
import matplotlib.pyplot as plt
import datetime as dt

# コマンドライン引数: 入力CSVファイルパス, 出力画像ファイルパス
src, out = sys.argv[1:3]

# CSV読み込み
with open(src) as f:
    reader = csv.DictReader(f)
    data = list(reader)

# 最新 24h（5分粒度×288点）を抽出
last_288 = data[-288:]

# 時系列と CPU%, Memory% をそれぞれ取得
xs  = [dt.datetime.fromisoformat(d['timestamp']) for d in last_288]
cpu = [float(d['cpu_used_pct'])           for d in last_288]
mem = [float(d['mem_used_pct'])           for d in last_288]

# グラフ作成
plt.figure(figsize=(12, 4))
plt.plot(xs, cpu, label='CPU %')
plt.plot(xs, mem, label='Memory %')
plt.legend()
plt.tight_layout()

# 画像保存
plt.savefig(out, dpi=120)
