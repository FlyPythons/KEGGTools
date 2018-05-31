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
    download .keg file contains KO information from KEGG
    :param org: KEGG organism abbr.
    :param status: the download status
    :param output_dir: output directory
    :return: 0
    """

    time.sleep(2)

    LOG.info("%s processing %s" % (status, org))
    id = org + "00001.keg"
    out_file = os.path.join(output_dir, id)

    if os.path.exists(out_file):
        LOG.info("%s has been downloaded before, skip")
        return 0

    file = urllib.request.urlopen("http://www.kegg.jp/kegg-bin/download_htext?htext=%s&format=htext&filedir=" % id)

    if not file.read():
        LOG.warning("%s has no KO file" % org)
        return org
    else:
        with open(out_file, "wb") as out:
            out.write(file.read())

    return 0


def download_ko(orgs, output_dir, concurrent=1):

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

    fail = [i for i in returns if i]
    LOG.info("%s records, %s failed! Here are they!" % (len(orgs), len(orgs)-len(fail)))

    print("\n".join(fail))

    return 0


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
download all KEGG Orthology (KO) of KEGG organisms.

version: %s
contact: %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--org", metavar="FILE", required=True,
                      help="a list of KEGG organism abbr. at the first column")
    args.add_argument("--out", metavar="DIR",
                      default=".", help="output directory (default: current directory)")
    args.add_argument("--concurrent", metavar="INT", type=int,
                      default=5, help="number of processes concurrent (default: 1)")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )
    args = set_args()

    orgs = read_org(args.org)
    LOG.info("download .keg from KEGG")
    download_ko([i[0] for i in orgs], args.out, args.concurrent)


if __name__ == "__main__":
    main()

