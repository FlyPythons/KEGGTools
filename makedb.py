#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os.path
import sys
import argparse
import logging

from common import read_org, read_org_ko, __email__, __version__, __author__


LOG = logging.getLogger(__name__)


__all__ = []


def cat_proteins(org, pep, keg, out):

    pep_out = open(out+".pep.fasta", "w")
    ko_out = open(out+".pep2ko.txt", "w")
    num = len(org)

    for n, o in enumerate(set(org)):
        LOG.info("%s/%s process %s" % (n+1, num, o))
        pep_file = os.path.join(pep, "%s.pep.fasta" % o)
        keg_file = os.path.join(keg, "%s00001.keg" % o)

        if os.path.exists(pep_file) and os.path.exists(keg_file):
            pep_out.write(open(pep_file).read())

            for k, v in read_org_ko(keg_file).items():
                ko_out.write("%s\t%s\t%s\n" % (k, ";".join(v["ko"]), ";".join(v["path"])))
        else:
            LOG.warning("%r has no .keg or .pep.fasta")

    pep_out.close()
    ko_out.close()

    return 0


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:
    extract protein of KEGG organisms you wanted to make database

version: %s
author:  %s
email: %s
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--org", required=True, help="file contains KEGG organisms abbr.")
    args.add_argument("--pep", required=True, help="directory contains KEGG proteins")
    args.add_argument("--keg", required=True, help="directory contains KEGG KO files")
    args.add_argument("--out", default="kegg", help="output prefix")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()

    orgs = read_org(args.org)

    cat_proteins([i[0] for i in orgs], args.pep, args.keg, args.out)


if __name__ == "__main__":
    main()

