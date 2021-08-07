import argparse

BaseParser = argparse.ArgumentParser()
#----------------------------HEP ARGUMENTS---------------------------#

BaseParser.add_argument(
    "-arxiv",
    required=False,
    help="If used, your query will be used to search arxiv databse",
    action='store_true')

BaseParser.add_argument(
        "-hep",
        required=False,
        help="If used, your query will be used to search hep-inspire databse",
        action='store_true')

BaseParser.add_argument(
    "-all",
    required=False,
    help="Use for keyword search, if used simply write your keywords afterwards",
    type=str)

BaseParser.add_argument(
    "-a",
    required=False,
    help="Adds the name/s of the author/s to the query.",
    type=str)

BaseParser.add_argument(
    "-t",
    required=False,
    help="Adds title of the paper to the query",
    type=str)


BaseParser.add_argument(
    "-arx",
    required=False,
    help="Adds eprint to the query",
    type=str)


BaseParser.add_argument(
    "-doi",
    required=False,
    help="Add Digital Object Identifier to the query",
    type=str)

BaseParser.add_argument(
    "-j",
    required=False,
    help="If you’d like to stay up to date with publications of a specific journal, then a search by journal will be helpful ex: -j Physics.Rev.D",
    type=str)
