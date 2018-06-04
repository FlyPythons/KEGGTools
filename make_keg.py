#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from common import __author__, __email__, __version__

LOG = logging.getLogger(__name__)

__all__ = []


def read_tbl(file):
    """
    read table
    :param file:
    :return:
    """

    for line in open(file):
        line = line.strip()

        if line.startswith("#") or not line:
            continue

        yield line.split("\t")


def cluster_protein(file):
    """
    cluster protein by pathway and ko
    :param file: kegg annotation result consist protein id, ko and pathways joined with "\t"
    :return: dict {pathway: {ko: [proteins]}}
    """
    path_dict = {}
    LOG.info("reading kegg result from '%r'" % file)

    for protein, ko, pathway in read_tbl(file):
        paths = pathway.split(";")

        for path in paths:
            if path not in path_dict:
                path_dict[path] = {}

            if ko not in path_dict[path]:
                path_dict[path][ko] = []

            path_dict[path][ko].append(protein)

    return path_dict


def output_keg(keg, path_dict, output):
    """
    output .keg by kegg annotation result
    :param keg: ko00001.keg
    :param path_dict: see function cluster_protein
    :param output: output file
    :return: 0
    """
    path_id = ""

    LOG.info("output kegg map to '%r'" % output)
    fh = open(output, "w")

    for line in open(keg):
        line = line.strip()

        if not line:
            continue

        tag = line[0]

        if tag == "C":
            path_id = "ko" + line.split()[1]
            fh.write("%s\n" % line)
            continue
        elif tag == "D":

            if path_id not in path_dict:
                continue

            mess = line.split()
            ko = mess[1]
            name = " ".join(mess[2:])

            if ko not in path_dict[path_id]:
                continue

            for p in path_dict[path_id][ko]:

                if ko == "-":
                    fh.write("D      %s\t\n" % p)
                else:
                    fh.write("D      %s\t%s %s\n" % (p, ko, name))
        else:
            fh.write("%s\n" % line)

    return 0


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
create .keg file from kegg annotation result

version: %s
contact: %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--keg", metavar="FILE", required=True,
                      help="KO file downloaded from KEGG, usually named 'ko00001.keg'")
    args.add_argument("--in", metavar="FILE", dest="input", required=True,
                      help="KEGG annotation result consist protein id, KO, pathway joined with '\t'")
    args.add_argument("--out", metavar="STR", default="out", help="output prefix (default: out)")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()

    path_dict = cluster_protein(args.input)
    output_keg(args.keg, path_dict, args.out+".keg")


if __name__ == "__main__":
    main()

