import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import validate

def analizePackages():

    package_meta = pd.read_csv("../metadata/metadata.csv")

    for i in range(0,package_meta.shape[0]):
        package_meta['dependencies'].iloc[i] = package_meta['dependencies'].iloc[i].strip("[").strip(']').replace("'", "").split(", ")
        package_meta['resources'].iloc[i] = package_meta['resources'].iloc[i].strip("[").strip(']').replace("'", "").split(", ")
        package_meta['resource_types'].iloc[i] = package_meta['resource_types'].iloc[i].strip("[").strip(']').replace("'", "").split(", ")


    package_meta_copy = package_meta.copy()
    package_meta_copy['dependencies']  = ['; '.join(map(str, l)) for l in package_meta_copy['dependencies']]
    package_meta_copy['resources']  = ['; '.join(map(str, l)) for l in package_meta_copy['resources']]
    package_meta_copy['resource_types']  = ['; '.join(map(str, l)) for l in package_meta_copy['resource_types']]
    package_meta_copy.to_csv("../metadata/metadata.csv", index=False)

    # save basic seaborn plot of metadaata
    fig, ax = plt.subplots(figsize=[15,5])
    fig = sns.histplot(data=package_meta, x='status').get_figure()
    fig.savefig("../metadata/metadata_hist.png")

    all_dependencies = []
    for i in range(len(package_meta.query("status == 'passed'")['dependencies'])):
        for dependency in package_meta.query("status == 'passed'")['dependencies'].iloc[i]:
            all_dependencies.append(dependency)
            
    dependancies = pd.DataFrame({"dependency": all_dependencies})
    dependancies['count'] = 1
    dependancies = dependancies.groupby(['dependency'], as_index=False)['count'].sum()
    dependancies = dependancies.sort_values("count", ascending=False)
    fig, ax = plt.subplots(figsize=[25,5])
    fig = sns.barplot(data=dependancies.head(10), x='dependency', y='count').get_figure()
    fig.savefig("../metadata/dependancies_hist.png")
    dependancies.to_csv("../metadata/dependency_usage_hist.csv", index=False)

    all_resources = []
    for i in range(len(package_meta.query("status == 'passed'")['resources'])):
        for resource in package_meta.query("status == 'passed'")['resources'].iloc[i]:
            all_resources.append(resource)
            
    resources = pd.DataFrame({"resource": all_resources})
    resources['count'] = 1
    resources = resources.groupby(['resource'], as_index=False)['count'].sum()
    resources = resources.sort_values("count", ascending=False)
    fig, ax = plt.subplots(figsize=[30,5])
    fig = sns.barplot(data=resources.head(10), x='resource', y='count').get_figure()
    fig.savefig("../metadata/resource_usage_hist.png")
    resources.to_csv("../metadata/resource_usage.csv", index=False)

    all_resource_types = []
    for i in range(len(package_meta.query("status == 'passed'")['resource_types'])):
        for resource in package_meta.query("status == 'passed'")['resource_types'].iloc[i]:
            all_resource_types.append(resource)
            
    resource_types = pd.DataFrame({"resource_type": all_resource_types})
    resource_types['count'] = 1
    resource_types = resource_types.groupby(['resource_type'], as_index=False)['count'].sum()
    resource_types = resource_types.sort_values("count", ascending=False)
    fig, ax = plt.subplots(figsize=[25,5])
    fig = sns.barplot(data=resource_types.head(10), x='resource_type', y='count').get_figure()
    fig.savefig("../metadata/resource_types_hist.png")
    resource_types.to_csv("../metadata/resource_types.csv", index=False)

if __name__ == '__main__':
    analizePackages()