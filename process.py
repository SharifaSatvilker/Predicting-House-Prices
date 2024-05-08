# This is the code used to run over the 4 AWS EC2 instances to add the count of the crime for that month and postcode
import pandas as pd
import requests
import sys
path = sys.argv[1]

df = pd.read_csv(path)
df.set_index(['postcode','date'], inplace=True)
def get_crime_date(row: pd.Series):
    lat = row['latitude']
    lng = row['longitude']
    date = row.name[1]
    data = requests.get(f'https://data.police.uk/api/crimes-street/all-crime?lat={lat}&lng={lng}&date={date}')
    if data.status_code == 200:
        crime_data = data.json()
        crime_dict = {}
        for crime in crime_data:
            if crime['category'] in crime_dict:
                crime_dict[crime['category']]+=1
            else:
                crime_dict[crime['category']]=1
        for (crime,count) in crime_dict.items():
            row[crime] = count
    return row

df.apply(lambda row: get_crime_date(row),axis=1).to_csv('output.csv')