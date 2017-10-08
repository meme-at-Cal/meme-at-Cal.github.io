
import calendar
import operator
import json
from PIL import Image
from pprint import pprint 
from flask import Flask
from flask import request
from flask import render_template
import unicodedata






class Meme:
	def __init__(self, meme):
		self.image = meme["image"] #need to process URL
		#self.author = meme["author"]
		self.text = meme["description_text"].lower()
		self.time = meme["time"]#need to process time
		self.like = meme["hotness"]
		if "others" in self.like or "K" in self.like:
			if "K " in self.like:
				result = ""
				numlst = list(filter(str.isdigit, self.like))
				for i in numlst:
					result += i
				self.like = int(result)*100
			else:
				result = ""
				numlst = list(filter(str.isdigit, self.like))
				for i in numlst:
					result += i
				self.like  = int(result)
		else:
			self.like = int(self.like)
		#self.comment = int(meme["comment"])
		#self.share = int(meme["share"])

def sortbylikeness(): 
	disc = {}

	for  i in meme_array:

		disc[i.like] = i.image

	sorted_disc = sorted(disc.items(), key=operator.itemgetter(0))
	result = []
	for i in sorted_disc:
		result = [i[1]]+ result
	return result

def sortbytime():
	disc = {}
	mapmonth = {v: k for k,v in enumerate(calendar.month_abbr)}
	for i in meme_array:
		string = i.time.split(None,1)[1] #get rid of day in week
		stringlst = string.split()
		stringlst[0] = str(mapmonth[stringlst[0][:3]]) # change to Oct to 10
		if len(stringlst[0]) == 1:
			stringlst[0] = "0" + stringlst[0] #the edge case for Jan to 01
		if stringlst[-1][5:7] == 'pm' and stringlst[-1][:2] != "12":
			stringlst[-1] = str(int(stringlst[-1][:2])+12)+stringlst[-1][3:5]
		else:
			stringlst[-1] = stringlst[-1][:2]+stringlst[-1][3:5] #change the last digit

		intdate = stringlst[2] + stringlst[0] + stringlst[1] + stringlst[-1]

		disc[intdate] = i.image

	sorted_disc = sorted(disc.items(), key=operator.itemgetter(0))
	result = []
	for i in sorted_disc:
		result = [i[1]]+ result


	return result


def search(string):#implement long string and capital
	string = string.lower()
	result = set()
	for i in meme_array:
		datalst = i.text.split()
		searchlst = string.split()
		flag = False
		for j in searchlst:
			if j in datalst:
				flag = True
			else:
				flag = False
				break;
		if flag:
			result.add(i.image)
				
	return result

with open('data_with_description.json') as data_file:    
    data = json.load(data_file) # maybe loads


meme_array = []


for i in data.values():
	meme_array.append(Meme(i[0]))


#for j in meme_array:
	#print(j.like)



	
"""
meme1 = {"image":"url1", 
		"author":"alex",
		"text":"UC Berkeley Meme Page Start",
		"like":"200",
		"comment":"300",
		"share":"400" ,
		"time":"Friday, October 6, 2017 at 9:11pm "
		}
meme2 = {"image":"url2", 
		"author":"betty",
		"text":"UC Davis Gonna Die",
		"like":"500",
		"comment":"300",
		"share":"400" ,
		"time":"Sunday, November 6, 2014 at 12:50pm "
		}


meme_array = [Meme(meme1), Meme(meme2)]
"""


app = Flask(__name__)

@app.route('/')
def my_form():
	return render_template('memes.html')

@app.route('/', methods=['POST'])
def my_form_post():
	if 'choice' in request.form:
		if request.form['choice'] == 'recent':
			return render_template('memes.html', objects=sortbytime())
		else:
			return render_template('memes.html', objects=sortbylikeness())
	else:
		text1=request.form['text1']
		print(search(text1))
		return render_template('memes.html', objects=search(text1))

if __name__ == '__main__':
	app.run()


