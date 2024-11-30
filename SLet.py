# SLet interpreter attempt
# by islptng

# https://esolangs.org/wiki/SLet

from math import floor
from random import randint

class Pair:
	former = None
	latter = None
	def __init__(self, former, latter):
		self.former = former
		self.latter = latter

class Set:
	content = []
	def __init__(self):
		self.content = []
	def exist(self, value):
		return value in self.content
	def append(self, value):
		if type(value) == Pair:
			if value.latter == None: return
		if not self.exist(value):
			self.content.append(value)
		def to_num(x):
			if type(x) == int:
				return x
			elif type(x) == float:
				return x
			elif type(x) == Pair:
				return x.former
			elif type(x) == Set:
				return len(x.content)
			elif type(x) == str or type(x) == list:
				return len(x)
		def recursivenum(x):
			while type(x) != int and type(x) != float:
				x = to_num(x)
			return x
		self.content.sort(key=lambda x: recursivenum(x))
def union(set1, set2):
	result = Set()
	try:
		for x in set1.content:
			result.append(x)
	except: result.append(set1)
	try:
		for x in set2.content:
			result.append(x)
	except: result.append(set2)
	return result
def intersect(set1, set2):
	result = Set()
	for x in set1.content:
		if set2.exist(x):
			result.append(x)
	return result
def isfalse(x):
	if type(x) == bool:
		return not x
	elif type(x) == int:
		return x == 0
	elif type(x) == float:
		return x == 0.0
	elif type(x) == Pair:
		return isfalse(x.former) and isfalse(x.latter)
	elif type(x) == Set:
		return len(x.content) == 0
def filter1(set1, condition):
	result = Set()
	for x in set1.content:
		if not isfalse(condition(x)):
			result.append(x)
	return result
def pack(value):
	result = Set()
	result.append(value)
	return result
def unpack(set1):
	return set1.content[0]
def isnumber(x):
	return type(x) == int or type(x) == float
def packifnum(x):
	if isnumber(x):
		return pack(x)
	else:
		return x
def plus(level, num1, num2):
	if isnumber(num1) and isnumber(num2) and isnumber(level):
		if level == 0:
			return num1 + num2
		elif level == 1:
			return num1 * num2
		elif level == 2:
			return num1 ** num2
		result = num1
		for i in range(num2-1):
			result = plus(level-1, result, result)
		return result
	result = Set()
	for leveli in packifnum(level).content:
		for num1i in packifnum(num1).content:
			for num2i in packifnum(num2).content:
				result.append(plus(leveli, num1i, num2i))
	return result
def negate(num):
	if isnumber(num):
		return -num
	result = Set()
	for numi in packifnum(num).content:
		result.append(-numi)
	return result
def divide(num):
	if isnumber(num):
		return 1/num
	result = Set()
	for numi in packifnum(num).content:
		result.append(1/numi)
	return result
def issubset(set1, set2):
	for x in packifnum(set1).content:
		if not set2.exist(x):
			return False
	return True
	
def analyze(srcstr):
	class Tree:
		content = [None]
		depth = 0
		def dig(self):
			res = self.content
			for i in range(self.depth): res = res[-1]
			res.pop()
			res.append([None])
			self.depth += 1
		def push(self,val):
			res = self.content
			for i in range(self.depth): res = res[-1]
			res.pop()
			res.append(val)
			res.append(None)
		def pop(self):
			res = self.content
			for i in range(self.depth-1): res = res[-1]
			res.append(None)
			res = res[-2]
			res.pop()
			self.depth -= 1
		def finish(self):
			res = self.content
			for i in range(self.depth): res = res[-1]
			res.pop()
			return self.content
	# the 1st step we get rid of quotes and comments
	tcsrc = ""
	incomment = False
	inescape = False
	intext = False
	currentxt = ""
	for i in srcstr:
		if intext and not incomment:
			if inescape:
				inescape = False
				if i == 'n': currentxt += chr(10)
				elif i == 't': currentxt += '\t'
				else: currentxt += i
			else:
				if i == '\\':
					inescape = True
				elif i == '!':
					intext = False
					tcsrc += '['
					for j in range(len(currentxt)-1):
						tcsrc += str(ord(currentxt[j])) + ','
					tcsrc += str(ord(currentxt[len(currentxt)-1]))+'!'
				else: currentxt += i
			continue
		if i == '(':
			incomment = True
			continue
		if i == ')':
			incomment = False
			continue
		if i == '"' and not incomment:
			intext = True
			currentxt = ""
			continue
		if incomment: continue
		tcsrc += i
	srcstr = tcsrc.replace("\t","").replace("\n","").replace(" ","")
	srcstr = srcstr.replace("{","").replace("}","") # Don't forget we have no bracklets!
	# the 2nd step we tokenize it
	wdict = {'#':2,'@':1,'*':3,'~':2,';':0,':':1,"'":0,'`':1,
			 '|':-1,'&':-1,'^':1,'_':1,'=':1,'?':3,'+':3,'-':1,'/':1,'%':2,'<':1,'>':1,'$':2,
			 '[':-1,']':3,'\\':1,'!':0}
	currentxt = ""
	predlist = []
	for i in srcstr:
		if i in wdict:
			if currentxt != "":
				predlist.append(currentxt)
				currentxt = ""
			predlist.append(i)
		elif i == ',':
			if currentxt != "":
				predlist.append(currentxt)
				currentxt = ""
		else:
			currentxt += i
	# the 3rd step we analyze it
	res = Tree()
	tablist = [-1]
	for i in predlist:
		if i == '!':
			tablist.pop()
			res.pop()
		while tablist[-1] == 0:
			tablist.pop()
			res.pop()
		if i != '!':
			tablist[-1] -= 1
			if i in wdict:
				res.dig()
				tablist.append(wdict[i])
			res.push(i)
	return res.finish()[0]


