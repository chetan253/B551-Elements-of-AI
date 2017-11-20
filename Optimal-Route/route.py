#Chetan 11/04/2017
import sys
import csv
from haversine import haversine 
class Search:
	mapper = {}
	coordinates = {}
	coord_dist = {}
	
	def __init__(self, city_gps, segments, start_city, end_city):
		self.city_gps = city_gps
		self.segments = segments
		self.start_city = start_city
		self.end_city = end_city
	
	#returns the route info for a city2 to visit from city1
	def city_route_data(self, elements):
		return {'length' : elements[0], 'speed_limit': elements[1], 'highway_name': elements[2]}
	
	#returns the coordinates for all specific cities
	def city_coordinates(self, elements):
		return {'lat' : elements[0], 'long' : elements[1]}
	
	#maps the haversine distance between 2 cities ~~ used as an heuristic instead of eucledian distance 
	#as in case of earth the shape is not 2-D graph but spherical 
	def getDistInCities(self, city1, city2):
		if(self.coordinates.has_key(city1) and self.coordinates.has_key(city2)):
			city1coord = (float(self.coordinates[city1]['lat']), float(self.coordinates[city1]['long']))
			city2coord = (float(self.coordinates[city2]['lat']), float(self.coordinates[city2]['long']))
			if(self.coord_dist.has_key(city1)):
				if(self.coord_dist[city1].has_key(city2) == False):
					self.coord_dist[city1][city2] = haversine(city1coord , city2coord)
			else:
				self.coord_dist[city1] = {}
				self.coord_dist[city1][city2] = haversine(city1coord, city2coord)
	
	#maps the city 1 to city 2 information from the file
	def defineSegments(self, data):
		route = data[0].split(' ')
		from_city = route[0]
		to_city = route[1]
		if(self.mapper.has_key(from_city)):
			if(self.mapper[from_city].has_key(to_city) == False):
				self.mapper[from_city][to_city] = self.city_route_data(route[2:])
		else:
			self.mapper[from_city] = {}
			self.mapper[from_city][to_city] = self.city_route_data(route[2:])
		if(self.mapper.has_key(to_city)):
			if(self.mapper[from_city].has_key(from_city) == False):
				self.mapper[to_city][from_city] = self.city_route_data(route[2:])
		else:
			self.mapper[to_city] = {}
			self.mapper[to_city][from_city] = self.city_route_data(route[2:])
		self.getDistInCities(from_city, to_city)
		self.getDistInCities(to_city, from_city)
	
	#maps the coordinates from gps file to respective cities
	def defineCoordinates(self, data):
		city = data[0].split(' ')
		self.coordinates[city[0]] = self.city_coordinates(city[1:])
	
	#data loader
	def dataLoader(self, filename):
		f = open(filename)
		reader = csv.reader(f, delimiter = '\n')
		for row in reader:
			if (filename == self.segments):
				self.defineSegments(row)
			elif (filename ==  self.city_gps):
				self.defineCoordinates(row)
			else:
				print 'No such file :', filename
	
	#successor of current city
	def successors(self, city):
		succ = []
		for i in self.mapper[city]:
			succ.append(i)
		return succ
	
	#bfs search from start to end city
	def bfs(self, start, end):
		fringe = [start]
		visited = {}
		while(len(fringe) > 0):
			for i in self.successors(fringe.pop(0)):
				print i
				if visited.has_key(i):
					continue
				else:
					visited[i] = ""
				if i == end_city:
					print 'we reached'
					return
				fringe.append(i)
		return False
	
	def dfs(self, start, end):
		fringe = [start]
		visited = {}
		print 'chetan'
		while(len(fringe) > 0):
			for i in self.successors(fringe.pop()):
				print i
				if visited.has_key(i):
					continue
				else:
					visited[i] = ""
				if i == end_city:
					print 'we reached'
					return
				fringe.append(i)
		return False	
	
	#make search based on routing algo and cost function
	def start_search(self, routing_algo, cf_name):
		if(routing_algo  == 'bfs'):
			self.bfs(self.start_city, self.end_city)
		elif(routing_algo  == 'dfs'):
			self.dfs(self.start_city, self.end_city)
		
	

start_city, end_city, routing_algo, cost_function = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
city_gps = 'city-gps.txt'
segments = 'road-segments.txt'
search = Search(city_gps, segments, start_city, end_city)
search.dataLoader(city_gps)
search.dataLoader(segments)
#print search.mapper[start_city]
search.start_search(routing_algo, cost_function)
