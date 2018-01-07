import requests
from bs4 import BeautifulSoup as bs
from Queue import Queue
import threading
entry = 'https://www.yahoo.co.jp/'
# entry = 'http://www.celm.co.jp/interview/amazon/'
# entry = 'https://www.wikipedia.org/'


class Scrawler:
	def __init__(self):
		self.visited = {}
		self.que = Queue()
	
	def dfs(self, link):
		if link == None or link in self.visited:
			return
		print "{} || ".format(len(self.visited)) + link
		try:
			self.visited[link] = True
			resp = requests.get(link)
			soup = bs(rest.text, 'html.parser')
			tags = soup.find_all('a')
		except:
			return
		for tag in tags:
			next = tag.get('href', None)
			self.dfs(next)
	
	def bfs(self, link):
		self.que.put(link)
		while not self.que.empty():
			try:
				cur = self.que.get()
				if cur == None or cur in self.visited:
					continue
				self.visited[cur] = True
				resp = requests.get(cur)
				soup = bs(resp.text, 'html.parser')
				print "{} || ".format(len(self.visited)) + cur
				tags = soup.find_all('a')
				for tag in tags:
					next = tag.get('href', None)
					if next not in self.visited:
						self.que.put(next)
			except:
				continue

scw = Scrawler()
scw.bfs(entry)