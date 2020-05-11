import string,os
from django.conf import settings
import pandas as pd

def perform(text):
    text = text.translate(str.maketrans('', '', string.punctuation))
    store = [i.strip().lower() for i in text.split(" ")]
    my_input_file = open(os.path.join(settings.MEDIA_ROOT, 'groceries.csv'), 'r')
    items = set()
    storage = []
    for line in my_input_file:
        line = [i.strip() for i in line.split(',')]
        storage.append(" ".join(line))
        for every in line:
            items.add(every)
    smalltext = " ".join(storage)
    smalltext = smalltext.translate(str.maketrans('', '', string.punctuation))
    products = list(smalltext.split(" "))
    products.append("pulses")
    hold = list(set(products) & set(store))
    
    temp_lis = []
    for each in items:
        temp_lis.append(each)

    gg = pd.Series(temp_lis)

    essentials = set()
    for every in hold:
        demo = list(gg[gg.str.contains(every)])
        if len(demo) > 0:
            for each in demo:
                essentials.add(each)
    return essentials
