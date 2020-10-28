#City Growth Project
##Introduction
The U.S has been taking a Census every 10 years since 1990. 
Every person in the country is asked a few questions each
census about their family and household. This data is then
collected to provide a summary of life in the U.S.A. The 
Census records the population of every state, county
(county equivalent), city, town, and village. The population
is broken up by age, gender, race, and other categories. 
The Census also records poverty rates, median income, and
other data points relating to the economy. This data is 
then exported into table form, and placed into a .pdf, .xlsx,
.csv, or .txt file. These files are open to the public
on the Census Bureau website at census.gov. 

##Overview
The City Growth project tries to use the Census data to
predict future population levels, and possibly future levels
of povery and income. This project can show what causes 
losses and increases in population, poverty, income, homelessness,
and other factors important to quality of life. This can
then be used to find ways to help some places that are
very poor, or are becoming poor quickly (like Detroit, MI or 
West Virginia). 

##Steps
1. Find sources from the Census Bureau that have relevant information
1a. Find files with populations of states from recent times 
(2010 and 2000 census).
1b. Find information about counties and cities. 
1c. Find more information. 
1d. Find information for older censuses. 
2. Convert sources to easily readable data files. 
2a. Export (if possible) files to .csv or .txt
2b. Remove any unnecessary information, like population estimates. 
Our project will try to use facts, and not projections. 
2c. Convert any and all .pdf files to .csv files
3. Explore the data. 
3a. Find out what variables relate to each other. 
3b. Try to represent the same data in different ways. 
3c. Find out which variables are irrelevant. 
4. Create models. 
4a. Create a population model.
4b. There might be different models for cities and states
or the same model. 

##Directory
####Census-Files
This folder holds the final data files. All files will be .csv
files. These files will be created in step 2, and used in steps 
3 and 4. CSV Files here have the naming pattern:
YEAR-AREA-DATA.csv, where:
YEAR is a 4 digit number that says which decennial census it was for
AREA says which areas the data represents. It can be State, City, All, etc.
DATA is a one word description of what is represented.
One possible file is 2000-All-Population.csv

####OCR-Files
This folder holds any pdf files from the Census Bureau
that were converted to a .csv file using onlineocr.net. 
These files will be used in step 2, and deleted afterwards. 
There is no naming pattern for this folder. 

####Abbreviations.txt, Sources.txt
Abbreviations.txt has the meanings of any abbreviations
used in the column headers in the Census-Files folder. 

Sources.txt lists the source (where the original file was found)
for all files in the Census-Files folder. 

####Python Files
FileConvert.py converts files in OCR-Files to .csv files for
Census-Files. Some data must be entered manually, because
the OCR is not perfect. 

##Notes
All place names are Capitalized, to make it easier. 