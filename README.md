# fhir-ig-analytics
Georgia Tech project considering FHIR IG Analytics for the Spring 2021 semester

### getFHIRpackages
Python script to fetch most packages from FHIR Package Registry using Simplifier.net API. To run the script, please use Python v3. If dependencies are missing, you can install any like so:
`pip3 install tqdm`


What this project does
 - getFHIRIGs.py
 	- will download all of available fhir packages

 - validate.py
 	- will first check to make sure that each package has both a package.json and index.json files
 	- then checks to make sure the package.json has the mandatory fields ['name','version','description','dependencies','author']
 	- while checking those fields it records what dependencies are in each package 
 	- then checks resources present in the "package" folder other than package.json and index.json
 	- This also returns a list of resources and a list of resource types used in each package
 	- this outputs a csv to metatata/metadata.csv that

 - analytics.py 
 	- cleans the metadata.csv that will be used for github pages
 	- creates a histogram of the status of all packages
 	- creates a histogram of the dependancy usage & csv
 	- creates a histogram of the top 10 resources present & csv
	- creates a histogram of the top 10 resource types present & csv

	