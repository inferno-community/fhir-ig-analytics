import json
import os
import pandas as pd
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

def validatePackages():
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
    return package_meta

if __name__ == '__main__':
    validatePackages()