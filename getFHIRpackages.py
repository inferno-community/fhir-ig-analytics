import requests
from string import ascii_lowercase
from tqdm import tqdm
import os
import shutil
import urllib.request 

goodPackages = set()
badPackages = set()
reasons = list()

baseUrl = 'https://packages.fhir.org/'

if os.path.exists('output'):
    print("Output folder already exists. Deleting.")
    shutil.rmtree('output')
    
os.makedirs('output')
os.makedirs('output/good')
os.makedirs('output/bad')

def is_fhir_standard(response):
    # make sure the package follows the fhir standard
    # variable to track if package follows standard 
    is_standard = "passed"
    
    # Name must have at least one of these strings
    if not any(x in response['Name'].lower() for x in ['.']):
        is_standard = "incorrect_name"
    
    # Name Must not have any of these strings
    if any(x in response['Name'].lower() for x in ['test', "sandbox", 'dummy']):
        is_standard = "incorrect_name"    
        
    # the package must not containt the following
    try:
        if any(x in response['Description'].lower() for x in ['test', "sandbox", 'dummy', "Put a description here"]):
            is_standard = "incorrect_description"
    
        if any(x in response['Description'].lower() for x in ['retired', ]):
            is_standard = "retired"
    except:
        # no description
        is_standard = "incorrect_description"
    
    # only interestined in FHIR version 4
    if not response["FhirVersion"] == 'R4':
        is_standard = "incorrect_verison"
    
    return is_standard

def save_package(package, folder_name):
    packageDict = dict(package)
    response = requests.get(baseUrl + packageDict['Name']).json()
    responseVersions = response['versions']
    responseTarballURL = response['versions'][next(iter(responseVersions))]['dist']['tarball']

    filename = folder_name + responseTarballURL.split("/")[-2] + '.tgz'

    urllib.request.urlretrieve(responseTarballURL, filename)

print("Finding a bunch of packages...")
for c in tqdm(ascii_lowercase):
  
    params = {'name': c}

    # Making a get request
    response = requests.get(baseUrl + 'catalog', params=params)
    
    # print json content
    responseJSON = response.json()
    for response in responseJSON:
        # each response includes "Name", "Description", "FhirVersion"
        is_standard = is_fhir_standard(response)
        
        reasons.append(is_standard)
        if is_standard == 'passed':
            goodPackages.add(frozenset(response.items()))
        else:
            badPackages.add(frozenset(response.items()))

print("out of", len(reasons),"packages")
for reason in set(reasons):
    print(reasons.count(reason), reason)

print("Downloading " + str(len(goodPackages)) + " packages to the good output directory...")
for package in tqdm(goodPackages):
    save_package(package, "output/good/")

print("Downloading " + str(len(badPackages)) + " packages to the bad output directory...")
for package in tqdm(badPackages):
    save_package(package, "output/bad/")