# author manfred scheucher <scheucher@math.tu-berlin.de>

import requests
import requests_cache
from bs4 import BeautifulSoup
import operator

entries = {}

def parse(content):
	soup = BeautifulSoup(content, 'html.parser')
	#dlpage = soup.find("div",{"id": "dlpage"})
	#print(len(dlpage.dl))

	titles = []
	for x in soup.find_all("div", {"class": "list-title"}):
		title = x.text.replace("\n","")
		if 1: title = title.replace("Title: ","")
		titles.append(title)

	identifiers = []
	for x in soup.find_all("span", {"class": "list-identifier"}):
		identifier = x.text
		if 1: identifier = identifier.split()[0]
		if 1: identifier = identifier.replace("arXiv:","")
		identifiers.append(identifier)

	authorss = []
	authors_lists = []
	for x in soup.find_all("div", {"class": "list-authors"}):
		#authors = x.text.replace("\n","")
		#if 1: authors = authors.replace("Authors:","")
		authors = [y.text for y in x.find_all("a")]
		authors_lists.append(authors)
		if 1: 
			if len(authors)>1: 
				authors = ', '.join(authors[:-1])+" & "+authors[-1]
			else:
				authors = authors[0]
		authorss.append(authors)

	subjectss = []
	for x in soup.find_all("div", {"class": "list-subjects"}):
		subjects = x.text.replace("\n","")
		if 1: subjects = [x.split(")")[0] for x in subjects.split("(")[1:]]
		#if 1: subjects = ','.join(y.split(".")[-1] for y in subjects)
		#if 1: subjects = ','.join(subjects)
		subjectss.append(subjects)



	for i in range(len(titles)):
		if identifiers[i] not in entries:

			entries[identifiers[i]] = {
					'id':identifiers[i],
					'title':titles[i],
					'authors':authorss[i],
					'subjects':subjectss[i],
					'sortby':authors_lists[i][0].split()[-1],
				}


def perform():

	output = ''

	subjects = ['math.co','cs.cg','cs.DM']
	output += f"subjects: {subjects}"
	output += "<br><br>"

	#session = requests.Session()
	session = requests_cache.CachedSession('cache',expire_after=360) # seconds

	for s in subjects:
		parse(session.get(f'https://arxiv.org/list/{s}/new').content)


	statistic = {}
	#for ct,entry in enumerate(entries.values()):
	for ct,entry in enumerate(sorted(entries.values(), key=operator.itemgetter('sortby'))):
		output += f"[{ct+1}] "
		output += entry['authors']
		output += "<br>"
		output += f"<a href='http://arxiv.org/abs/{entry['id']}'>{entry['title']}</a>"
		if 0:
			output += "<br>"
			output += f"({','.join(entry['subjects'])})"
			#print((f"({','.join(subjectss[i])})").replace("math.","").replace("cs.",""))
		output += "<br><br>"
		#print(authorss[i],titles[i],identifiers[i])

		for s in entry['subjects']:
			if s not in statistic:
				statistic[s] = 0
			statistic[s] += 1


	if 0:
		output += "statistics"
		output += "<br>"
		for (key,val) in reversed(sorted(statistic.items(), key=operator.itemgetter(1))):
			output += f"{val} x {key}, "

	return output

if __name__ == "__main__":
	with open("out.html","w") as f:
		f.write(perform())
