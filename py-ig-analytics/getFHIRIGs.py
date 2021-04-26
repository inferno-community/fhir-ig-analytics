import json
import dateutil.parser
import os
import shutil
import urllib.request
from tqdm import tqdm

def getPackages():
    with open('qas.json') as f:
        data = json.load(f) #Load the JSON

    sorted_data = sorted(data, key=lambda x: dateutil.parser.parse(x['date']), reverse=True) #Sort by most recent

    seen = set()
    igs = []

    for ig in sorted_data:
        if ig["package-id"] not in seen: #Take the most recent version of the package, skip duplicates
            seen.add(ig["package-id"])
            igs.append(ig)

    if os.path.exists('../output'):
            print("Warning: Output folder with downloads already exists.")
            user = input("Would you like to delete and download again? Y/N: ")
            if user == "Y" or user == "y":
                shutil.rmtree('../output')
            else:
                print("Aborted")
                quit()
            
    os.makedirs('../output')

    for ig in tqdm(igs):
        baseURL = "https://build.fhir.org/ig/"
        packageURL = ig['repo'].replace("qa.json","package.tgz")

        try:
            filename = "../output/" + ig["name"] + '.tgz'
        except:
            filename = "../output/" + ig['package-id'] + '.tgz'

        try:
            urllib.request.urlretrieve(baseURL+packageURL, filename)
        except:
            print(ig["name"] + " could not be found.")

if __name__ == '__main__':
    getPackages()