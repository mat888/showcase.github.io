import math
import draw as d

print('---------------------start-----------------------')

def minVert(li): #given list of point pairs, finds pair with smallest first value
	bottom = -float('inf')
	floor = []
	for i in li:
		if (i[1] == bottom):
			floor.append(i)
		elif (i[1] > bottom):
			floor = [i]
			bottom = i[1]
	result = max(floor, key=lambda x: x[0])
	return result


def get_radian(a, b): #find radian value between two points from 0 to 2*pi
	if   (b[0] == a[0] and b[1] > a[1]):
		return math.pi / 2
	elif (b[0] == a[0] and b[1] < a[1]):
		return (3 * math.pi) / 2
	elif (b == a):
		return print("GET RADIAN BETWEEN SAME TWO POINTS", a, b)

	atan = math.atan((b[1] - a[1]) / (b[0] - a[0]))
	if   (a[0] > b[0]):
		return math.pi + atan
	else:
		if (atan < 0):
			return 2* math.pi + atan
		else:
			return atan


def get_distance(a, b):
	if (a[0] == b[0]):
		return abs(a[1] - b[1])
	if (a[1] == b[1]):
		return abs(a[0] - b[0])
	c = (a[1] - b[1]) **2
	d = (a[0] - b[0]) **2
	return math.sqrt( c + d )

data = d.data
data = d.flipVert(data)
data = d.padding(data, 4)
data = d.scalar(data, 10)
d.setup(data, 1)


class wrap:
	def __init__(self, points, exclusions=[]):
		points = points; 
		points = [point for point in points if (point not in exclusions)]
		self.available_points = points
		# print(exclusions)
		# print('self.points = ', points)
		self.border = [minVert(points)] #starts with most extreme x coord
		# self.exclude = exclusions.append(self.border[-1])
		self.exclude = exclusions
		#///////////////
		self.radian = 0
		#///////////////

	def remove_points(self, x):
		self.exclude.append(x)
		self.available_points.remove(x)

	def next_point(self):
		start_radian = self.radian #radian of last two connected points
		candidate_radian = math.pi * 2 #shrink from max possible radian value
		radian = None				   #defined by points tested in loop below
		start_point = self.border[-1]  #work outwards from last connected point
		candidates = {}				   #sorted in dict in case multiple radians are equal

		# "Find the smallest radian that's larger than the start radian" **
		for point in self.available_points:

			if (point in self.exclude or point == start_point):#or point == start_point):
				continue
			else:
				radian = get_radian(point, start_point)

			try:
				radian >= start_radian
			except:
				print('error')
				print('radian: ', radian, ' :: Abs rad: ', start_radian)
				print('point: ', point, ' :: start_point: ', start_point)

			#**radian must be less/equal than cand but greater/equal than start
			if (radian == candidate_radian):
				dist = get_distance(start_point, point)
				candidates[dist] = point #finding a radian equal to current -
				#- candidate adds to a dict that becomes a straight line of points.
				# print(radian)

			if (radian >= start_radian and radian < candidate_radian): 
				dist = get_distance(point, start_point)
				candidates = {} #finding a radian closer to abs radian -
				#- than current candidate resets dict to single new candidate.
				candidates[dist] = point
				candidate_radian = radian #next cand radian must be smaller than this

		candidates = {key:candidates[key] for key in sorted(candidates)}
		#in case the dict does contain more than one point:
		#we sort it by their distance from the start point before connecting them.

		

		for distance in candidates: #add points in dict to border and exclude lists.
			self.border.append(candidates[distance])
			self.exclude.append(candidates[distance])

		self.radian = candidate_radian
		return 0

def wrap_iter(exclude=[]):
	borders = []
	point_data = data

	while (len(point_data) > len(exclude)):
		# print('len(point_data) == ', len(point_data))
		# print('len(exlude) == ', len(exclude))
		border = wrap(point_data, exclude)
		for i in range(200):
			border.next_point()
		print(len(border.border))
		borders.append(border.border)
		exclude = border.exclude
	return borders

test = wrap_iter()
# test = [test[0]]
for i in test:
	print(i)
	for index, j in enumerate(i[:-1]):
		# d.drawPoint(j[0], j[1], 8, 'green')
		d.line(j[0], j[1], i[index + 1][0], i[index + 1][1], 'red')
	# d.drawPoint(i[-1][0], i[-1][1], 8, 'pink')
	d.line(i[-1][0], i[-1][1], i[0][0], i[0][1], 'red')

d.render(data)
quit()

test = wrap(data, [])

for i in range(92):
	test.next_point()

for i in test.border:
	d.drawPoint(i[0], i[1], 8, 'green')

print(test.border)
d.render(data)






