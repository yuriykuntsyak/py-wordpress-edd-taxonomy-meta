#!/usr/bin/env python3

import pymysql


from utils import *

def main():
    # to do:
    # - accept cli args
    # - add const file
    # - read config (credentials etc.) from file
    # - add logging on file
    # - get date of the products to work on
    # - get metadata for the media files (images) related to the specified date
    # - check if the related products have the correct taxonomy
    #   if false, create (if doesn't exist) and add it to the product

    db = pymysql.connect("address", "user", "psw", "db")


if __name__ == "__main__":
    main()