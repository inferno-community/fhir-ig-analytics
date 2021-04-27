# fhir-ig-analytics
Georgia Tech project considering FHIR IG Analytics for the Spring 2021 semester.

Cameron Farzaneh - cfarzaneh3@gatech.edu

Greg Bertolacci - gbertolacci3@gatech.edu

## Project Overview
FHIR Implementations Guides are key to interoperable health information. Standardizing data representation and terminology is key to preserving semantic interoperability. FHIR IGs are crafted by groups of stakeholders and domain experts who must adapt their models to meet growing challenges. This project will use publicly available metadata about implementation guides to provide useful analytic information. 

This project will analyze various FHIR Implementations Guides and uncover which IGs conform to the [FHIR NPM Package Specification](https://wiki.hl7.org/FHIR_NPM_Package_Spec) and which ones do not. It will also analyze the different dependencies and resources of each IG. Lastly, we display this information visually with histograms and a Github Pages website.

## Getting Started

This project uses Python3. <u>Please make sure to run this project from the py-ig-analytics working directory.</u> If there are any missing dependencies in your environment, you can install the missing packages like so:
<br>`pip3 install tqdm`</br>

### py-ig-analytics
Python project to perform the implementation guide analysis. This project consists of four python files:
- `main.py`
	- Main python module to run entire analysis from start to finish.
- `getFHIRIGs.py`
	- Uses qas.json and Simplifier.net API to download the FHIR IG's/
- `validate.py`
 	- will first check to make sure that each package has both a package.json and index.json files
 	- then checks to make sure the package.json has the mandatory fields ['name','version','description','dependencies','author']
 	- while checking those fields it records what dependencies are in each package 
 	- then checks resources present in the "package" folder other than package.json and index.json
 	- This also returns a list of resources and a list of resource types used in each package
 	- this outputs a csv to metatata/metadata.csv
- `analytics.py`
 	- cleans the metadata.csv that will be used for github pages
 	- creates a histogram of the status of all packages
 	- creates a histogram of the dependancy usage & csv
 	- creates a histogram of the top 10 resources present & csv
	- creates a histogram of the top 10 resource types present & csv

To get output, please run `main.py` from the py-ig-analytics directory. In the root level of the project, you can find two new directories. `output` and `metadata`. The output directory contains the FHIR IG's while the metadata folder includes all of the analysis and histograms stored as CSV files and histogram images. To view results, open `index.html` in your browser or go to: https://inferno-community.github.io/fhir-ig-analytics/

##  How to extend/augment project functionality

To run analysis on custom FHIR packages, you can place the tar files in the output directory. Then you can run the script as noraml.