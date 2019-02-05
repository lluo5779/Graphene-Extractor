import json
from collections import Counter

path = 'YOUR PATH'#'C:/Users/yiqing.luo/Documents/OpenIE/Graphene-3.0.0/graphene-cli/'
filename = 'YOUR FILE NAME'
jsonData = open(path + filename).read()

data = json.loads(jsonData)


import requests
import re
import json


class GrapheneExtract(object):

    def __init__(self, blob, isRE):
        try:
            self.json = blob['sentences']
            if isRE:
                self.json = {k: v for d in [i['extractionMap'] for i in self.json] for k, v in d.items()} 
            else:
                self.json = {k: v for d in [i['elementMap'] for i in self.json] for k, v in d.items()}
			print(self.json)
			self.visited = {e:False for e in self.json} 
			self.failed = False
		except json.decoder.JSONDecodeError:
			self.failed = True

	def linearize(self):
		''' Depth-first search and append on the extracts '''
		if self.failed:
			return ""
		self.strbuild = ""
		for hashId in self.json:
			self.visit(hashId)
		self.strbuild =  self.strbuild.replace(".", "")
		self.strbuild = re.sub(r"\s+", ' ', self.strbuild)
		return self.strbuild.strip()

	def visit(self, hashId):
		if self.visited[hashId]:
			return
		self.visited[hashId] = True
		self.strbuild += " ( " + self.json[hashId]['arg1'] + " <> " + self.json[hashId]['relation'] + " <> " + self.json[hashId]['arg2']
		for simple in self.json[hashId]['simpleContexts']:
			if simple['classification'] != "NOUN_BASED":
				if simple['classification'] == "TEMPORAL_BEFORE":
					if simple['text'].lower().startswith("after"): 
						simple['text'] = simple['text'][len("after"):]
				if simple['classification'] == "TEMPORAL_AFTER":
					if simple['text'].lower().startswith("before"):
							simple['text'] = simple['text'][len("before"):]
				self.strbuild += " " + simple['classification'] + " " + simple['text']
		for child in self.json[hashId]['linkedContexts']:
			if not self.visited[child['targetID']]:
				self.strbuild += " " + child['classification'] + " "
				self.visit(child['targetID'])
		self.strbuild += " ) "

	def visit_SIM(self, hashId): # NOT FINISHED
		if self.visited[hashId]:
			return
		self.visited[hashId] = True
		self.strbuild += self.json[hashId]['text']  + " <> " + hashId + '/n'
		for simple in self.json[hashId]['simpleContexts']:
			if simple['relation'] == "UNKNOWN":
                continue
            elif simple['relation'] == "CONTRAST":
                
				self.strbuild += " " + simple['classification'] + " " + simple['text']
		for child in self.json[hashId]['linkedContexts']:
			if not self.visited[child['targetID']]:
				self.strbuild += " " + child['classification'] + " "
				self.visit(child['targetID'])
		self.strbuild += " ) "

	def extractList(self):
		''' Output a list of all extracts (used for simple 3-tuples OpenIE) '''
		toReturn = []
		for i in self.json:
			if self.failed or self.json[i]['arg1'] == "" or self.json[i]['relation'] == "" or self.json[i]['arg2'] == "":
				continue
			toReturn.append(self.json[i]['arg1'] + " <> " + self.json[i]['relation'] + " <> " + self.json[i]['arg2'])
		return toReturn

g = GrapheneExtract(data, isRE = True)

