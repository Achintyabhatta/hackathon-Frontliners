import string,os
from django.conf import settings
import pandas as pd
import csv

def perform(essentials):
    df = pd.read_csv(os.path.join(settings.MEDIA_ROOT, 'all_rules.csv'))
    mydata = {}
    for index,row in df.iterrows():
        for each in row['ordered_product'].split(','):
            if each not in mydata.keys():
                mydata[each] = set()
            mydata[each].add(row['recommended_product'])
    recommended = set()
    print(essentials)
    for each in essentials:
        if each in mydata.keys():
            for every in mydata[each]:
                if every not in essentials:
                    recommended.add(every)
    return recommended