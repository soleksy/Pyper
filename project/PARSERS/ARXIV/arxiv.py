from PARSERS.BASE.base import subparsers

parser_ARXIV = subparsers.add_parser('ARXIV', help="Search Arxiv database")

#----------------------------ARXIV ARGUMENTS-----------------------------#

parser_ARXIV.add_argument(
    "-ALL",
    required=False,
    help="This option is highly advised for general queries which could include terms related to either content of an article or any other parameter availible here. Besides the available arguments -ALL options searches through comments,abstract,subject categories and report numbers",
    type=str,
)
parser_ARXIV.add_argument(
    "-a",
    required=False,
    help="Add author name to the query",
    type=str,
)
parser_ARXIV.add_argument(
    "-t",
    required=False,
    help="Add title to the query",
    type=str,
)
parser_ARXIV.add_argument(
    "-id",
    required=False,
    help="Search by a comma separated Arxiv ID's",
    type=str,
)
parser_ARXIV.add_argument(
    "-j",
    required=False,
    help="Add journal reference to the query",
    type=str,
)
parser_ARXIV.add_argument(
    "-doi",
    required=False,
    help="Add doi to the query",
    type=str,
)
#-------------------------GENERAL ARXIV ARGUMENTS--------------------------#
#if NAME_FILES_CURRENT_DATES == 0:
parser_ARXIV.add_argument(
    "-file",
    required=True,
    help="Write contents to file",
    type=str,
)
parser_ARXIV.add_argument(
    "-sort",
    required=False,
    help="Sort the output of your query by either number of authors, date published or date of last update on the paper",
    choices=[
        'authors',
        'published',
        'updated'])

parser_ARXIV.add_argument(
    "-range",
    required=False,
    help="Add year range to show results published within given range, Examples: '-X' till year X , '+X' after year X, 'X-Y' between X and Y",
    type=str,
)