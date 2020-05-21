import sys
import os
from whoosh.qparser import QueryParser, OrGroup
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.query import FuzzyTerm
from gensim.parsing.preprocessing import strip_non_alphanum
from gensim.parsing.preprocessing import strip_multiple_whitespaces

# index_path = os.path.join('indexers', 'FAQs')
# ix = open_dir(index_path)

# # query_str is query string
# query_str = sys.argv[1]
# query_str = strip_non_alphanum(query_str)
# query_str = strip_multiple_whitespaces(query_str)

# # Top 'n' documents as result
# topN = int(sys.argv[2])

# with ix.searcher(weighting=scoring.BM25F) as searcher:
#     query = QueryParser("question", ix.schema, termclass=FuzzyTerm).parse(query_str)
#     try:
#         results = searcher.search(query,limit=topN)
#         for i in range(topN):
#                 print(results[i]['question'], results[i]['response'], str(results[i].score))
#     except IndexError:
#         print("No match found!")

def query_indexer(query_string, directory, topN=30):
	'''
	query_string - sentence used to perform the search.
	directory - location of the indexer to be used.
	topN - number of documents returned by the query. The default is 30.
	'''
	ix = open_dir(directory)

	query_string = strip_non_alphanum(query_string)
	query_string = strip_multiple_whitespaces(query_string)

	with ix.searcher(weighting=scoring.BM25F) as searcher:
	# with ix.searcher(weighting=scoring.Frequency) as searcher:
		query = QueryParser("question", ix.schema, termclass=FuzzyTerm, group=OrGroup).parse(query_string)
		try:
			options = []
			options_answers = []
			loop_range = 0

			results = searcher.search(query, limit=topN, terms=True)

			if topN <= len(results):
				loop_range = topN
			else:
				loop_range = len(results)

			for i in range(loop_range):
				# this needs to be adapted in order to work with the Whoosh Chatbot; uncomment next line in order to work with the normal Chatbot
				options_answers.append(results[i]['response'])
				options.append(results[i]['question'])

			return options, options_answers

			# return the element with the highest similarity score from the indexer
			# return results[0]['response']
		except IndexError:
			return None

# if __name__ == '__main__':
# 	question = "ola, tudo bem?"
# 	question = "sou o Jose"
# 	responses = query_indexer(question)
# 	print(responses)