def printable(val):
	if type(val) == Set:
		res = "{"
		for i in val.content:
			res += printable(i) + ", "
		if res == "{":
			return "Ø"
		return res[:-2]+"}"
	if type(val) == Pair:
		return "(%s %s)" % (printable(val.former), printable(val.latter))
	return str(val)

class SLetProcedure:
	variables = {}
	def __init__(self,getchar,getnum,putchar,putnum):
		self.getchar = getchar
		self.getnum = getnum
		self.putchar = putchar
		self.putnum = putnum
	def execute(self, instruction):
		if type(instruction) == str:
			try:
				return int(instruction)
			except:
				try:
					return float(instruction)
				except:
					if instruction in self.variables:
						return self.variables[instruction]
					else:
						raise NameError("Undefined variable: "+instruction)
		elif type(instruction) == list:
			if type(instruction[0]) == list:
				for i in instruction:
					self.execute(i)
				return None
			if instruction[0] == '#':
				self.variables[instruction[1]] = self.execute(instruction[2])
			elif instruction[0] == '@':
				return self.execute(self.execute(instruction[1]))
			elif instruction[0] == '*':
				set1 = self.execute(instruction[1])
				inst = instruction[3][1:]
				var = instruction[2]
				for x in set1.content:
					self.variables[var] = x
					self.execute(inst)
			elif instruction[0] == '~':
				while not isfalse(self.execute(instruction[1])):
					self.execute(self.execute(instruction[2]))
			elif instruction[0] == ';':
				self.getchar()
			elif instruction[0] == ':':
				self.putchar(self.execute(instruction[1]))
			elif instruction[0] == "'":
				return self.getnum()
			elif instruction[0] == '`':
				return self.putnum(self.execute(instruction[1]))
			elif instruction[0] == '|':
				result = Set()
				for i in instruction[1:]:
					result = union(result, self.execute(i))
				return result
			elif instruction[0] == '&':
				result = self.execute(instruction[1])
				for i in instruction[2:]:
					result = intersect(result, self.execute(i))
				return result
			elif instruction[0] == '^':
				return pack(self.execute(instruction[1]))
			elif instruction[0] == '_':
				param = self.execute(instruction[1])
				try:
					return unpack(param)
				except:
					if type(param) == int or type(param) == float:
						return floor(param)
					elif type(param) == Pair:
						return randint(param.former, param.latter)
					else:
						raise TypeError("Cannot unpack non-set value: "+printable(param))
			elif instruction[0] == '=':
				return len(self.execute(instruction[1]).content)
			elif instruction[0] == '?':
				set1 = self.execute(instruction[1])
				var = instruction[2]
				# condition is a bit tricky, we need a lambda function to evaluate it
				def condition(param):
					self.variables[var] = param
					return self.execute(instruction[3])
				return filter1(set1, condition)
			elif instruction[0] == '+':
				return plus(self.execute(instruction[1]), self.execute(instruction[2]), self.execute(instruction[3]))
			elif instruction[0] == '-':
				return negate(self.execute(instruction[1]))
			elif instruction[0] == '/':
				return divide(self.execute(instruction[1]))
			elif instruction[0] == '%':
				return Pair(self.execute(instruction[1]), self.execute(instruction[2]))
			elif instruction[0] == '<':
				return self.execute(instruction[1]).former
			elif instruction[0] == '>':
				return self.execute(instruction[1]).latter
			elif instruction[0] == '$':
				return issubset(self.execute(instruction[1]), self.execute(instruction[2]))
			elif instruction[0] == '[':
				result = Set()
				for i in range(len(instruction)-1):
					result.append(Pair(i, self.execute(instruction[i+1])))
				return result
			elif instruction[0] == ']':
				from1 = self.execute(instruction[1])
				to1 = self.execute(instruction[2])
				step1 = self.execute(instruction[3])
				if step1 > 0: judge = lambda a,b: a < b
				else: judge = lambda a,b: a > b
				result = Set()
				while judge(from1,to1):
					result.append(from1)
					from1 += step1
				return result
			elif instruction[0] == '\\':
				if instruction[1][0] == '[':
					return instruction[1][1:]
				return instruction[1]