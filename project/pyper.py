import sys
import argparse
import hep_helper


def replace_spaces(string):
    return string.replace(" ", "%20")


def main():
    commands = ""
    flag = 0
    BAI = False

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        help="sub parser help", dest="command", required=True)

    parser_HEP = subparsers.add_parser('HEP', help="Search HEP databse")
    parser_ARXIV = subparsers.add_parser('ARXIV', help="in consturction")

    # Add author to the query
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

    # Add BAI to the query
    parser_HEP.add_argument(
        "-BAI",
        required=False,
        help="Looks for specific INSPiRE identifier and returns the results. Note it will override any other options since the query has to be done on different a platform",
        type=str)

    # Add Collaboration to the query
    parser_HEP.add_argument(
        "-cn",
        required=False,
        help="Search for papers published by a collaboration , i.e. a group of academics and researchers",
        type=str)

    # Add ranges of authors to be taken in the consideration
    parser_HEP.add_argument(
        "-ac",
        required=False,
        help="Search for papers published by specific amount of authors for example: '-ac 10+ , -ac 1->10",
        type=str)

    # Add affiliation to the query
    parser_HEP.add_argument(
        "-aff",
        required=False,
        help="If you want to search for papers published by people affiliated to a particular institution, you can use this operator. Note, however, that you need to know how the institution is registered in INSPIRE’s database",
        type=str)
    
    # Wrtie result to the JSON file
    parser_HEP.add_argument(
        "-save",
        required=False,
        help="Write contents of the query to the json file",
        type=str,
        choices=['json'],
    )
    # Article based search arguments:
    parser_HEP.add_argument(
        "-t",
        required=False,
        help="Adds title of the paper to the query",
        type=str)
    
    # need to add: TEXKEY , EPRINT, DOI, REPORT_NUMBER , RECORD_ID, DOC_TYPE
    # DATE , JOURNAL ,CITATION NUMBER , CITATION OF A RECORD

    # ARXIV:
    parser_ARXIV.add_argument(
        "-b",
        required=False,
        help="Adds the name/s of the author/s to the query",
        type=str)

    args = parser.parse_args()
    hep_args = parser_HEP.parse_args(args=sys.argv[2:])

    # IF A PARAMETER WAS TYPED ADD TO THE QUERY"
    if hep_args.a is not None:
        flag = 1
        commands += "author:" + replace_spaces(hep_args.a) + "%20"
    if hep_args.t is not None:
        flag = 1
        commands += "title:" + replace_spaces(hep_args.t) + "%20"
    if hep_args.ea is not None:
        flag = 1
        commands += "exactauthor:" + replace_spaces(hep_args.ea) + "%20"
    if hep_args.BAI is not None:
        flag = 1
        BAI = True
        commands += replace_spaces(hep_args.BAI) + "%20"
    if hep_args.cn is not None:
        flag = 1
        print("XD")
        commands += "collaboration:" + replace_spaces(hep_args.cn) + "%20"
    if hep_args.ac is not None:
        flag = 1
        commands += "authorcount:" + replace_spaces(hep_args.ea) + "%20"
    if hep_args.aff is not None:
        flag = 1
        commands += "affiliation:" + replace_spaces(hep_args.ea) + "%20"

    if flag == 0:
        print("Choose at least one query variable try:\n" +
              "python3 pyper.py HEP -h " + "for more information")
    else:
        if hep_args.save is not None:
            url = hep_helper.hep_url_generator(commands, hep_args.save, BAI)
            hep_helper.save_to_json(url, "sample_api.json")
        else:
            url = hep_helper.hep_url_generator(commands, hep_args.save, BAI)
            hep_helper.display_in_cmd(url)


if __name__ == "__main__":
    main()
