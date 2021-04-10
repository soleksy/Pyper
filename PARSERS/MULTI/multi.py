from PARSERS.BASE.base import subparsers

parser_MULTI = subparsers.add_parser(
    'MULTI', help="Search multiple databases")


    #-----------------------MULTI SEARCH ARGUMENTS-----------------------#
parser_MULTI.add_argument(
    "-ARXIV",
    required=False,
    help="Search in ARXIV database",
    action='store_true'
)
parser_MULTI.add_argument(
    "-HEP",
    required=False,
    help="Search in HEP database",
    action='store_true'
)
parser_MULTI.add_argument(
    "-a",
    required=False,
    help="Adds the name/s of the author/s to the query.",
    type=str
)
parser_MULTI.add_argument(
    "-t",
    required=False,
    help="Addds the title or its part to the search query",
    type=str
)

parser_MULTI.add_argument(
    "-d",
    required=False,
    help="Adds date ranges to the multi search query",
    type=str
)
parser_MULTI.add_argument(
    "-arxiv",
    required=False,
    help="Addds the arxiv id to the query",
    type=str
)
parser_MULTI.add_argument(
    "-doi",
    required=False,
    help="Adds the document id to the query",
    type=str
)
parser_MULTI.add_argument(
    "-j",
    required=False,
    help="Adds journal reference to the query",
    type=str
)
#if NAME_FILES_CURRENT_DATES == 0:
parser_MULTI.add_argument(
    "-file",
    required=True,
    help="Add file name for the output to be written into",
    type=str
)

parser_MULTI.add_argument(
    "-sort",
    required=False,
    help="Sort by: date or title",
    type=str,
    choices=['date', 'title']
)