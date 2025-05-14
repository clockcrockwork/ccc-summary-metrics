#!/usr/bin/env python3
"""月次CSVをローテートし、日平均を計算して年次ファイルに追記"""
import pandas as pd
import gzip
import shutil
import pathlib
import datetime as dt

# メトリクス格納ディレクトリ
ROOT = pathlib.Path.cwd() / "metrics"

# 対象月 = 当日から見て3か月前の月初
month = (
    dt.date.today().replace(day=1)
    - dt.timedelta(days=1)
).replace(day=1)

def process_csv(prefix: str):
    """
    prefix: 'system_metrics' または 'container_metrics'
    prefix-YYYY-MM.csv を処理する
    """
    name = f"{prefix}-{month:%Y-%m}.csv"
    raw = ROOT / name
    if not raw.exists():
        print(f"No target CSV: {raw}")
        return

    print(f"Rolling {raw}")
    # ヘッダー付きCSVを読み込み
    df = pd.read_csv(raw, parse_dates=["timestamp"])

    # 日平均を計算
    if prefix == "system_metrics":
        # 全数値列を日次平均
        daily = (
            df.set_index("timestamp")
              .resample("1D")
              .mean()
              .dropna()
        )
    else:
        # コンテナ毎に日次平均
        daily = (
            df.set_index("timestamp")
              .groupby("container_name")
              .resample("1D")
              .mean()
              .dropna()
        )
        # フォーマットのためインデックスをリセット
        daily = daily.reset_index()

    # 日次データ保存先ディレクトリ
    daily_dir = ROOT / "daily" / prefix
    daily_dir.mkdir(parents=True, exist_ok=True)
    daily_file = daily_dir / f"{month:%Y}.csv"

    # 年次ファイルに追記
    # system_metrics はインデックス(timestamp)を含めて出力、container_metrics は index=False
    daily.to_csv(
        daily_file,
        mode="a",
        header=not daily_file.exists(),
        index=(prefix == "system_metrics")
    )

    # 元CSVをgzip圧縮して削除
    with open(raw, "rb") as f_in,
         gzip.open(f"{raw}.gz", "wb", compresslevel=9) as f_out:
        shutil.copyfileobj(f_in, f_out)
    raw.unlink()
    print(f"Rotated & gzipped {raw}")

# system と container の両方を順次処理
def main():
    for prefix in ["system_metrics", "container_metrics"]:
        process_csv(prefix)

if __name__ == "__main__":
    main()
