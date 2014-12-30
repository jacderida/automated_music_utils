#!/usr/bin/env python
import argparse
import sys


def main():
    driver = CliDriver()
    return driver.main()

class CliDriver(object):
    def main(self):
        parser = argparse.ArgumentParser()
        subparsers = parser.add_subparsers(dest='command')
        subparsers.add_parser('rip', help='rips the current CD to WAV')
        search_parser = subparsers.add_parser('search', prog='search', help='performs a very simple search on discogs')
        search_parser.add_argument('term', help='the term to search for')
        encode_parser = subparsers.add_parser('encode', help='encodes a CD or a set of WAV files to mp3')
        encode_parser.add_argument('source', choices=['cd', 'wav'], help='the source to encode from')
        encode_parser.add_argument('releaseid', type=int, help='the ID of the discogs release')
        args = parser.parse_args()
        print(args)
        return 0

if __name__ == '__main__':
    sys.exit(main())
