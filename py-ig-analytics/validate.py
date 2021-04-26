import json
import os
import pandas as pd
import tarfile

# checks from https://wiki.hl7.org/FHIR_NPM_Package_Spec
def check_for_required_json_files(package):
    if not "package/package.json" in package.getnames():
        return "missing package.json"
    
    elif not "package/.index.json" in package.getnames():
        return "missing index.json"

    return "passed"

def check_package_file_content(package):
    manifest = package.extractfile("package/package.json")
    manifest_text = json.loads(manifest.read())
    mandatory_keys = ['name','version','description','dependencies','author']
    if not set(mandatory_keys).issubset(set(manifest_text.keys())):
        return "missing mandatory manifest key", []
    
    dependencies = list(manifest_text['dependencies'].keys())
    return "passed", dependencies

def check_resources(package, resources, resource_types):
    # more care needed here. some are examples or other non-dependency files
    for json_file in package.getnames():
        if not json_file in ["package/package.json","package/.index.json"]:
            string = json_file.strip("package/").strip(".json")
            if "/" not in string:
                resources.append(string)
                try:
                    resource = package.extractfile(json_file)
                    resource_text = json.loads(resource.read())
                    resource_types.append(resource_text['resourceType'])
                except:
                    resource_types.append("Not an actual resource")
    if len(resources) == 0:
        return "no dependencies", [], []
    return "passed", resources, resource_types

def validatePackages():
    all_packages = os.listdir('../output')
    package_meta = pd.DataFrame(columns=['package_name', "status", "dependencies"])
    for package_name in all_packages:
        package_dependencies = [] 
        package_resources = []
        package_resource_types = []

        try:
            package = tarfile.open(f"../output/{package_name}")
            # check to make sure the package has the required json files
            status = check_for_required_json_files(package)
            if status == "passed":
                # check to make sure the package.json has the correct fields
                status, package_dependencies = check_package_file_content(package)
            if status == "passed":
                # find the dependencies of each package
                status, package_resources, package_resource_types = check_resources(package, package_resources, package_resource_types)
            # find packages in the folder that aren't found in the description
            if status == "passed":
                if len(package_dependencies) == 0:
                    status = f"no dependencies found"
            # add name, status, and dependencies to meta

            package_meta = package_meta.append({"package_name":package_name,
                                                "status":status, 
                                                "dependencies":package_dependencies,
                                                "resources":package_resources,
                                                "resource_types": package_resource_types},
                                            ignore_index=True)
            package.close()
        except:
            # this is where the broken packages go to be forgotten forever
            package_meta = package_meta.append({"package_name":package_name, 
                                                "status":"broken_package",
                                                "dependencies":package_dependencies,
                                                "resources":package_resources,
                                                "resource_types": package_resource_types},
                                                ignore_index=True)
    # save the package metadata
    if not os.path.exists("../metadata"):
        os.mkdir("../metadata")
    package_meta.to_csv("../metadata/metadata.csv")

if __name__ == '__main__':
    validatePackages()