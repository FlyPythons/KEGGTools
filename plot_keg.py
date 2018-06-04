#!/usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import logging
import sys
from collections import OrderedDict

from common import __author__, __email__, __version__

LOG = logging.getLogger(__name__)

__all__ = []


def stat_keg(keg):
    """
    read pathway information from .keg
    :param keg: .keg file
    :return: a dict {pathway_A: {pathway_B: [proteins]}}
    """

    r = OrderedDict()
    LOG.info("reading kegg map from %r" % keg)

    path1 = ""
    path2 = ""

    for line in open(keg):
        line = line.strip()

        if not line:
            continue

        tag = line[0]

        if tag == "A" and "<b>" in line:
            path1 = line[4:-4]
            r[path1] = OrderedDict()
            continue

        if tag == "B" and "<b>" in line:
            path2 = line[6:-4]
            r[path1][path2] = []
            continue

        if tag == "D":
            r[path1][path2].append(line.split()[1])

    return r


def plot_keg(keg_dict, out):
    """
    plot function
    :param keg_dict: see stat_keg
    :param out: output filename
    :return: 0
    """
    x = []
    y = []
    n = 1

    for path1 in keg_dict:
        x.append(n)
        y.append(0)
        n += 1

        for path2 in keg_dict[path1]:
            num = len(set(keg_dict[path1][path2]))

            if not num:
                continue

            x.append(n)
            y.append(num)
            n += 1

    y_max = max(y) * 1.1

    colors = []
    color = ["", "blue", "green", "red", "purple", "skyblue", "orange", "gray"]
    lv = 0
    n = 1

    LOG.info("plot KEGG annotation result to %r" % out)
    from matplotlib import pyplot as plt

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, )

    for path1 in keg_dict:

        colors.append("white")
        lv += 1
        ax.text(y_max / -1.7, n, path1, fontsize=8, verticalalignment='center', horizontalalignment='left', family="Arial",
                color=color[lv])
        n += 1

        for path2 in keg_dict[path1]:

            num = len(set(keg_dict[path1][path2]))

            if not num:
                continue

            ax.text(num, n, num, fontsize=8, verticalalignment='center', family="Arial",)
            ax.text(y_max / -1.8, n, path2, fontsize=8, verticalalignment='center', horizontalalignment='left', family="Arial",
                    color=color[lv])
            colors.append(color[lv])
            n += 1

    ax.barh(x, y, color=colors, alpha=0.5)
    ax.set_xlim([y_max / -100, y_max])
    ax.set_ylim([0, ax.get_ylim()[1]])
    plt.xticks(fontsize=8, family="Arial",)
    ax.set_yticks([])
    plt.subplots_adjust(top=0.95, left=0.35, right=0.95, bottom=0.05)
    plt.xlabel("Number of Genes", fontsize=10, family="Arial",)

    ax.invert_yaxis()
    plt.savefig(out)

    return 0


def set_args():

    args = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                   description="""
plot kegg annotation from .keg

version: %s
contact: %s <%s>\
    """ % (__version__, " ".join(__author__), __email__))

    args.add_argument("--keg", metavar="FILE", required=True,
                      help="KO file named '*.keg', can be make by make_keg.py")
    args.add_argument("--out", metavar="STR", default="out", help="output prefix (default: out)")

    return args.parse_args()


def main():

    logging.basicConfig(
        stream=sys.stderr,
        level=logging.INFO,
        format="[%(levelname)s] %(message)s"
    )

    args = set_args()
    keg_dict = stat_keg(args.keg)
    plot_keg(keg_dict, args.out+".pdf")


if __name__ == "__main__":
    main()

