# Pyper

## How to use

### Note: Using Python version 3.7 or above is necessary for the scripts to behave properly.

    Note that if option NAME_FILES_CURRENT_DATES in the config file is set to 1 the file name will be
    automatically set to current date and the -file option is not required.

python3 pyper.py -h for help

python3 pyper.py {ARXIV,HEP} -h for detailed query parameters


## EXAMPLE FOR ARXIV QUERY:

./pyper.py ARXIV -a "S. Dong" -t Detector -file "Arxiv_output.txt"



## Below one of many outputs:

- Authors: 
 - David Blair, Li Ju, Chunnong Zhao, Linqing Wen, Haixing Miao, Ronggen Cai, Jiangrui Gao, Xuechun Lin, Dong Liu, Ling-An Wu, Zonghong Zhu, Giles Hammond, Ho Jung Paik, Viviana Fafone, Alessio Rocchi, Chunnong Zhao, Yiqiu Ma, Jiayi Qin, Michael Page, 

- Date_Published: 
- 2016-02-16T16:44:01Z

- Last_Update: 
- 2016-02-16T16:44:01Z

- Title: 
- The next detectors for gravitational wave astronomy

- ID: 
- 1602.05087

- DOI: 
- 10.1007/s11433-015-5747-7

- Journal: 
- Sci China-Phys Mech Astron, 58: 120405 (2015)

- Num_Of_Authors: 
- 19



## EXAMPLE FOR HEP QUERY:

./pyper.py HEP -a witten -t "black hole" -file "Hep_output.txt"
    
## Below one of many outputs:

- Authors: 
- Herrera, L. ,Di Prisco, A. ,Ospino, J. ,Witten, L. ,

- Date_Published: 
- 2020-02-19T04:16:45

- Title: 
- Geodesics of the hyperbolically symmetric black hole

- ID: 
- 2002.07586

- DOI: 
- 10.1103/PhysRevD.101.064071

- Citations: 
- 1

- Journal: 
- Phys. Rev. D 101, 064071 (2020)

- Num_Of_Authors: 
- 4



## EXAMPLE FOR MULTI QUERY:

./pyper.py MULTI -a witten -t "black hole" -file "Multi_output.txt"

- Authors: 
- Cenalo Vaz ,Louis Witten ,T. P. Singh ,

- Date_Published: 
- 2003-06-11T11:52:49Z

- Last_Update: 
- 2004-02-04T19:26:45Z

- Title: 
- Exact Quantum State of Collapse and Black Hole Radiation

- ID: 
- gr-qc/0306045

- DOI: 
- 10.1103/PhysRevD.69.104029

- Journal: 
- Phys.Rev. D69 (2004) 104029

- Citations: 
- No data from HEP

- Num_Of_Authors: 
- 3

- The above result might not seem to differ from the 2 previous ones but actually if one would have searched 
- inside hep database only this result would not show up since there was no data in HEP for this article.
