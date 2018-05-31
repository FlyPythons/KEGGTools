#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import argparse
import logging

from common import read_org_ko, read_org, __email__, __version__, __author__
from FastaReader import open_fasta


LOG = logging.getLogger(__name__)

__all__ = []


def process_protein(org, keg, pep, out):
    """
    get the protein seq of with ko
    :param org: the organism abbr.
    :param keg: directory contains org.keg
    :param pep: directory contains org.pep.fasta.gz
    :param out: output directory
    :return:
    """

    keg_name = os.path.join(keg, "%s00001.keg" % org)
    pep_name = os.path.join(pep, "%s.pep.fasta.gz" % org)

    if not os.path.exists(keg_name):
        LOG.info("keg %r not exists, skip" % keg_name)
        return 1

    if not os.path.exists(pep_name):
        LOG.info("pep %r not exists, skip" % pep_name)
        return 1

    gene_dict = read_org_ko(keg_name)

    if not gene_dict:
        LOG.info("keg %r is empty, skip" % keg_name)
        return 1

    fh = open(os.path.join(out, "%s.pep.fasta" % org), "w")

    for record in open_fasta(pep_name):
        name = record.name

        # gene_id is in db_xref or locus_tag

        if "locus_tag=" in name:
            id = name.split("locus_tag=")[1].split("]")[0]
        elif "db_xref=GeneID:" in name:
            id = name.split("db_xref=GeneID:")[1].split("]")[0]
        elif "protein_id=" in name:
            id = name.split("protein_id=")[1].split("]")[0].split(".")[0]
        else:
            continue

        if id in gene_dict:
            fh.write(">%s:%s\n%s\n" % (org, id, record.seq))

    fh.close()

    return 0


def process_proteins(orgs, keg, pep, out):
    """
    get the protein seq of ids in keg from pep
    :param keg:
    :param pep:
    :param out:
    :return:
    """

    num = len(orgs)

    for n, org in enumerate(orgs):
        LOG.info("%s/%s process %s" % (n+1, num, org))
        process_protein(org, keg, pep, out)

    return 0


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
description:
    get the protein of genes in keg from pep

version: %s
author:  %s
email: %s
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--org", required=True, help=".org file created by get_organism.py")
    args.add_argument("--keg", required=True, help="directory contains org00001.keg")
    args.add_argument("--pep", required=True, help="directory contains org.pep.fasta.gz")
    args.add_argument("--out", default=".", help="output directory")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()

    orgs = read_org(args.org)
    process_proteins([i[0] for i in orgs], args.keg, args.pep, args.out)


if __name__ == "__main__":
    main()

