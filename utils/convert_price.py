def convert_price(price_decimal):
    price_int = int(price_decimal)
    return "{:,}".format(price_int)
