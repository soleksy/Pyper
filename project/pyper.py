#!/home/linuxuser/anaconda3/bin/python

import sys
import argparse
from hep_classes import Hep_Helper,Hep_Parser


def replace_spaces(string):
    return string.replace(" ", "%20")
def show_parsed(date,names,titles,citations):
        for i in range(len(names)):
            print( "Date: "+ date[i] +"\n" + "Creator: " + names[i] + "\n" + "Title: " + titles[i]+ "\n" + "Citations: "+ str(citations[i])+"\n")

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
    #Add DOI to the query
    parser_HEP.add_argument(
        "-doi",
        required=False,
        help="Add Digital Object Identifier to the query",
        type=str)
    #Add journal reference to the query
    parser_HEP.add_argument(
        "-j",
        required=False,
        help="If you’d like to stay up to date with publications of a specific journal, then a search by journal will be helpful ex: -j Physics.Rev.D",
        type=str)
    #Add Type-Code to the query
    parser_HEP.add_argument(
        "-tc",
        required=False,
        help="Search for papers of specyfic type ex: b: book ,c: conference paper ,core: work covering high-energy-physics,i: introductory" +\
             " l: lectures, note: experimental note, p: published,proceedings:collected volume of a conference proceedings, r: review ,t: thesis",
        type = str,
        choices = ['b','c','i','l','p','r','t','core','note','proceedings']
    )

    parser_HEP.add_argument(
        "-topcite",
        required=False,
        help="If you want to find works that are often cited in other publications, you can use this option to search, ex of use: topcite 100->150",
        type = str,

    )
    # Write result to the JSON file
    parser_HEP.add_argument(
        "-show",
        required=False,
        help="Write contents of the query to the json file",
        type=str,
        choices=['json', 'out'],
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
        for i, (el1, el2) in enumerate(filtered_params):
            if(i == len(filtered_params) - 1):
                commands += el1 + "%3A+" + el2
            else:
                commands += el1 + "%3A+" + el2 + "%20+"

        commands = hep_helper.hep_url_encode(commands)
        url = hep_helper.hep_url_generator(
                commands, hep_args.show)
        source = hep_helper.get_source(url)
        

    if hep_args.show is not None:
        if hep_args.show == "json":

            

            hep_helper.write_to_json(source, "API_OUTPUT_JSON.json")

        else:
            hep_parser = Hep_Parser(source)

            creator_names = hep_parser.get_creator_names()
            titles = hep_parser.get_title()
            dates = hep_parser.get_creation_date()
            citations = hep_parser.get_citation_count()

            show_parsed(dates,creator_names,titles,citations)


        

if __name__ == "__main__":
    main()
