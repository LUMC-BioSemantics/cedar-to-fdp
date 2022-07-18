import json
import requests
import pandas as pd
import FDPClient
import Config
import chevron

FDP_CLIENT = FDPClient.FDPClient(Config.FDP_URL, Config.FDP_USERNAME, Config.FDP_PASSWORD, Config.FDP_PERSISTENT_URL)

def cedar_to_fdp(name):
    template_ids = [Config.CEDAR_TEMPLATE_ID]
    templ_url = Config.CEDAR_TEMPLATE_URL
    beg_url = Config.CEDAR_BEG_URL
    headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': Config.CEDAR_API_KEY}

    all_instances = []
    # Retrieve instances from CEDAR (Ask Aliya for logic of this code block)
    for template_id in template_ids:
        r = requests.get(templ_url + template_id, {'limit': 500}, headers=headers)
        templ_data = json.loads(r.content)
        for items in templ_data['resources']:
            url_crt = beg_url + items['@id'][51:]
            print(url_crt)
            r = requests.get(url_crt, headers=headers)
            content = json.loads(r.content)
            all_instances.append(content)
    df_instances = pd.DataFrame(all_instances)

    dict_columns = ['@context', 'Name of the Lead Institution', 'Country', 'acronym',
       'homepage', 'has Funder Name', 'title', 'startDate', 'endDate', 'ORCID',
       'identifier']

    for col in dict_columns:
        df_instances[col] = df_instances[col].apply(lambda x: dict(x).get('@value'))

    # Populate FDP with CEDAR instances
    for index, row in df_instances.iterrows():
        title = row['title']
        acronym = row['acronym']
        endDate = row['endDate']
        identifier = row['identifier']
        startDate = row['startDate']
        homepage = row['homepage']
        ORCID = row['ORCID']
        # Replace place holders in mutache with values from CEDAR instance
        with open('templates/project.mustache', 'r') as f:
            post_body = chevron.render(f, {'title': title, 'acronym': acronym, 'endDate': endDate,
                                           'identifier': identifier, 'startDate': startDate, 'homepage': homepage,
                                           'ORCID': ORCID})
        print(post_body)
        # Publish project in FDP
        project_url = FDP_CLIENT.fdp_create_metadata(post_body, "project")
        print(project_url)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    cedar_to_fdp('PyCharm')
