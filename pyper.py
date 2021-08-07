#!/usr/bin/env python3
import sys
from datetime import datetime
import json
import argparse
import subprocess


from APIS.HEP.HepClasses import HepHelper, HepParser
from APIS.ARXIV.ArxivClasses import ArxivHelper, ArxivParser

from PARSER.base.base import BaseParser

def main():

    ArxivOutput = ""
    HepInspireOutput = ""


    with open("config.json") as f:
        conf_data = json.load(f)
        ArxivOutput = conf_data["ARXIV_OUTPUT_FOLDER"]
        HepInspireOutput =  conf_data["HEP_OUTPUT_FOLDER"]

    parser = BaseParser.parse_args(args=sys.argv[1:])

    apiParams = {
        "arxiv": parser.arxiv,
        "hep": parser.hep,
    }

    searchParams = [

        ("author",
            parser.a),
        ("title",
            parser.t),
        ("arx",
            parser.arx),
        ("doi",
            parser.doi),
        ("journal",
            parser.j),
        ("all",
            parser.all)]

    def isNotNone(x): return x[1] is not None

    filteredParams = list(filter(isNotNone, searchParams))

    if parser.hep is True:
        hepHelper = HepHelper()
        commands = ""

        if len(filteredParams) == 0:
            print("Choose at least one query variable try:\n" +
                    "python3 pyper.py -h " + "for more information")
        else:
            for i, (el1, el2) in enumerate(filteredParams):
                if(i == len(filteredParams) - 1):
                    commands += "%3A+" + el2
                else:
                    commands += "%3A+" + el2 + "%20+"

            commands = hepHelper.hepUrlEncode(commands)

            if(parser.all is not None):
                url = hepHelper.hepUrlGenerator(parser.all)
            else:
                url = hepHelper.hepUrlGenerator(commands)

            source = hepHelper.getSource(url)
            hepParser = HepParser(source)
            hepParser.parseJsonFile()

            hepParser.writeData(HepInspireOutput + "test.txt")
            hepParser.writeBibtex(HepInspireOutput + "/bibtex.txt")

            print("Your query result has been written to the " + HepInspireOutput + "test.txt")

            
    if parser.arxiv is True:

        arxivHelper = ArxivHelper()
        queryURL = ""

        if len(filteredParams) == 0:
            print("Please choose at least one parameter for the query type -h for more information on query options")
            return -1

        elif parser.all is not None:
            # Run Query for all parameters
            queryURL = arxivHelper.allParamSearch(parser.all)
        else:
            # Run Query for specific parameters
            queryURL = arxivHelper.paramsToUrl(filteredParams)

        file_to_parse_arxiv = 'data/ARXIV_OUTPUT.xml'

        # Load api result to file
        print(queryURL)

        arxivHelper.apiToFile(queryURL, file_to_parse_arxiv)

        # Initialize Arxiv Parser
        arxivParser = ArxivParser(file_to_parse_arxiv)
        
        # Load , standardize and save data

        arxivParser.standarizeXmlFile()
        arxivParser.parseXML()

        arxivParser.writeData(ArxivOutput + "arxtest")
        arxivParser.writeBibtex(ArxivOutput + "bibtest")

        print("Your query result has been written to the " + ArxivOutput + "bibtest")
        print("Your query result has been written to the " + ArxivOutput + "arxtest")


    


if __name__ == "__main__":
    main()
