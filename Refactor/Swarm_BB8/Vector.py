import numpy as np

class Vector:
	def __init__(self, x=0, y=0):
		self.x = x
		self.y = y

	def __mul__(self, a):
		self.x = self.x * a
		self.y = self.y * a
		return self

	def __add__(self, a):
		self.x = self.x + a.x
		self.y = self.y + a.y
		return self

	def __sub__(self, a):
		self.x = self.x - a.x
		self.y = self.y - a.y
		return self

	def __truediv__(self, a):
		self.x = self.x / a
		self.y = self.y / a
		return self

	def add(self, a):
		self.x = self.x + a.x
		self.y = self.y + a.y

	def parseToInt(self):
		return (int(self.x), int(self.y))

	def magnitude(self):
		return np.sqrt(self.x * self.x + self.y * self.y)

	def normalize(self):
		mag = self.magnitude()
		if not (mag == 0 ):
			self = self/mag
			
	def Normalize(self):
		mag = self.magnitude()
		if mag != 0:
			return Vector(self.x/mag, self.y/mag)
		else:
			return Vector(1, 1)

	def heading(self):
		angle = np.arctan2(self.y, self.x)
		return angle

	def limit(self, max_length):
		squared_mag = self.magnitude() * self.magnitude()
		if squared_mag > (max_length * max_length):
			self.x = self.x/np.sqrt(squared_mag)
			self.y = self.y/np.sqrt(squared_mag)
			self.x = self.x * max_length
			self.y = self.y * max_length
		
	def reset(self, x=0, y=0):
		self.x = x
		self.y = y

	def __repr__(self):
		return f'vector-> x:{self.x}, y:{self.y}'
	
def cart2pol(x, y):
	rho = np.sqrt(x**2 + y**2)
	phi = np.arctan2(y, x)
	return rho, phi

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y

def getDistance(v1, v2):
	return np.sqrt((v2.x - v1.x)*(v2.x - v1.x) + (v2.y -v1.y)*(v2.y - v1.y))

def AddVectors(v1, v2):
	return Vector(v1.x + v2.x, v1.y + v2.y)

def translate(value, min1, max1, min2, max2):
    return min2 + (max2 - min2)* ((value-min1)/(max1-min1))

def SubVectors(v1, v2):
	return Vector(v1.x - v2.x, v1.y - v2.y)

def SubVectorsX(v1, v2):
	return Vector(v1.x - v2.x, v2.y)

def SubVectorsY(v1, v2):
	return Vector(v2.x, v1.y - v2.y)

def middle_point(x1, x2):
	return (x1 + x2) / 2