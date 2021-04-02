import requests
from string import ascii_lowercase
from tqdm import tqdm
import os
import shutil
import urllib.request 

allPackages = set()
baseUrl = 'https://packages.fhir.org/'

if os.path.exists('output'):
    print("Output folder already exists. Deleting.")
    shutil.rmtree('output')
os.makedirs('output')

print("Finding a bunch of packages...")
for c in tqdm(ascii_lowercase):
  
    params = {'name': c}

    # Making a get request
    response = requests.get(baseUrl + 'catalog', params=params)
    
    # print json content
    responseJSON = response.json()
    for response in responseJSON:
        allPackages.add(frozenset(response.items()))

print("Downloading " + str(len(allPackages)) + " packages to output directory...")
for package in tqdm(allPackages):
    packageDict = dict(package)
    response = requests.get(baseUrl + packageDict['Name']).json()
    responseVersions = response['versions']
    responseTarballURL = response['versions'][next(iter(responseVersions))]['dist']['tarball']

    filename = "output/" + responseTarballURL.split("/")[-2] + '.tgz'

    urllib.request.urlretrieve(responseTarballURL, filename)

