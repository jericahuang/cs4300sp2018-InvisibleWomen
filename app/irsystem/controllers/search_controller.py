# -*- coding: utf-8 -*-

from . import *  
from app.irsystem.models.helpers import *
from app.irsystem.models.helpers import NumpyEncoder as NumpyEncoder

import sys
import pickle
import scipy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import spacy
nlp = spacy.load('en_core_web_md')

reload(sys)
sys.setdefaultencoding('utf-8')

project_name = "Invisible Women"
net_id = "Amanda Chen (aec255), Pegah Moradi (pm443), Nina Ray (nr327), Jerica Huang (jh2263), May Zhou (mz278)"

top_5_dict_words = pickle.load( open( "top_5_dict_words.pickle", "rb" ) )
top_5_dict_women = pickle.load( open( "top_5_dict_women.pickle", "rb" ) )
women_name_to_data = pickle.load( open( "women_name_to_data.pickle", "rb" ) )
deduped_women = pickle.load( open( "deduped_women-search.pickle", "rb" ) )
pkl_file_spacy = open('spacyarray.pickle', 'rb')
pkl_file = open('myvectorizer.pickle', 'rb')
vectorizer = pickle.load(pkl_file)
matx = pickle.load(pkl_file)
spacy_array = pickle.load(pkl_file_spacy)



def cossim_scores(vectorizer, matx, query, data_dict):
    q_vec = vectorizer.transform([query])
    sim_doc_scores = cosine_similarity(q_vec, matx)
    return sim_doc_scores[0]

def spacysim_scores(spacy_mat, query, data_dict):
    q = nlp(query)
    sim_scores = np.dot(spacy_mat, q.vector)/((np.linalg.norm(spacy_mat)*np.linalg.norm(q.vector))+1)
    return sim_scores

def return_query(cossim_arr, spacysim_arr, data_dict):

    cosine_used = True
    spacy_used = True
    if max(cossim_arr) == 0:
        cosine_used = False
    if max(spacysim_arr) == 0:
        spacy_used = False
    weighted_scores = cossim_arr*0.7 + spacysim_arr*0.3
    sim_docs = np.argsort(weighted_scores)[::-1]
    return_docs = []
    for hit in sim_docs[0:30]:
        return_docs.append(data_dict[hit])
    return return_docs, cosine_used, spacy_used


@irsystem.route('/', methods=['GET'])

def search():
	query = request.args.get('search')
	if not query:
		data = []
		output_message = ''
	else:
		output_message = "You searched for a woman who " + query + "."
		q_vec = vectorizer.transform([query])

		if "is similar to " in query:
			woman = query.split("is similar to ")[1]
			woman = woman.title()
			if woman in top_5_dict_women:
				data = top_5_dict_women[woman]
			else:
				data = ["We don't have data on that person. :( Check back soon!"]
				
		elif "is like " in query:
			woman = query.split("is like ")[1]
			woman = woman.title()
			if woman in top_5_dict_women:
				data = top_5_dict_women[woman]
			else:
				data = ["We don't have data on that person. :( Check back soon!"]
				
		else:
			s = spacysim_scores(spacy_array, query, deduped_women)
			c = cossim_scores(vectorizer, matx, query, deduped_women)
			data_tuple = return_query(c, s, deduped_women)
			data = list(data_tuple[0])
			if data_tuple[1] == False:
				# This means that cosine sim was not used
				# PRINT SOMETHING HERE ? (HOW?)
				output_message += "<br />" + "We don't have the exact result you were looking for, but we've done our best to find possible related results."
			if data_tuple[2] == False:
				# This means that spacy sim was not used
				# PRINT SOMETHING HERE ? (HOW?)
				data = ["No results :("]
	
	if data != ["No results :("] and data != ["We don't have data on that person. :( Check back soon!"] and len(data)>0 and type(data[0]) is not dict:
		for i in range(len(data)):
			womanname=data[i]
			data[i] = {"name": womanname, "summary": women_name_to_data[womanname]["summary"], "views": women_name_to_data[womanname]["views"], "url": women_name_to_data[womanname]["url"]}
			if womanname in top_5_dict_women:
				data[i]["similar"] = top_5_dict_women[womanname]
	elif data != ["No results :("] and data != ["We don't have data on that person. :( Check back soon!"] and len(data)>0 and "views" not in data[0] and "similar" not in data[0]:
		print data
		for i in range(len(data)):
			womanname=data[i]["name"]
			data[i]["views"] = women_name_to_data[womanname]["views"]
			data[i]["similar"] = top_5_dict_women[womanname]
			data[i]["url"] = women_name_to_data[womanname]["url"]
	
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data)