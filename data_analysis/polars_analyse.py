import polars as pl

pl.read_csv("/Users/bhuvanshree/ml/radiation_tracker/data/fully_sorted.csv").write_parquet("radiation_data.parquet")

df = (
    pl.read_parquet("radiation_data.parquet", low_memory=True)
    .lazy()
    .with_columns([
        pl.col("Captured Time").str.strptime(pl.Datetime, fmt="%Y-%m-%d %H:%M:%S").alias("captured_ts")
    ])
    .filter(pl.col("captured_ts").is_not_null())
    .with_columns([
        pl.col("captured_ts").dt.truncate("1m").alias("hour_bucket")
    ])
    .groupby("hour_bucket")
    .agg(pl.count().alias("count"))
    .sort("hour_bucket")
)


result = df.collect()
print(result.head())