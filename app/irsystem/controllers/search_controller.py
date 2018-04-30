# -*- coding: utf-8 -*-

from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

import sys
import pickle
import scipy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
reload(sys)
sys.setdefaultencoding('utf-8')

project_name = "Invisible Women"
net_id = "Amanda Chen (aec255), Pegah Moradi (pm443), Nina Ray (nr327), Jerica Huang (jh2263), May Zhou (mz278)"

top_5_dict_words = pickle.load( open( "top_5_dict_words.pickle", "rb" ) )
top_5_dict_women = pickle.load( open( "top_5_dict_women.pickle", "rb" ) )
women_name_to_data = pickle.load( open( "women_name_to_data.pickle", "rb" ) )
deduped_women = pickle.load( open( "deduped_women-search.pickle", "rb" ) )
pkl_file = open('myvectorizer.pickle', 'rb')
vectorizer = pickle.load(pkl_file)
matx = pickle.load(pkl_file)

@irsystem.route('/', methods=['GET'])

def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "You searched for a woman who " + query
		q_vec = vectorizer.transform([query])

		if "is similar to " in query:
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
				
		else:
			sim_doc_scores = cosine_similarity(q_vec, matx)
			sim_docs = np.argsort(sim_doc_scores.flatten())[::-1]
			data = []
#			print sim_docs
			for hit in sim_docs:
				if sim_doc_scores[0][hit] > 0:
					data.append(deduped_women[hit])
			if len(data)>30:
				data = data[:30]
			
			if len(data)==0:	
				data = ["No results :("]
	
	if data != ["No results :("] and len(data)>0 and type(data[0]) is not dict:
		for i in range(len(data)):
			womanname=data[i]
			data[i] = {"name": womanname, "summary": women_name_to_data[womanname]["summary"], "views": women_name_to_data[womanname]["views"], "url": women_name_to_data[womanname]["url"]}
			if womanname in top_5_dict_women:
				data[i]["similar"] = top_5_dict_women[womanname]
	elif data != ["No results :("] and len(data)>0 and "views" not in data[0] and "similar" not in data[0]:
#		print data
		for i in range(len(data)):
			womanname=data[i]["name"]
			data[i]["views"] = women_name_to_data[womanname]["views"]
			data[i]["similar"] = top_5_dict_women[womanname]
			data[i]["url"] = women_name_to_data[womanname]["url"]
	
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)