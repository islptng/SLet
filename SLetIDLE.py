from SLet import *

inbuffer = ""
def iputchar(x):
	print(chr(x), end="")
def iputnum(x):
	print(x, end=" ")
def igetchar():
	global inbuffer
	if len(inbuffer) == 0:
		try: a = input()
		except EOFError: a = "\0"
		inbuffer += a + '\n'
	t = inbuffer[0]
	inbuffer = inbuffer[1:]
	return t
def igetnum():
	global inbuffer
	originalnum = ""
	t = 'a'
	while t not in '0123456789.': t = igetchar()
	while t in '0123456789.':
		originalnum += t
		t = igetchar()
	inbuffer = t + inbuffer
	try:
		return int(originalnum)
	except:
		return float(originalnum)

show = """SLet 2.0.1 - IDLE 1.0 (Nov.28 2024)  by islptng
Type ".info" for the online document,
     ".def"  to see a list of variables,
  or ".exit" to quit. """
print(show)
idle = SLetProcedure(igetchar,igetnum,iputchar,iputnum)

text = ""
while text != ".exit":
	if text == ".def":
		print("Name     Value\n--------------------")
		for i in idle.variables.keys():
			print(i,"\t",printable(idle.variables[i]))
		print("--------------------")
		text = ""
		continue
	elif text == ".info":
		import webbrowser
		webbrowser.open("https://esolangs.org/wiki/SLet")
		text = ""
		continue
	try:
		text = analyze("[" + text + "!")
		error = True
		try:
			rtv = idle.execute(text)
			error = False
		except Exception as e: print(type(e),e)
		if not error:
			print("=",printable(rtv.content[0].latter))
	except:
		pass
	print("\n    --> ", end="")
	text = input()