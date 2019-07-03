from bs4 import BeautifulSoup
import os
import csv
path = './nips28/reviews'

ResponsesList=[]
keys=['nips_edition', 'paper_id', 'title','Q1', 'Q2', 'rebuttals' ]

for filename in os.listdir(path):

	soup = BeautifulSoup(open(path+"/"+filename,'rb'))
	table = soup.find( "table", class_='paperHeader' )
	rows = table.findAll(lambda tag: tag.name=='td')
	responses=soup.find_all('div', class_='response')
	i=2
	while i<len(responses):
		Paper=["nips28",rows[1].getText(),rows[3].getText()]
		Paper=Paper+[responses[i-2].getText().replace('\n',''),responses[i-1].getText().replace('\n',''),responses[len(responses)-1].getText().replace('\n','')]
		ResponsesList.append(dict(zip(keys, Paper)))
		i=i+2

with open('nips28results.csv', 'w') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(ResponsesList)
