#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import logging
import urllib.request
import argparse

from common import __author__, __version__, __email__


LOG = logging.getLogger(__name__)


def html2org(url="http://www.kegg.jp/kegg/catalog/org_list.html"):
    """
    request KEGG organism url and get the organism abb. name and download url
    :param url: the url of KEGG organism, default is http://www.kegg.jp/kegg/catalog/org_list.html
    :param out: the output
    :return: dict contain org information
    """

    r = {}

    LOG.info("open url %r to get KEGG org list" % url)
    file = urllib.request.urlopen(url)

    org = name = link = ""
    n = 0

    for line in file:
        line = line.decode("utf-8").strip()

        if "show_organism?org=" in line:

            if org:
                r[org] = [name, link]

            org = line.split("</a>")[0].split("'>")[-1]
            name = link = ""
            n = 1
            continue

        if n == 1:
            name = line.split("</a>")[0].split("'>")[-1]
            n = 2
            continue
        if n == 2:
            if "ftp://" not in line:
                continue
            link = line.split("href='")[-1].split("'>")[0]
            n = 0

    if org:
        r[org] = [name, link]

    LOG.info("get %s records from KEGG org" % len(r))

    return r


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:
    Download KEGG organism information from KEGG website.
    The result consists organism abbr., organism name and source url

version: %s
author:  %s
email: %s
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--url", default="http://www.kegg.jp/kegg/catalog/org_list.html", help="KEGG organism url")
    args.add_argument("--out", default="KEGG.org", help="output filename")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()
    org_dict = html2org(args.url)

    LOG.info("output records to %s" % args.out)

    with open(args.out, "w") as fh:
        for k, v in sorted(org_dict.items()):
            fh.write("%s\t%s\t%s\n" % (k, v[0], v[1]))


if __name__ == "__main__":
    main()

