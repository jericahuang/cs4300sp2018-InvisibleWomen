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
from operator import itemgetter

import en_core_web_sm
nlp = spacy.load('en_core_web_sm')
#import en_core_web_sm
#nlp = en_core_web_sm.load()
#nlp = spacy.load('en_core_web_md')

reload(sys)
sys.setdefaultencoding('utf-8')

project_name = "Invisible Women"
net_id = "Amanda Chen (aec255), Pegah Moradi (pm443), Nina Ray (nr327), Jerica Huang (jh2263), May Zhou (mz278)"

top_5_dict_words = pickle.load( open( "top_5_dict_words.pickle", "rb" ) )
top_5_dict_women = pickle.load( open( "top_5_dict_women.pickle", "rb" ) )
top_5_dict_women_upperkeys = pickle.load( open( "top_5_dict_women_upperkeys.pickle", "rb" ) )
women_name_to_data = pickle.load( open( "women_name_to_data.pickle", "rb" ) )
deduped_women = pickle.load( open( "deduped_women-search.pickle", "rb" ) )

pkl_file = open('myvectorizer.pickle', 'rb')
vectorizer = pickle.load(pkl_file)
matx = pickle.load(pkl_file)

pkl_file_spacy = open('spacyarray.pickle', 'rb')
spacy_array = pickle.load(pkl_file_spacy)

sim_msg = "" # Message returned if cosine sim fails

pkl_file = open('myvectorizer.pickle', 'rb')
vectorizer = pickle.load(pkl_file)
matx = pickle.load(pkl_file)

# From functions, calculates cossim
def cossim_scores(vectorizer, matx, query):
    q_vec = vectorizer.transform([query])
    sim_doc_scores = cosine_similarity(q_vec, matx)
    return sim_doc_scores[0]

# 
def spacysim_scores(spacy_mat, query):
    q = nlp(query)
    sim_scores = np.dot(spacy_mat, q.vector)/((np.linalg.norm(spacy_mat)*np.linalg.norm(q.vector))+1)
    return sim_scores

# user_input is a boolean that tells 
def sort_views_low(input_lst_dict):
	length = len(input_lst_dict)
	if (length > 0) : 
		input_lst_dict = sorted(input_lst_dict, key = itemgetter('views'), reverse = False)
	return input_lst_dict

def sort_views_high(input_lst_dict):
	length = len(input_lst_dict)
	if (length > 0) : 
		input_lst_dict = sorted(input_lst_dict, key= itemgetter('views'), reverse=True)
	return input_lst_dict

# a list of 30 dictionaries, each dictionary has name, summary, and views
# [{woman1: "name", summary1: "summary", views1: "views"} ... {woman30: "name", summary30: "summary", views30: "views"}]
def return_query(cossim_arr, spacysim_arr):
    '''
    cossim_arr : 1D array of cosine similarity scores
    spacysim_arr: 1D array of spacy similarity scores
    data_dict: list of dicts (women)
    
    returns: TUPLE!
    
    return_docs : list of dict with top 30 women (keys are name, summary, views)
    
    '''
    cosine_used = True
    spacy_used = True
    if max(cossim_arr) == 0:
        cosine_used = False
    if max(spacysim_arr) == 0:
        spacy_used = False
    weighted_scores = (cossim_arr*0.7) + (spacysim_arr*0.3)
    sim_docs = np.argsort(weighted_scores)[::-1]
    return_docs = []
    for hit in sim_docs[0:30]:
        return_docs.append(deduped_women[hit])
    return return_docs, cosine_used, spacy_used
    

@irsystem.route('/', methods=['GET'])

def search():
	query = request.args.get('search')
	sorting_mode = request.args.get('sortingmode')
	sim_msg = ""

	sorting=sorting_mode # Sorting by most similar

	if not query:
		data = []
		output_message = ''
	else:
		output_message = query

		if "is similar to " in query:
			woman = query.split("is similar to ")[1].upper()
			if woman in top_5_dict_women_upperkeys:
				data = top_5_dict_women_upperkeys[woman]
			else:
				data = ["Sorry - we did not find a result matching that query."]
				
		elif "is like " in query:
			woman = query.split("is similar to ")[1].upper()
			if woman in top_5_dict_women_upperkeys:
				data = top_5_dict_women_upperkeys[woman]
			else:
				data = ["Sorry - we did not find a result matching that query."]
				
		else:
			s = spacysim_scores(spacy_array, query)
			c = cossim_scores(vectorizer, matx, query)
			data_tuple = return_query(c, s)
			data = data_tuple[0]
			if data_tuple[1] == False:
				sim_msg = "We don't have the exact result you were looking for, but we've done our best to find related results."
			if data_tuple[2] == False:
				data = ["No results :("]

# 			sim_doc_scores = cosine_similarity(q_vec, matx)
# 			sim_docs = np.argsort(sim_doc_scores.flatten())[::-1]
# 			data = []
# #			print sim_docs
# 			for hit in sim_docs:
# 				if sim_doc_scores[0][hit] > 0:
# 					data.append(deduped_women[hit])
# 			if len(data)>30:
# 				data = data[:30]
# 			if len(data)==0:	
# 				data = ["Sorry - we did not find a result matching that query."]

# Data is a list of
                
	
	if data != ["No results :("] and data != ["Sorry - we did not find a result matching that query."] and len(data)>0 and type(data[0]) is not dict:
        
		for i in range(len(data)):
			womanname=data[i]
			data[i] = {"name": womanname, "summary": women_name_to_data[womanname]["summary"], "views": women_name_to_data[womanname]["views"], "url": women_name_to_data[womanname]["url"]}
			if womanname in top_5_dict_women:
				data[i]["similar"] = top_5_dict_women[womanname]

		# mostviewed_data = sort_views_high(data)
		# leastviewed_data = sort_views_low(data)
		# if (sorting=="mostviewed"):
		# 	data = mostviewed_data
		# if (sorting == "leastviewed"):
		# 	data = leastviewed_data
            
	elif data != ["No results :("] and data != ["Sorry - we did not find a result matching that query."] and len(data)>0 and "views" not in data[0] and "similar" not in data[0]:
#		print data
		for i in range(len(data)):
			womanname=data[i]["name"]
			data[i]["views"] = women_name_to_data[womanname]["views"]
			data[i]["similar"] = top_5_dict_women[womanname]
			data[i]["url"] = women_name_to_data[womanname]["url"]

		# mostviewed_data = sort_views_high(data)
		# leastviewed_data = sort_views_low(data)
		# if (sorting=="mostviewed"):
		# 	data = mostviewed_data
		# if (sorting == "leastviewed"):
		# 	data = leastviewed_data
	if (len(data) > 0 and data != ["No results :("] and data != ["Sorry - we did not find a result matching that query."]) :
		mostviewed_data = sort_views_high(data)
		leastviewed_data = sort_views_low(data)
		if (sorting == "mostviewed"):
			data = mostviewed_data
		if (sorting == "leastviewed"):
			data = leastviewed_data
	return render_template('search.html', name=project_name, netid=net_id, output_message=output_message, data=data, query=query, sortingmode=sorting, sim_msg=sim_msg)
