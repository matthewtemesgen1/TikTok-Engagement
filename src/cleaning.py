import json
from typing import Tuple

import numpy as np
import pandas as pd

from utils import get_raw_path, get_processed_path


RAW_FILENAME = "trending.json"
CLEAN_FILENAME = "trending_clean.csv"


def load_raw_trending() -> pd.DataFrame:
    """
    Load the raw trending.json file and turn the 'collector' list
    into a flat pandas DataFrame.
    """
    path = get_raw_path(RAW_FILENAME)

    with open(path, "r") as f:
        raw = json.load(f)

    collector = raw["collector"]

    df = pd.json_normalize(collector)

    print(f"Loaded {len(df)} raw records from {path}")
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names:
    - lower case
    - replace spaces with underscores
    - replace dots (from json_normalize) with underscores
    """
    df = df.copy()
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace(".", "_")
    )
    return df


def rename_key_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename the most important columns to cleaner, more meaningful names.
    This will help when you write the report and build models.
    """
    df = df.copy()

    rename_map = {
        "id": "video_id",
        "text": "caption",
        "createtime": "create_time",
        "authormeta_id": "author_id",
        "authormeta_name": "author_name",
        "authormeta_nickname": "author_nickname",
        "authormeta_verified": "author_verified",
        "musicmeta_musicid": "music_id",
        "musicmeta_musicname": "music_name",
        "musicmeta_musicauthor": "music_author",
        "videometa_height": "video_height",
        "videometa_width": "video_width",
        "videometa_duration": "video_duration",
        "diggcount": "like_count",
        "sharecount": "share_count",
        "playcount": "play_count",
        "commentcount": "comment_count",
    }

    existing_renames = {
        old: new
        for old, new in rename_map.items()
        if old in df.columns
    }

    df = df.rename(columns=existing_renames)

    return df


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert important columns to appropriate types:
    - create_time: datetime
    - *_count columns: numeric
    """
    df = df.copy()

    if "create_time" in df.columns:
        df["create_time"] = pd.to_datetime(df["create_time"], unit="s", errors="coerce")

    count_cols = [
        "like_count",
        "share_count",
        "play_count",
        "comment_count",
    ]
    for col in count_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "author_verified" in df.columns:
        df["author_verified"] = df["author_verified"].astype("bool")

    return df


def handle_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Handle missing data in a simple, transparent way:
    - caption: fill missing with empty string
    - lists (hashtags, mentions): fill missing with empty list
    - numeric counts: fill missing with 0
    """
    df = df.copy()

    if "caption" in df.columns:
        df["caption"] = df["caption"].fillna("")

    for col in ["mentions", "hashtags"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: x if isinstance(x, list) else [])

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    for col in numeric_cols:
        df[col] = df[col].fillna(0)

    return df


def feature_engineering(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create initial features that you'll describe in Sprint 2:
    - caption_length: number of characters in the caption
    - hashtag_count: number of hashtags in the post
    - engagement: likes + comments + shares
    - engagement_rate: engagement divided by play_count
    """
    df = df.copy()

    # Caption length
    if "caption" in df.columns:
        df["caption_length"] = df["caption"].astype(str).str.len()

    # Number of hashtags
    if "hashtags" in df.columns:
        df["hashtag_count"] = df["hashtags"].apply(lambda x: len(x) if isinstance(x, list) else 0)

    # Engagement counts
    like = df["like_count"] if "like_count" in df.columns else 0
    comment = df["comment_count"] if "comment_count" in df.columns else 0
    share = df["share_count"] if "share_count" in df.columns else 0

    df["engagement"] = like + comment + share

    # Engagement rate: avoid division by zero
    if "play_count" in df.columns:
        df["engagement_rate"] = df["engagement"] / df["play_count"].replace(0, np.nan)
    else:
        df["engagement_rate"] = np.nan

    return df


def clean_trending_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Full cleaning pipeline:
    1 load raw json
    2 standardize columns
    3 rename key columns
    4 convert types
    5 handle missing data
    6 feature engineering
    7 save cleaned CSV

    Returns (raw_df, clean_df)
    """
    df_raw = load_raw_trending()
    print("Original shape:", df_raw.shape)

    df = standardize_columns(df_raw)
    df = rename_key_columns(df)
    df = convert_types(df)
    df = handle_missing_data(df)
    df = feature_engineering(df)

    print("Cleaned shape:", df.shape)

    out_path = get_processed_path(CLEAN_FILENAME)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False)
    print(f"Saved cleaned data to {out_path}")

    return df_raw, df


if __name__ == "__main__":
    clean_trending_data()