
from __future__ import absolute_import

import gzip
from os.path import abspath, expanduser


def split_header(name):
    """
    split fasta header to id and description
    :param name:
    :return:
    """
    parts = name.split(None, 1)

    if len(parts) == 1:
        parts.append("")

    return parts


class FastaRecord(object):
    """
    object to process a fasta record
    """
    DELIMITER = ">"

    def __init__(self, name, seq):
        try:
            assert "\n" not in name
            assert "\n" not in seq
            assert self.DELIMITER not in seq
            self._name = name
            self._seq = seq
            self._id, self._description = split_header(name)
        except AssertionError:
            raise ValueError("Invalid FASTA record data")

    @property
    def name(self):
        """
        the name of the seq, strings after ">"
        """
        return self._name

    @property
    def id(self):
        """
        The id of the seq, equal to the FASTA header
        up to the first whitespace.
        """
        return self._id

    @property
    def description(self):
        """
        The description of the seq in the FASTA file, equal to
        the contents of the FASTA header following the first whitespace
        """
        return self._description

    @property
    def seq(self):
        """
        The seq of the record

        """
        return self._seq

    @property
    def length(self):
        """
        the length of the seq
        """
        return len(self._seq)

    @classmethod
    def from_string(cls, string):
        """
        Interprets a string as a FASTA record.  Does not make any
        assumptions about wrapping of the seq string.
        """
        string = string.strip()

        try:
            lines = string.splitlines()
            assert len(lines) > 1
            assert lines[0][0] == cls.DELIMITER
            name = lines[0][1:]
            seq = "".join(lines[1:])
            return FastaRecord(name, seq)
        except AssertionError:
            raise ValueError("String not recognized as a valid FASTA record")

    def __str__(self):
        """
        str conversion
        :return:
        """
        return ">%s\n%s" % (self.name, self.seq)


def check_format(filename):
    """
    check the format of file
    :param filename:
    :return:
    """
    allowed_format = [".fa", ".fasta", ".fa.gz", ".fasta.gz"]

    if any([f for f in allowed_format if filename.endswith(f)]):
        return 0
    else:
        msg = "file format is not in %s" % allowed_format
        raise Exception(msg)


def yield_fasta_records(stream):
    """
    yield fastq records from stream
    :param stream: a stream object
    :return:
    """
    string = ""

    for line in stream:
        line = line.strip()

        if not line:
            continue

        if string and line.startswith(">"):
            yield FastaRecord.from_string(string)
            string = ""

        string += "%s\n" % line

    if string:
        yield FastaRecord.from_string(string)


def open_fasta(filename):
    """
    read fasta file and return fasta records
    :param filename:
    :return:
    """
    check_format(filename)
    filename = abspath(expanduser(filename))
    mode = 'r'

    if filename.endswith(".gz"):
        stream = gzip.open(filename, mode)
    else:
        stream = open(filename, mode)

    return yield_fasta_records(stream)
