import re

import pandas as pd  # import pandas library

""" Reading Files """
# set poke_file to values within pokemon_data.csv
poke_file = pd.read_csv('pokemon_data.csv')
# poke_file_xcell = pd.read_excel('pokemon_data.xlsx')

# When importing a tab seperated file, we have to include the delimiter aspect so python knows when to creat a column
# poke_file_txt = pd.read_csv('pokemon_data.txt', delimiter='\t')

# print(poke_file_txt.head(3))
# print(poke_file_xcell.head(3)) #we Can look at first three rows
# print(poke_file.tail(3)) #we can look at last three rows

""" Reading Data in Pandas """
## Reading headers
# print(poke_file.columns)

## Reading each column
# print(poke_file['Name'][0:5]) # print names column only for first five of dataframe
# print(poke_file[['Name', 'HP', 'Type 1'][0:5]]) # print multiple columns

## Read Each row
# print(poke_file.iloc[1]) #iloc = imageing location- gives back everything in first row of data
# print(poke_file.iloc[0:3]) #return first three rows of data

# iterate through table and pull all columns data in index and Name only
# for index, row in poke_file.iterrows():
#    print(index, row['Name'])

# filters and prints all row data where each pokemon is a grass type
# .loc is used for finding specific data in data set based on textural information
# print(poke_file.loc[(poke_file['Type 1'] == 'Grass')])
# print(poke_file.loc[(poke_file['Type 1'] == 'Grass') & (poke_file['Generation'] == 1)])

## Read a specific location (Row,Column)
# print(poke_file.iloc[2, 1]) # we want to return the exact data at a specified point (Row,Column) -> Venasaur in 2nd row 1st Column

"""Sorting and Describing Data"""
# gives us high level stats of data (avg,mean,standard deviation, min, max)
# print(poke_file.describe())

# sort by names in descending order and show top 10 results
# print(poke_file.sort_values('Name', ascending = False).head(10))

# Sort by multiple column types
# print(poke_file.sort_values(['Name', 'HP']))

# Sort ascending Name with Descending Generation
# print(poke_file.sort_values(['Name', 'Generation'], ascending=[1, 0]))

""" Making Changes to the data """
print(poke_file.head(5))

# add a total column which adds all the HP, attack info together for each pokemon - We can possibly use this to rank pokemon
poke_file['Total'] = poke_file['HP'] + poke_file['Attack'] + poke_file['Defense'] + poke_file['Sp. Atk'] + \
                     poke_file['Sp. Def'] + poke_file['Speed']

# another way to do this is:

# Based on column and row number, we will use iloc to grab columns 4->9 and add them together horizontally (AKA axis = 1)
# AXIS = 0 is add vertically
# the iloc[:, 4:10] -> : means grab all rows, 4:10 means grab only columns 4,5,6,7,8,9 *10 IS EXCLUDED
# poke_file['Total'] = poke_file.iloc[:, 4:10].sum(axis=1)

# print(poke_file.head(5))

# we can drop data from the table
poke_file.drop('Total', axis=1, inplace=True)
# The axis argument specifies whether to drop rows (0) or columns (1).
# The inplace argument specifies to drop the columns in place without reassigning the DataFrame.

""" Saving our Data (Exporting into desired Format """

# poke_file['Total'] = poke_file.iloc[:, 4:10].sum(axis=1)
# poke_file.to_csv("modified.csv", index=False) # index number is removed (usually in first column
# poke_file.to_excel("modified.xlsx", index=False)
# poke_file.to_csv("modified.tct", index=False, sep='\t') # save to text file with data separated by tabs

""" Filtering Data """

poke_file.loc[poke_file['Type 1'] == 'Grass']

# two conditions seperated by parenthasis, within pandas we use & vs and, | -> or vs or
filter_data = poke_file.loc[(poke_file['Type 1'] == 'Grass') & (poke_file['Type 2'] == 'Poison') & (poke_file['HP'] > 70)]
print(filter_data)

# we filtered the data, however the new dataframe kept the old indexes in the first row, we want to reset the index's
# filter_data = filter_data.reset_index()

# by default, this will save the old index alongside the new index values
# if we dont want this
filter_data.reset_index(drop=True, inplace=True)
# now we have our filtered data, set to a new dataframe variable with new index's and got rid of the old (using inline,
# will use less data
# print(filter_data)

#filter names of pokemon with only mega names
# print(poke_file.loc[poke_file['Name'].str.contains('Mega')])

# We can also filter it out using "~"
# print(poke_file.loc[~poke_file['Name'].str.contains('Mega')])

""" RegX funcations """
# import re

# We can filter for fire and grass pokemon only using regular expressions
print(poke_file.loc[poke_file['Type 1'].str.contains('Fire|Grass', regex=True)])

# We want to filter only pokemon names starting with Pi
# regex - ^ -> beginning on line, [a-z] -> next set of letters can be characters a - z, * means 1 or more values after pi
# flags ignore case sensitivy
print(poke_file.loc[poke_file['Name'].str.contains('^Pi[a-z]*', flags=re.I, regex=True)])

""" Conditional Changes - Changes data frame based on conditions we filtered out by"""

# Say we want to change the name of the fire in type 1 too flameboy
poke_file.loc[poke_file['Type 1'] == 'Fire', 'Type 1'] = 'Flameboy'
print(poke_file)

# We can change multiple columns values
# Say we want to change the Generation and Legendary field based on the total value being over 500
poke_file = pd.read_csv('modified.csv')
poke_file.loc[poke_file['Total'] > 500, ['Generation', "Legendary"]] = ["Test", "Value"]
print(poke_file)

""" Aggregate Statistics (Groubby) mean, sum, count """
poke_file = pd.read_csv('modified.csv')

# Want to see avg HP and attack of all the pokemon
print(poke_file.groupby(['Type 1']).mean())

# We want to see which group of pokemon has the highest average attack in Desc order.
# mean() calculates average, sort_value() sorts list by certain column in asc od desc order
print(poke_file.groupby(['Type 1']).mean().sort_values('Attack', ascending=False))

# We want to count how many pokemon are in each category.
# We want to create a seperate column for each pokemon enterance with the value of one due to type 2 values
poke_file['Count'] = 1
print(poke_file.groupby(['Type 1']).count()['Count'])

# We can group 2 columns together
print(poke_file.groupby(['Type 1', 'Type 2']).count()['Count'])
