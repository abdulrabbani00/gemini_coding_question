#!/usr/local/bin/python3
"""
[Alerts setup for symbols]

"""
import argparse
import logging
import requests
import numpy as np

logger = logging.getLogger(__name__)

def _set_logger(output_type):
    """[SetUp Logging]
    This function will allow users the capability to specify
    if they want the logging to be plain text (default) or in json

    Args:
        output_type ([str]): [Either default or json]

    Returns:
        [logging.Logger]: [Logging type]
    """
    logger.setLevel(logging.INFO)

    if output_type == 'default':
        plain_handler=logging.StreamHandler()
        plain_formatter=logging.Formatter(
            '%(asctime)-s - %(alert_type)s - %(levelname)-s - %(message)s')
        plain_handler.setFormatter(plain_formatter)
        logger.addHandler(plain_handler)
    elif output_type == 'json':
        json_handler=logging.StreamHandler()
        json_formatter=logging.Formatter(
            "{'time':'%(asctime)s', 'alert_type': '%(alert_type)s', \
            'level': '%(levelname)s', 'message': '%(message)s'}"
        )
        json_handler.setFormatter(json_formatter)
        logger.addHandler(json_handler)

    return logger

def call_argprase():
    """[Wrapper function for argparse]

    Returns:
        [argparse.Namespace]: [arg object]
    """
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('-t','--type', nargs='+', help='The type of check to run, or ALL',
                           choices=["pricedev", "pricechange" ,"voldev", "ALL"],
                           default='ALL')
    my_parser.add_argument('-c','--currency', nargs='+', action='store',
                           help="The currency trading pair, or ALL", default='ALL')
    my_parser.add_argument('-l', '--log_format', action='store', choices=['default', 'json'],
                           help='The format of the logging, do you want json or plain text',
                           default='default')

    args = my_parser.parse_args()

    return args


def _query_api(endpoint, base="https://api.gemini.com"):
    """[Reusable function to query gemini's api]

    Args:
        endpoint ([str]): [Specific endpoint to use for the call]
        base (str, optional): [Base URL]. Defaults to "https://api.gemini.com".

    Returns:
        [dict or list]: [Return from the API query]
    """
    return requests.get(base + endpoint).json()


def outside_standard_dev(cur_price, symbol, price_array):
    """[Figure out if the current price is outside the standard deviations]

    Args:
        cur_price ([float]): [The current price]
        symbol ([str]): [Name of the symbol]
        price_array ([list]): [list of prices over the last 24 hours]
    """
    num_array = np.array(price_array)
    stand_dev = np.std(num_array)
    mean = np.mean(num_array)
    upper_limit = mean + stand_dev
    lower_limit = mean - stand_dev

    logger.info("Mean for %s: %s", symbol, mean)
    logger.info("Standard Deviation for %s: %s" ,symbol, stand_dev)

    if cur_price < lower_limit:
        logger.error("Outside the lower limit (%s) by %s", lower_limit, (lower_limit - cur_price))
        logger.error("%s current price %s outside standard deviation", symbol, cur_price)
        logger.error("******   Price Deviation")
    if cur_price > upper_limit:
        logger.error("Outside the upper limit (%s) by %s", upper_limit, (cur_price - upper_limit))
        logger.error("%s current price %s outside standard deviation", symbol, cur_price)
        logger.error("******   Price Deviation")

def call_pricedev(symbols_to_check):
    """[Run the pricedev type]

    Args:
        symbols_to_check ([list]): [List of symbols to check to see if they are
        1 standard deviation]
    """
    for symbol in symbols_to_check:
        logger.info("Checking: %s", symbol)
        sym_info = _query_api(f"/v2/ticker/{symbol}")
        try:
            change_array = list(map(float, sym_info['changes']))
            outside_standard_dev(float(sym_info['close']), symbol, change_array)
        except KeyError:
            logger.warning("Unable to get correct info for: %s", symbol)
            logger.debug("Symbol Reponse: %s", sym_info)

def main():
    """[Run all checks]
    """
    args = call_argprase()
    global logger
    logger = _set_logger(args.log_format)
    logger = logging.LoggerAdapter(logger, {'alert_type':'AlertingTool'})

    logger.debug("Arguments passed in: %s", args)


    if "ALL" in args.currency:
        logger.info("Getting all instruments")
        symbols = _query_api("/v1/symbols")
        logger.debug("Instrument list: %s", symbols)
    else:
        symbols = args.currency
        logger.info("Using following instruments: %s", symbols)

    if "ALL" in args.type or "pricedev" in args.type:
        call_pricedev(symbols)

if __name__ == '__main__':
    main()
