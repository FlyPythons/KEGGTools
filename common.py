
import logging


LOG = logging.getLogger(__name__)

__version__ = "0.1.0"
__author__ = ("Junpeng Fan",)
__email__ = "jpfan@whu.edu.cn"


def read_org(file):
    """
    read .org file create by get_organism.py
    :return: a list [org.abbr, name, url]
    """

    r = []

    LOG.info("get organism infomation from %r" % file)

    for line in open(file):
        line = line.strip()

        if line:
            r.append(line.split("\t"))

    LOG.info("get %s records" % len(r))

    return r


def read_org_ko(file):
    """
    read KEGG organism KO .keg file
    :param file: file name
    :return: dict contains {protein_id: {"ko": [], "path": []}}, if protein_id has no ko, the ko will be "-"
    """

    r = {}

    path_id = ""

    for n, line in enumerate(open(file)):
        line = line.strip()

        if not line:
            continue

        tag = line[0]

        if tag == "C":
            path_id = "ko"+line[-6:-1]
            continue

        if tag != "D":
            continue

        tmp = line.split("\t")
        gene = tmp[0].split()[1]

        if len(tmp) == 2:
            ko = tmp[1].split()[0]
        else:
            LOG.warning("line %s: %r has no ko" % (n+1, line))
            ko = ""

        if gene not in r:
            r[gene] = {"ko": [], "path": []}

        if ko not in r[gene]["ko"]:
            r[gene]["ko"].append(ko)

        if path_id not in r[gene]["path"]:
            r[gene]["path"].append(path_id)

    return r
