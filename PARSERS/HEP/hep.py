from PARSERS.BASE.base import subparsers

parser_HEP = subparsers.add_parser('HEP', help="Search HEP databse")

#----------------------------HEP ARGUMENTS---------------------------#
# Add author to the query
parser_HEP.add_argument(
    "-q",
    required=False,
    help="Use for keyword search, if used simply write your keywords afterwards",
    type=str)

parser_HEP.add_argument(
    "-a",
    required=False,
    help="Adds the name/s of the author/s to the query.",
    type=str)

# Add exact author to the query
parser_HEP.add_argument(
    "-ea",
    required=False,
    help="Query will include only the exact name of the author",
    type=str)

# Add Collaboration to the query
parser_HEP.add_argument(
    "-cn",
    required=False,
    help="Search for papers published by a collaboration , i.e. a group of academics and researchers",
    type=str)

# Article based search arguments:
parser_HEP.add_argument(
    "-t",
    required=False,
    help="Adds title of the paper to the query",
    type=str)

# Add Eprint to the query
parser_HEP.add_argument(
    "-arxiv",
    required=False,
    help="Adds eprint to the query",
    type=str)

# Add Record ID to the query
parser_HEP.add_argument(
    "-recid",
    required=False,
    help="Adds record id to the query",
    type=str)

# Specify Date ranges for the query
parser_HEP.add_argument(
    "-d",
    required=False,
    help="Specify date range for the query. Examples : -d 2018+ ,-d 2000- ,-d 1980->1982",
    type=str)

# Add DOI to the query
parser_HEP.add_argument(
    "-doi",
    required=False,
    help="Add Digital Object Identifier to the query",
    type=str)

# Add journal reference to the query
parser_HEP.add_argument(
    "-j",
    required=False,
    help="If you’d like to stay up to date with publications of a specific journal, then a search by journal will be helpful ex: -j Physics.Rev.D",
    type=str)

# Add Type-Code to the query
parser_HEP.add_argument(
    "-tc",
    required=False,
    help="Search for papers of specyfic type ex: b: book ,c: conference paper ,core: work covering high-energy-physics,i: introductory" +
    " l: lectures, note: experimental note, p: published,proceedings:collected volume of a conference proceedings, r: review ,t: thesis",
    type=str,
    choices=[
        'b',
        'c',
        'i',
        'l',
        'p',
        'r',
        't',
        'core',
        'note',
        'proceedings'])

parser_HEP.add_argument(
    "-topcite",
    required=False,
    help="If you want to find works that are often cited in other publications, you can use this option to search, ex of use: topcite 100->150",
    type=str,

)
#-------------------------GENERAL HEP ARGUMENTS---------------------------#
parser_HEP.add_argument(
    "-file",
    required=True,
    help="Show the query output: cmd->show in terminal, 'filename.txt'->write contents to the file named 'filename.txt'",
    type=str,
)

parser_HEP.add_argument(
    "-sort",
    required=False,
    help="Sort by: name, citations or date. Ex: -sort name",
    type=str,
    choices=['authors', 'citations', 'date']
)
