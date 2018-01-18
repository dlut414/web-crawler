import requests
from bs4 import BeautifulSoup as bs
from Queue import Queue
import threading

def timerWrapper(timeout):
	def decorator(func):
		def wrapper(*args):
			class FuncThread(threading.Thread):
				def __init__(self):
					threading.Thread.__init__(self)
					self.ret = None
				def run(self):
					self.ret = func(*args)
				def _stop(self):
					if self.isAlive():
						threading.Thread._Thread__stop(self)
			it = FuncThread()
			it.start()
			it.join(timeout)
			if it.isAlive():
				it._stop()
				raise Exception(" Time out! {}".format(args[1]))
			else:
				return it.ret
		return wrapper
	return decorator

class Scrawler:
	def __init__(self):
		self.visited = {}
		self.que = Queue()
	
	@timerWrapper(10)
	def rget(self, link):
		return requests.get(link)
	
	def dfs(self, link):
		if link == None or link in self.visited:
			return
		print "{} || ".format(len(self.visited)) + link
		try:
			self.visited[link] = True
			resp = self.rget(link)
			soup = bs(resp.text, 'html.parser')
			tags = soup.find_all('a')
		except Exception as e:
			print e
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
				resp = self.rget(cur)
				soup = bs(resp.text, 'html.parser')
				print "{} || ".format(len(self.visited)) + cur
				tags = soup.find_all('a')
				for tag in tags:
					next = tag.get('href', None)
					if next not in self.visited:
						self.que.put(next)
			except Exception as e:
				print e
				continue

if __name__ == "__main__":
	# entry = 'https://www.yahoo.co.jp/'
	# entry = 'http://www.celm.co.jp/interview/amazon/'
	# entry = 'https://www.wikipedia.org/'
	entry = input(" input the entry url: ")
	scw = Scrawler()
	scw.bfs(entry)
