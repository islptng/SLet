# SLet.py
# which interprets SLet.
# Pass the filename as an argument to the interpreter to run the file.
# Otherwise, run as IDLE.

from sys import argv
from math import gcd
from random import randint

# Environment
# Version 3.1.2 by islptng
# Last modified: 12th Feb 2025, 10:22
class Number:
    def simplify(self):
        if self.denominator == 0:
            if self.numerator != 0: self.numerator = 1
        else:
            gcdn = gcd(self.numerator, self.denominator)
            self.numerator //= gcdn
            self.denominator //= gcdn
    def __init__(self, val, denominator = 1):
        if isinstance(val, str):
            if val == "nan": val = "0/0"
            if val == "infinity": val = "1/0"
            val = val.split("/")
            self.numerator = int(val[0])
            try: self.denominator = int(val[1])
            except: self.denominator = 1
        else:
            self.numerator = val
            self.denominator = denominator
        self.simplify()
    def __str__(self):
        if self.denominator == 0:
            if self.numerator == 0: return "nan"
            else: return "infinity"
        if self.denominator == 1:
            return str(self.numerator)
        return str(self.numerator) + "/" + str(self.denominator)
    def __add__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        denominator = self.denominator * other.denominator
        numerator = self.numerator * other.denominator + other.numerator * self.denominator
        res = Number(numerator, denominator)
        res.simplify()
        return res
    def __sub__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        denominator = self.denominator * other.denominator
        numerator = self.numerator * other.denominator - other.numerator * self.denominator
        res = Number(numerator, denominator)
        res.simplify()
        return res
    def __mul__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        numerator = self.numerator * other.numerator
        denominator = self.denominator * other.denominator
        res = Number(numerator, denominator)
        res.simplify()
        return res
    def __truediv__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        numerator = self.numerator * other.denominator
        denominator = self.denominator * other.numerator
        res = Number(numerator, denominator)
        res.simplify()
        return res
    def __mod__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        intn = int(self / other)
        modn = self - other * intn
        return modn
    def __floordiv__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return int(self / other)
    def __eq__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.numerator == other.numerator and self.denominator == other.denominator
    def __lt__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.numerator * other.denominator < other.numerator * self.denominator
    def __gt__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.numerator * other.denominator > other.numerator * self.denominator
    def __le__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.numerator * other.denominator <= other.numerator * self.denominator
    def __ge__(self, other):
        if not isinstance(other, Number):
            other = Number(other)
        return self.numerator * other.denominator >= other.numerator * self.denominator
    def __int__(self): return self.numerator // self.denominator
    def __bool__(self): return self.numerator != 0
    def __float__(self): return float(self.numerator) / float(self.denominator)
Boolean = bool

class Pair:
    def __init__(self, former, latter):
        self.former = former
        self.latter = latter
    def __str__(self):
        return "(%s,%s)" % (str(self.former), str(self.latter))

class Set:
    def sort(self):
        self.objects.sort(key=cmp_array)
    def __init__(self, objects):
        self.objects = list(objects)
        self.sort()
    def __str__(self):
        return "{%s}" % (",".join(str(obj) for obj in self.objects))
    def append(self, obj):
        if obj not in self.objects:
            self.objects.append(obj)
            self.sort()
    def __contains__(self, obj):
        return obj in self.objects
    def __len__(self):
        return len(self.objects)
    def issubset(self, other):
        flag = True
        for obj in self.objects:
            if obj not in other:
                flag = False
                break
        return flag
    def intersect(self, other):
        res = Set([])
        for obj in self.objects:
            if obj in other:
                res.append(obj)
        return res

def cmp_array(obj):
    ndict = {Boolean: 0, Number: 1, Pair: 2, Set: 3, Lambda: 4}
    typen = ndict[type(obj)]
    res = [typen]
    if typen == 0: res.append(obj)
    if typen == 1: res.append(obj)
    if typen == 2:
        res.append(cmp_array(obj.former))
        res.append(cmp_array(obj.latter))
    if typen == 3: res.append(len(obj.objects))
    if typen == 4: res.append(0) # Lambdas are not comparable
    return res

variables = {}

inbuffer = ""
def get_char():
    global inbuffer
    if not inbuffer: inbuffer = input() + "\n"
    returnv = inbuffer[0]
    inbuffer = inbuffer[1:]
    return returnv
