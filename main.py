from utils import (
    load_orders,
    clean_types,
    clean_items_html,
    fill_coupon_used,
    add_order_month,
    add_high_value_order,
    add_country_rating_mean,
    filter_orders,
    add_delivery_status,
)


def main():
    df = load_orders("orders_simple.json")
    df = clean_types(df)
    df = clean_items_html(df)
    df = fill_coupon_used(df)
    df = add_order_month(df)
    df = add_high_value_order(df)
    df = add_country_rating_mean(df)
    df = filter_orders(df)
    df = add_delivery_status(df)
    df.to_csv("clean_orders_[209700798].csv", index=False)
    print(df)


if __name__ == "__main__":
    main()
