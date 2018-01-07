import requests
from bs4 import BeautifulSoup as bs
from Queue import Queue
import threading
entry = 'https://www.yahoo.co.jp/'
# entry = 'http://www.celm.co.jp/interview/amazon/'
# entry = 'https://www.wikipedia.org/'

def timerWrapper(timeout):
	def decorator(func):
		def wrapper(*args=(), **kwargs={}):
			class FuncThreading(threading.Thread):
				def __init__(self):
					threading.Thread.init(self)
				def run(self):
					self.ret = func(*args, **kwargs)
				def _stop(self):
					if self.isActive():
						threading.Thread._Thread__stop(self)
			it = FuncThread()
			it.start()
			it.join(timeout)
			if it.isActive():
				it._stop()
				print " Time out! "
				raise Exception()
			else:
				return it.ret
		return wrapper

class Scrawler:
	def __init__(self):
		self.visited = {}
		self.que = Queue()
	
	@timerWrapper(1)
	def rget(link):
		return requests.get(link)
	
	def dfs(self, link):
		if link == None or link in self.visited:
			return
		print "{} || ".format(len(self.visited)) + link
		try:
			self.visited[link] = True
			resp = rget(link)
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
				resp = rget(cur)
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