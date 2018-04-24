# -*- coding: utf-8 -*-

from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

import sys
import pickle
reload(sys)
sys.setdefaultencoding('utf-8')

project_name = "Invisible Women"
net_id = "Amanda Chen (aec255), Pegah Moradi (pm443), Nina Ray (nr327), Jerica Huang (jh2263), May Zhou (mz278)"

top_5_dict_words = pickle.load( open( "top_5_dict_words.pickle", "rb" ) )
top_5_dict_women = pickle.load( open( "top_5_dict_women.pickle", "rb" ) )
women_name_to_data = pickle.load( open( "women_name_to_data.pickle", "rb" ) )

@irsystem.route('/', methods=['GET'])


def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "You searched for a woman who " + query
		
		if query in top_5_dict_words:
			data = top_5_dict_words[query]
			
		elif "is similar to " in query:
			woman = query.split("is similar to ")[1]
			woman = woman.title()
			if woman in top_5_dict_women:
				data = top_5_dict_women[woman]
			else:
				data = ["No results :("]
				
		elif "is like " in query:
			woman = query.split("is like ")[1]
			woman = woman.title()
			if woman in top_5_dict_women:
				data = top_5_dict_women[woman]
			else:
				data = ["No results :("]
				
		elif "is an " in query:
			word = query.split("is an ")[1]
			if word in top_5_dict_words:
				data = top_5_dict_words[word]
			else:
				data = ["No results :("]
		elif "is a " in query:
			word = query.split("is a ")[1]
			if word in top_5_dict_words:
				data = top_5_dict_words[word]
			else:
				data = ["No results :("]
				
		elif "is " in query:
			woman = query.split("is ")[1]
			if woman in top_5_dict_women:
				data = top_5_dict_women[woman]
			elif woman in top_5_dict_words:
				data = top_5_dict_words[woman]
			elif woman.title() in top_5_dict_women:
				data = [woman.title()]
				data = data + top_5_dict_women[woman.title()]
			else:
				data = ["No results :("]
				
		else:
			data = ["No results :("]
   
	if data != ["No results :("] and type(data[0]) is not dict:
		for i in range(len(data)):
			womanname=data[i]
			data[i] = {"name": womanname, "summary": women_name_to_data[womanname]["summary"], "views": women_name_to_data[womanname]["views"]}
			if womanname in top_5_dict_women:
				data[i]["similar"] = top_5_dict_women[womanname]
				
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)