put_char = lambda x: print(ord(x), end="")
print_obj = lambda x: print("" if x is None else str(x), end="")
def printdec(n, digits):
    # print integer part
    print(int(n),end="")
    # print decimal part
    digits = int(digits)
    if digits > 0: print(end=".")
    for i in range(digits):
        n *= 10
        print(int(n % 10),end="")

def analyze(code):
    def tokenize(code):
        # Remove comments
        commentdepth = 0
        instring = False
        newcode = ""
        tokens = []
        for i in range(len(code)):
            if code[i] == '"':
                instring = not instring
                newcode += code[i]
                continue
            if instring:
                newcode += code[i]
                continue
            if code[i] in " \n\t":
                if newcode:
                    tokens.append(newcode)
                    newcode = ""
                    continue
            if code[i] == "(":
                commentdepth += 1
            elif code[i] == ")":
                commentdepth -= 1
            if commentdepth == 0:
                newcode += code[i]
        if newcode: tokens.append(newcode)
        for i in range(len(tokens)):
            if tokens[i] == "true": tokens[i] = True
            elif tokens[i] == "false": tokens[i] = False
            elif tokens[i] == "empty": tokens[i] = Set([])
            elif tokens[i] == "nan": tokens[i] = Number("nan")
            elif tokens[i] == "infinity": tokens[i] = Number("infinity")
            elif tokens[i][0] == '"':
                parsed = eval('""'+tokens[i].replace("\\q","\\\"")+'""')
                res = Set([])
                for j in range(len(parsed)):
                    curpair = Pair(Number(j), Number(ord(parsed[j])))
                    res.append(curpair)
                tokens[i] = res
            else:
                flag = True
                for j in range(len(tokens[i])):
                    if tokens[i][j] not in "0123456789-/":
                        flag = False
                        break
                if flag: tokens[i] = Number(tokens[i])
        return tokens
    tokens = tokenize(code)
    # add left and right bracklets to the tokens
    # and remove the "all" keyword
    argdict = {'for':3,'while':2,'do':-1,'call':1,
'get-char':0,'put-char':1,'input':0,'print':1,
'match':2,'combine':-1,'opposite':1,'swap':1,
'former':1,'latter':1,'pack':1,'exist':2,
'reveal':1,'add':2,'multiply':2,'divide':2,
'range':3,'filtrate':3,'size':1,'let':2,
'or':2,'and':2,'intersect':2,'first':1,
'decprint':2,'floordiv':2,'modulo':2}
    class Cursor: pass # we need a "Cursor" keyword and not a class, just does nothing
    class Tree:
        content = [Cursor]
        depth = 0
        def dig(self):
            res = self.content
            for i in range(self.depth): res = res[-1]
            res.pop()
            res.append([Cursor])
            self.depth += 1
        def push(self,val):
            res = self.content
            for i in range(self.depth): res = res[-1]
            res.pop()
            res.append(val)
            res.append(Cursor)
        def pop(self):
            res = self.content
            for i in range(self.depth-1): res = res[-1]
            res.append(Cursor)
            res = res[-2]
            res.pop()
            self.depth -= 1
        def finish(self):
            res = self.content
            for i in range(self.depth): res = res[-1]
            res.pop()
            return self.content
    tablist = [-1]
    res = Tree()
    for token in tokens:
        if isinstance(token, str) and token in argdict:
            tablist[-1] -= 1
            tablist.append(argdict[token] + 1 if argdict[token] >= 0 else -1)
            res.dig()
        if isinstance(token, str) and token == "all":
            res.pop()
            if tablist[-1] < 0: tablist.pop()
            else: raise SyntaxError("Unexpected keyword 'all'")
        else:
            if not isinstance(token, str) or token not in argdict: tablist[-1] -= 1
            res.push(token)
        while tablist[-1] == 1:
            tablist.pop()
            res.pop()
    return res.finish()

class Lambda:
    code = ""
    def __init__(self, code):
        if isinstance(code, str): self.code = analyze(code)
        else: self.code = code
    def __str__(self):
        return "<code>"
    def call(self):
        for i in self.code:
            exec1(i)

