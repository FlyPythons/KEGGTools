#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import argparse
import os.path
import logging
import sys
import time
from multiprocessing import Pool

from common import read_org, __author__, __email__, __version__


LOG = logging.getLogger(__name__)


def download(org, status, output_dir):
    """
    download proteins from NCBI according to KEGG organism url
    :param org: [organism abbr., organism name, url]
    :param status: download status, m/n
    :param output_dir: output directory
    :return: 0
    """

    time.sleep(2)

    o, name, url = org
    LOG.info("%s get %s proteins from %r" % (status, o, url))
    url = "%s/%s_translated_cds.faa.gz" % (url, url.split("/")[-1])
    file = urllib.request.urlopen(url)
    out_file = os.path.join(output_dir, "%s.pep.fasta.gz" % o)

    if not os.path.exists(out_file):

        with open(out_file, "wb") as out:
            out.write(file.read())

    return 0


def get_proteins(orgs, output_dir, concurrent=1):
    """
    download proteins from NCBI use multiprocessing
    :param orgs: org list read from .org
    :param output_dir: output directory
    :param concurrent: max concurrent process to download
    :return: 0
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pool = Pool(processes=concurrent)
    results = []
    num = len(orgs)

    for n, org in enumerate(orgs):

        index = "%s/%s" % (n + 1, num)
        results.append(pool.apply_async(download, (org, index, output_dir)))

    pool.close()
    pool.join()

    returns = []

    for i, result in enumerate(results):
        returns.append(result.get())

    fail = [i for i in returns if i != 0]
    LOG.info("%s success, %s failed" % (len(orgs)-len(fail), len(fail)))

    return 0


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
download protein sequences of KEGG organism from NCBI.

version: %s
contact: %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--org", metavar="FILE", required=True, help=".org file created by download_organism.py")
    args.add_argument("--out", metavar="DIR", default=".", help="output directory (default: current directory)")
    args.add_argument("--concurrent", metavar="INT", type=int,
                      default=1, help="number of download processes concurrent (default: 1)")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    args = set_args()

    orgs = read_org(args.org)

    allowed_orgs = []

    for org in orgs:

        if len(org) != 3:
            LOG.info("record %r has no url, skip" % org)
            continue

        o, name, url = org

        if "ftp.ncbi.nlm.nih.gov" not in url:
            LOG.info("record %r not in NCBI, skip" % org)
            continue

        allowed_orgs.append(org)

    LOG.info("%s records pass, downloading..." % len(allowed_orgs))
    get_proteins(allowed_orgs, args.out, args.concurrent)


if __name__ == "__main__":
    main()

