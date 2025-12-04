import re

import numpy as np
import pandas as pd


def load_orders(path: str) -> pd.DataFrame:
    return pd.read_json(path)


# 1
def clean_types(df: pd.DataFrame) -> pd.DataFrame:
    df['total_amount'] = pd.to_numeric(df.total_amount.astype(str) \
                                       .str.replace('$', ''))
    df["order_date"] = pd.to_datetime(df.order_date)
    return df


# 2
def clean_items_html(df: pd.DataFrame) -> pd.DataFrame:
    df['items_html'] = df['items_html'].apply(_remove_html_tags_regex)
    return df


# 3
def fill_coupon_used(df: pd.DataFrame) -> pd.DataFrame:
    df['coupon_used'] = df.coupon_used.astype(str) \
        .replace('', 'no coupon')
    return df


# 4
def add_order_month(df: pd.DataFrame) -> pd.DataFrame:
    df = df.assign(order_month=lambda x: x["order_date"].dt.month.astype(int))
    return df


# 5
def add_high_value_order(df: pd.DataFrame) -> pd.DataFrame:
    total_amount_mean = df["total_amount"].mean()
    df = df.assign(
        high_value_order=lambda x: x["total_amount"] > total_amount_mean)
    return df


# 6
def add_country_rating_mean(df: pd.DataFrame) -> pd.DataFrame:
    df["country_rating_mean"] = (
        df.groupby("country")["rating"].transform("mean"))
    return df


# 8
def filter_orders(df: pd.DataFrame) -> pd.DataFrame:
    df.query("total_amount > 1000 and rating > 4.5")
    return df


# 9
def add_delivery_status(df: pd.DataFrame) -> pd.DataFrame:
    df = df.assign(delivery_status=lambda x: np.where(x.shipping_days > 7, 'delayed', 'on time'))
    return df


def _remove_html_tags_regex(text):
    clean_text = re.sub('<[^<]+?>', ' ', str(text))
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text
