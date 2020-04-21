# Pyper

## How to use

python3 pyper.py -h for help

python3 pyper.py {ARXIV,HEP} -h for detailed query parameters


## EXAMPLE FOR ARXIV QUERY:

./pyper.py ARXIV -a "S. Dong" -t Detector -file "Arxiv_output.txt"

## AND 3 OUTPUTS:

- S. Dong is one of 7 authors
- Title: Detector control system for CBM-TOF
- ID: http://arxiv.org/abs/2004.08969v1
- Date Published: 2020-04-19T21:46:10Z
- Last Update: 2020-04-19T21:46:10Z
-----------------------------------------------------------------------
- S. Dong is one of 38 authors
- Title: Design and construction of the POLAR detector
- ID: http://arxiv.org/abs/1709.07191v2
- Date Published: 2017-09-21T07:53:41Z
- Last Update: 2017-09-28T09:45:19Z
- DOI: 10.1016/j.nima.2017.09.053
-----------------------------------------------------------------------
- S. Dong is one of 48 authors
- Title: Time performance of a triple-GEM detector at high rate
- ID: http://arxiv.org/abs/2004.04944v1
- Date Published: 2020-04-10T08:26:24Z
- Last Update: 2020-04-10T08:26:24Z




## EXAMPLE FOR HEP QUERY:

./pyper.py HEP -a witten -t "black hole" -out "Hep_output.txt"

## AND 3 OUTPUTS:

- Creation_date: 2020-02-19T04:16:45
- Creator_name: Herrera, L.
- Title: Geodesics of the hyperbolically symmetric black hole
- Arxiv_ID: arXiv:2002.07586
- DOI: 10.1103/PhysRevD.101.064071
- Citations: 1
-----------------------------------------------------------------------
- Creation_date: 2016-09-07T12:06:22
- Creator_name: Gass, Richard
- Title: Do Black Holes Form?
- Arxiv_ID: ['hep-th/9212034', 'UCTP-10-92']
- DOI: DOI not specified
- Citations: 0
-----------------------------------------------------------------------
- Creation_date: 2012-10-17T00:00:00
- Creator_name: Witten, Edward
- Title: Quantum mechanics of black holes
- Arxiv_ID: None
- DOI: 10.1126/science.1221693
- Citations: 2

