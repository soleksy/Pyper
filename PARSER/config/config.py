from PARSER.base.base import subparsers

parser_CONFIG = subparsers.add_parser('CONFIG' , help = "Modify the current state of configuration file")

#-----------------------CONFIG ARGUMENTS-----------------------------#
parser_CONFIG.add_argument(
    "-edit",
    required=False,
    help="Edit the current state of the configuration file",
    action="store_true"
)