#!/home/linuxuser/anaconda3/bin/python

import sys
import argparse
from hep_classes import Hep_Helper, Hep_Parser


def main():
    commands = ""
    json_as_string = ""
    hep_helper = Hep_Helper()

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(
        help="sub parser help", dest="command", required=True)

    parser_HEP = subparsers.add_parser('HEP', help="Search HEP databse")
    # parser_ARXIV = subparsers.add_parser('ARXIV', help="in
    # consturction")#for future use

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
    # Write result to given output buffer
    parser_HEP.add_argument(
        "-out",
        required=False,
        help="Show the query output: cmd->show in terminal, 'filename.txt'->write contents to the file named 'filename.txt'",
        type=str,
    )

    parser_HEP.add_argument(
        "-sort",
        required=False,
        help="Sort by: name, citations or date. Ex: -sort name",
        type=str,
        choices=['name', 'citations', 'date']
    )

    args = parser.parse_args()

    hep_args = parser_HEP.parse_args(args=sys.argv[2:])

    # IF A PARAMETER WAS TYPED , ADD TO THE QUERY"

    hep_params = [
        ("author",
         hep_args.a),
        ("exactauthor",
         hep_args.ea),
        ("collaboration",
         hep_args.cn),
        ("title",
         hep_args.t),
        ("arxiv",
         hep_args.arxiv),
        ("recid",
         hep_args.recid),
        ("date",
         hep_args.d),
        ("type-code",
         hep_args.tc),
        ("topcite",
         hep_args.topcite),
        ("doi",
         hep_args.doi),
        ("journal",
         hep_args.j)]

    def isNotNone(x): return x[1] is not None

    filtered_params = list(filter(isNotNone, hep_params))

    if len(filtered_params) == 0:
        print("Choose at least one query variable try:\n" +
              "python3 pyper.py HEP -h " + "for more information")
    else:
        # Initial param encoding.
        for i, (el1, el2) in enumerate(filtered_params):
            if(i == len(filtered_params) - 1):
                commands += el1 + "%3A+" + el2
            else:
                commands += el1 + "%3A+" + el2 + "%20+"

        # Ensure any possible mistakes by the user are properly encoded.
        commands = hep_helper.hep_url_encode(commands)
        # Generate URL
        url = hep_helper.hep_url_generator(commands,
                                           hep_args.out)
        # Retrieve the data from url
        source = hep_helper.get_source(url)

        hep_parser = Hep_Parser(source)

    if hep_args.out is None:
        print("Your output has been written into 'API_OUTPUT_JSON.json'")

    elif hep_args.out == 'cmd':
        if hep_args.sort is not None:
            hep_parser.sort_by(hep_args.sort)

            hep_parser.show()
        else:
            hep_parser.show()
    else:
        if hep_args.sort is not None:
            hep_parser.sort_by(hep_args.sort)

            hep_parser.write(hep_args.out)
            print("Your output has been written into " + hep_args.out)
        else:
            hep_parser.write(hep_args.out)
            print("Your output has been written into " + hep_args.out)


if __name__ == "__main__":
    main()
