import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import validate

def analizePackages():
    package_meta = validate.validatePackages()

    if not os.path.exists("metadata"):
        os.mkdir("metadata")
    package_meta_copy = package_meta.copy()
    package_meta_copy['dependencies']  = ['; '.join(map(str, l)) for l in package_meta['dependencies']]
    package_meta_copy['resources']  = ['; '.join(map(str, l)) for l in package_meta['resources']]
    package_meta_copy.to_csv("metadata/metadata.csv", index=False)

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

if __name__ == '__main__':
    analizePackages()