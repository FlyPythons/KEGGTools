#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import logging
import string
import sys

from common import __version__, __email__, __author__


LOG = logging.getLogger(__name__)
__all__ = []


def read_kegg_org(file):
    """
    read br08610.keg
    :param file:
    :return:
    """
    r = {}

    taxon = ""
    level = "A"
    levels = {k: n for n, k in enumerate(string.ascii_uppercase)}

    for line in open(file):
        line = line.strip()

        tag = line[0]

        if tag not in levels:
            continue

        if "TAX:" in line:
            taxon = line.split("TAX:")[-1].split("]")[0]
            level = tag
            continue

        if levels[tag] - levels[level] == 1:
            if taxon:
                # print("%s\t %s" % (line.split()[1], taxon))
                org = line.split()[1]

                if not org.isdigit():
                    r[org] = taxon
        else:
            taxon = ""

    return r


def read_taxon(file):

    r = {}

    for line in open(file):

        if line.startswith("#"):
            continue

        line = line.rstrip("\n")
        taxon_id = line.split()[0]
        r[taxon_id] = line

    return r


def org2taxon(org, taxon):

    r = {}

    LOG.info("reading KEGG Organisms taxon from %r" % org)
    org = read_kegg_org(org)
    LOG.info("reading NCBI taxon ranks from %r" % taxon)
    taxon = read_taxon(taxon)

    LOG.info("process KEGG Organisms ranks")
    for o, t in org.items():

        if t in taxon:
            r[o] = taxon[t]
        else:
            LOG.info("taxon_id %r not in taxon file" % t)

    return r


def set_args():
    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:
    Get KEGG organism ranks by taxon id

version: %s
author:  %s
email: %s
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--keg", required=True, help="The htex file of KEGG Organisms in the NCBI Taxonomy, usually named as 'br08610.keg'")
    args.add_argument("--taxon", required=True, help="NCBI Taxonomy file, taxon_id, rank information separated with tab")
    args.add_argument("--out", default="KEGG.ranks", help="output file")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()

    org_dict = org2taxon(args.keg, args.taxon)

    LOG.info("output result to %r" % args.out)

    with open(args.out, "w") as fh:

        for k, v in sorted(org_dict.items()):
            fh.write("%s\t%s\n" % (k, v))


if __name__ == "__main__":
    main()

