import os
import glob
import pandas as pd
os.chdir("/Users/parzavel/Documents/NEA/NEA_CODE/Test/new systems")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')

# reading two csv files
data1 = pd.read_csv('/Users/parzavel/Documents/NEA/NEA_CODE/Test/new systems/city1data.csv')
data2 = pd.read_csv('/Users/parzavel/Documents/NEA/NEA_CODE/Test/new systems/city2data.csv')
  
# using merge function by setting how='inner'
output1 = pd.merge(data1, data2, 
                   on='Susceptible', 
                   how='inner')
  
# displaying result
print(output1)

df = pd.read_csv("/Users/parzavel/Documents/NEA/NEA_CODE/Test/new systems/city1data.csv", usecols = ['Susceptible'])
print(df)