def exec1(command):
    try:
        if not isinstance(command, type([])):
            if isinstance(command, str):
                if command[0] in variables: return variables[command[0]]
            return command
        args = command[1:]
        # pass is TODO
        if   command[0] ==      "let": variables[command[1]] = exec1(args[1])
        elif command[0] ==      "for":
            for i in exec1(args[0]).objects:
                variables[args[1]] = i
                exec1(args[2]).call()
        elif command[0] ==    "while":
            while exec1(args[0]): exec1(args[1]).call()
        elif command[0] ==       "do": return Lambda(args)
        elif command[0] ==     "call": exec1(args[0]).call()
        elif command[0] == "get-char": return Number(ord(get_char()))
        elif command[0] == "put-char": print(end=chr(int(exec1(args[0]))))
        elif command[0] ==    "input": return Number(input())
        elif command[0] ==    "print": print_obj(exec1(args[0]))
        elif command[0] == "decprint": printdec(exec1(args[0]), exec1(args[1]))
        elif command[0] ==    "match": return Pair(exec1(args[0]), exec1(args[1]))
        elif command[0] ==  "combine":
            res = Set([])
            for i in args: res.append(exec1(i))
            return res
        elif command[0] == "opposite": return not a if isinstance((a := exec1(args[0])), Boolean) else (a * Number(-1))
        elif command[0] ==     "swap": return Pair(a.latter, a.former) if isinstance((a := exec1(args[0])), Pair) else (Number(1) / a)
        elif command[0] ==   "former": return a.former if isinstance((a := exec1(args[0])), Pair) else a.numerator
        elif command[0] ==   "latter": return a.latter if isinstance((a := exec1(args[0])), Pair) else a.denominator
        elif command[0] ==     "pack": return Set([exec1(args[0])])
        elif command[0] ==    "exist": return a.issubset(b := exec1(args[1])) if isinstance((a := exec1(args[0])), Set) else a in b.objects
        elif command[0] ==   "reveal": return exec1(args[0]).objects[randint(0,len(exec1(args[0]).objects)-1)] if isinstance((a := exec1(args[0])), Set) else randint(int(a.former),int(a.latter))
        elif command[0] ==    "first": return exec1(args[0]).objects[0]
        elif command[0] ==      "add": return exec1(args[0]) + exec1(args[1])
        elif command[0] ==       "or": return exec1(args[0]) or exec1(args[1])
        elif command[0] == "multiply": return exec1(args[0]) * exec1(args[1])
        elif command[0] ==      "and": return exec1(args[0]) and exec1(args[1])
        elif command[0] =="intersect": return exec1(args[0]).intersect(exec1(args[1]))
        elif command[0] ==   "divide": return exec1(args[0]) / exec1(args[1])
        elif command[0] == "floordiv": return exec1(args[0]) // exec1(args[1])
        elif command[0] ==   "modulo": return exec1(args[0]) % exec1(args[1])
        elif command[0] ==    "range":
            fromn = exec1(args[0])
            ton = exec1(args[1])
            step = exec1(args[2])
            i = fromn
            res = Set([])
            while i <= ton:
                res.append(i)
                i += step
            return res
        elif command[0] == "filtrate":
            res = Set([])
            for i in exec1(args[0]).objects:
                variables[args[1]] = i
                if exec1(args[2]): res.append(i)
            return res
        elif command[0] ==     "size": return len(exec1(args[0]).objects)
        else: raise NameError("'%s' is not defined" % (str(command[0])))
    except RecursionError:
        print("\n\n\nSorry, but it's Python's fault.\n\
You have exceeded the maximum recursion depth.")

# Interpret a file.
if len(argv) > 1:
    with open(argv[1], "r") as f:
        code = f.read()
    lamb = Lambda(code)
    lamb.call()
    exit()

# IDLE
def help():
    import webbrowser
    webbrowser.open("https://esolangs.org/wiki/SLet")

def vars():
    print("================")
    for var in variables:
        print("%s\t| %s" % (var, str(variables[var])))
    print("================")

def execute(code):
    token = analyze(code)
    if len(token) == 1:
        code = "print " + code
    lamb = Lambda(code)
    lamb.call()

print("""SLet 3.1.2 by islptng
Type "help" for help, "vars" to see variables, and "exit" to quit.""")
while True:
    code = input("\n=> ")
    if code == "help": help()
    elif code == "vars": vars()
    elif code == "exit": exit()
    else:
        try:
            execute(code)
        except Exception as e:
            print("ERROR:", e)

