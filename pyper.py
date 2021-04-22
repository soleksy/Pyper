#!/usr/bin/env python3
import sys
from datetime import datetime
import json
import argparse
import subprocess

from PARSERS.BASE.base import subparsers , parser

from PARSERS.HEP.hep import parser_HEP
from PARSERS.HEP.hep_classes import Hep_Helper, Hep_Parser

from PARSERS.ARXIV.arxiv import parser_ARXIV
from PARSERS.ARXIV.arxiv_classes import Arxiv_Helper, Arxiv_Parser

from PARSERS.MULTI.multi import parser_MULTI
from PARSERS.MULTI.multi_classes import MultiSearch

from PARSERS.CONFIG.config import parser_CONFIG

def main():

    #LOAD CONFIGURATION FILE OPTIONS

    ARX_OUTPUTS = ""
    HEP_OUTPUTS = ""
    MULTI_OUTPUTS = ""
    NAME_FILES_CURRENT_DATES = 0

    with open("config.json") as f:
        conf_data = json.load(f)
        ARX_OUTPUTS = conf_data["ARXIV_OUTPUT_FOLDER"]
        HEP_OUTPUTS =  conf_data["HEP_OUTPUT_FOLDER"]
        MULTI_OUTPUTS = conf_data["MULTI_OUTPUT_FOLDER"]
        NAME_FILES_CURRENT_DATES = conf_data["NAME_FILES_CURRENT_DATES"]

    #---------------------------PARSER SELECTION------------------------------#
    MS_dict = dict()
    HEP = False
    ARXIV = False
    CONFIG = False
    MULTISEARCH = False

    Selected_Parser = ""
    args = parser.parse_args()
    Selected_Parser = sys.argv[1]

    if Selected_Parser == "HEP":
        HEP = True
    elif Selected_Parser == "ARXIV":
        ARXIV = True
    elif Selected_Parser == "CONFIG":
        CONFIG = True
    elif Selected_Parser == "MULTI":
        multi_args = parser_MULTI.parse_args(args=sys.argv[2:])
        #For now by default both databases are set to true since there are only 2 and it makes no sense to use Mult-search to look in one database.
        #if multi_args.ARXIV == True:
        ARXIV = True
        #if multi_args.HEP == True:
        HEP = True


    #--------------------------------HEP--------------------------------------#
    if CONFIG:
        conf_args = parser_CONFIG.parse_args(args=sys.argv[2:])
        
        if conf_args.edit is not None:
            subprocess.run(args=["vim" , "config.json"])
    if HEP:
        hep_helper = Hep_Helper()
        commands = ""
        json_as_string = ""

        if Selected_Parser == "MULTI":
            hep_args = parser_MULTI.parse_args(args=sys.argv[2:])
            hep_params = [
                ("author",
                 hep_args.a),
                ("title",
                 hep_args.t),
                ("date",
                 hep_args.d),
                ("arxiv",
                 hep_args.arxiv),
                ("doi",
                 hep_args.doi),
                ("journal",
                 hep_args.j)
            ]
        else:

            hep_args = parser_HEP.parse_args(args=sys.argv[2:])
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
                 hep_args.j),
                ("query",
                 hep_args.q)]

        def isNotNone(x): return x[1] is not None

        filtered_params = list(filter(isNotNone, hep_params))

        if len(filtered_params) == 0:
            print("Choose at least one query variable try:\n" +
                  "python3 pyper.py HEP -h " + "for more information")
        else:
            # Initial param encoding.
            for i, (el1, el2) in enumerate(filtered_params):
                if(i == len(filtered_params) - 1):
                    commands += "%3A+" + el2
                else:
                    commands += "%3A+" + el2 + "%20+"

            # Ensure any possible mistakes by the user are properly encoded.
            commands = hep_helper.hep_url_encode(commands)
            # Generate URL
            if(hep_args.q is not None):
                url = hep_helper.hep_url_generator(hep_args.q)
            else:
                url = hep_helper.hep_url_generator(commands)
            # Retrieve the data from url
            source = hep_helper.get_source(url)

            hep_parser = Hep_Parser(source)

            
    #-------------------------------ARXIV------------------------------------#
    if ARXIV:

        arx_helper = Arxiv_Helper()
        query_url = ""
        data = ""

        if Selected_Parser == "MULTI":
            arx_args = parser_MULTI.parse_args(args=sys.argv[2:])
            arx_params_list = [
                ("au", arx_args.a),
                ("ti", arx_args.t),
                ("jr", arx_args.j),
                ("doi", arx_args.doi),
                ("id_list", arx_args.arxiv),
            ]
        else:
            arx_args = parser_ARXIV.parse_args(args=sys.argv[2:])
            arx_params_list = [
                ("au", arx_args.a),
                ("ti", arx_args.t),
                ("jr", arx_args.j),
                ("doi", arx_args.doi),
                ("id_list", arx_args.id),
                ("ALL", arx_args.ALL)
            ]

        def isNotNone(x): return x[1] is not None

        filtered_params = list(filter(isNotNone, arx_params_list))

        if len(filtered_params) == 0:
            print("Please choose at least one parameter for the query type -h for more information on query options")
            return -1

        if Selected_Parser == "MULTI":
            query_url = arx_helper.params_to_url(filtered_params)

        elif arx_args.ALL is not None:
            # Run Query for all parameters
            query_url = arx_helper.all_param(arx_args.ALL)
        else:
            # Run Query for specific parameters
            query_url = arx_helper.params_to_url(filtered_params)
        file_to_parse_arxiv = 'data/ARXIV_OUTPUT.xml'

        # Load api result to file
        arx_helper.api_to_file(query_url, file_to_parse_arxiv)

        # Initialize Arxiv Parser
        arx_parser = Arxiv_Parser(file_to_parse_arxiv)
        
        # Load , standarize and save data

        arx_parser.standarize_xml_file()

        arx_parser.parse_xml()

    #------------------SECTION FOR FILE OUTPUT HANDLING--------------------#
    
    #--------------------------------ARXIV---------------------------------#
    if ARXIV == True and Selected_Parser != "MULTI":
        if arx_args.range is not None:
            if arx_parser.filter_range(arx_args.range) == -1:
                return
        if arx_args.sort is not None:
            arx_parser.sort_by(arx_args.sort)



        if NAME_FILES_CURRENT_DATES == 1:
            arx_parser.write_data(ARX_OUTPUTS + str(datetime.now()) + ".txt")
            print("Your query result has been written to the " + ARX_OUTPUTS + str(datetime.now()) + ".txt")
        else:
            arx_parser.write_data(ARX_OUTPUTS + arx_args.file)
            arx_parser.write_bibtex(ARX_OUTPUTS + "/bibtex.txt")
            print("Your query result has been written to the " + ARX_OUTPUTS + arx_args.file)


    #-------------------------------HEP------------------------------------#
    if HEP == True and Selected_Parser != "MULTI":
        if hep_args.sort is not None:
            hep_parser.sort_by(hep_args.sort)

        if NAME_FILES_CURRENT_DATES == 1:
            hep_parser.write_data(HEP_OUTPUTS + str(datetime.now())  + ".txt")
            print("Your query result has been written to the " + HEP_OUTPUTS + str(datetime.now()) + ".txt")
        else:
            hep_parser.write_data(HEP_OUTPUTS + hep_args.file)
            hep_parser.write_bibtex(HEP_OUTPUTS + "/bibtex.txt")

            print("Your query result has been written to the " + HEP_OUTPUTS + hep_args.file)
        

    #----------------SECTION FOR MULTISEARCH COMPARISONS-------------------#
    if Selected_Parser =="MULTI":
        if HEP == True:
            MS_dict["HEP"] = hep_parser
        else:
            MS_dict["HEP"] = None
    
        if ARXIV == True:
            MS_dict["ARXIV"] = arx_parser
        else:
            MS_dict["ARXIV"] = None

        MS = MultiSearch(MS_dict)
        multi_args = parser_MULTI.parse_args(args=sys.argv[2:])
        # compare results of every passed database object
        if NAME_FILES_CURRENT_DATES == 1:
            MS.write(MULTI_OUTPUTS + str(datetime.now())  + ".txt")
            print("Your query result has been written to the " + MULTI_OUTPUTS + str(datetime.now()) + ".txt")
        else:
            MS.write(MULTI_OUTPUTS + multi_args.file)
            print("Your query has been written to the " + MULTI_OUTPUTS  + multi_args.file)
    


if __name__ == "__main__":
    main()
