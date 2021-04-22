import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tarfile

# checks from https://wiki.hl7.org/FHIR_NPM_Package_Spec
def check_for_required_json_packages(package):
    if not "package/package.json" in package.getnames():
        return "missing package.json"
    
    elif not "package/.index.json" in package.getnames():
        return "missing index.json"

    return "passed"

def check_package_manifest(package):
    manifest = package.extractfile("package/package.json")
    manifest_text = json.loads(manifest.read())
    mandatory_keys = ['name','version','description','dependencies','author']
    if not set(mandatory_keys).issubset(set(manifest_text.keys())):
        return "missing mandatory manifest key", []
    
    dependencies = list(manifest_text['dependencies'].keys())
    return "passed", dependencies

def check_for_at_least_one_dependency(package, resources):
    # more care needed here. some are examples or other non-dependency files
    for json_file in package.getnames():
        if not json_file in ["package/package.json","package/.index.json"]:
            string = json_file.strip("package/").strip(".json")
            if "/" not in string:
                resources.append(string)
    if len(resources) == 0:
        return "no dependencies", []
    return "passed", resources

all_packages = os.listdir('output')
package_meta = pd.DataFrame(columns=['package_name', "status", "dependencies"])
for package_name in all_packages:
    package_dependencies = [] 
    package_resources = []
    try:
        package = tarfile.open(f"output/{package_name}")
        # check to make sure the package has the required json files
        status = check_for_required_json_packages(package)
        if status == "passed":
            # check to make sure the package.json has the correct fields
            status, package_dependencies = check_package_manifest(package)
        if status == "passed":
            # find the dependencies of each package
            status, package_resources = check_for_at_least_one_dependency(package, package_resources)
        # find packages in the folder that aren't found in the description
        if status == "passed":
            if len(package_dependencies) == 0:
                status = f"no dependencies found"
        # add name, status, and dependencies to meta
        package_meta = package_meta.append({"package_name":package_name,
                                            "status":status, 
                                            "dependencies":package_dependencies,
                                            "resources":package_resources},
                                           ignore_index=True)
        package.close()
    except:
        # this is where the broken packages go to be forgotten forever
        package_meta = package_meta.append({"package_name":package_name, 
                                            "status":"broken_package",
                                            "dependencies":package_dependencies},
                                            ignore_index=True) 
        
if not os.path.exists("metadata"):
    os.mkdir("metadata")
package_meta.to_csv("metadata/metadata.csv", index=False)

# save basic seaborn plot of metadaata
fig, ax = plt.subplots(figsize=[15,5])
fig = sns.histplot(data=package_meta, x='status').get_figure()
fig.savefig("metadata/metadata_hist.png")

all_dependencies = []
for i in range(len(package_meta.query("status == 'passed'")['dependencies'])):
    for dependency in package_meta.query("status == 'passed'")['dependencies'].iloc[i]:
        all_dependencies.append(dependency)
        
dependancies = pd.DataFrame({"dependency": all_dependencies})
dependancies['count'] = 1
dependancies = dependancies.groupby(['dependency'], as_index=False)['count'].sum()
dependancies = dependancies.sort_values("count", ascending=False)
dependancies.to_csv("metadata/dependency_usage.csv", index=False)



all_resources = []
for i in range(len(package_meta.query("status == 'passed'")['resources'])):
    for resource in package_meta.query("status == 'passed'")['resources'].iloc[i]:
        all_resources.append(resource)
        
resources = pd.DataFrame({"resource": all_resources})
resources['count'] = 1
resources = resources.groupby(['resource'], as_index=False)['count'].sum()
resources = resources.sort_values("count", ascending=False)
resources.to_csv("metadata/resource_usage.csv", index=False)
