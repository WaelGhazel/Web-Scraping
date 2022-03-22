import petl
from pprint import pprint
import os
import csv

#import csv file
data = petl.fromcsv("./Assets/Result.csv",encoding="UTF-8")

#removing currency from the price by splitting case by space
data = petl.split(data,'old_price', ' ', ['old_price', 'currency'])
data = petl.split(data,'new_price', ' ', ['new_price', 'currency'])

#selecting only needed data
cols = ['name', 'new_price', 'old_price', 'image']
data = petl.cut(data,cols)

#converting prices from string to float
data = petl.convert(data)
data['new_price']=float
data['old_price']=float

#removing duplicates
data = petl.mergeduplicates(data,["name", "new_price", "old_price", "image"])

#removing old saves
if os.path.exists("./Assets/ResultCleaned.csv"):
  os.remove("./Assets/ResultCleaned.csv")

#creating new clean file
petl.tocsv(data,'./Assets/ResultCleaned.csv',encoding="UTF-8")
pprint(data)