import random
#from typing import type_check_only

TT_INT="TT_INT"
TT_FLOAT="FLOAT"
TT_PLUS="PLUS"
TT_MINUS="MINUS"
TT_MUL="MUL"
TT_DIV="DIV"
TT_LPAREN="LPAREN"
TT_MOD="MOD"
TT_RPAREN="RPAREN"
TT_EOF="EOF"
TT_KEYWORD="KEYWORD"
TT_IDENTIFIER="IDENTIFIER"
TT_EQ="EQ"
KEYWORDS=["data","and","or","not", "if","then", "instruct","end",'close',"finish","print",'mov','mova']
TT_POW="POW"
TT_EE = "EE"
TT_NE="NE"
TT_LT="LT"
TT_GT="GT"
TT_LTE="LTE"
TT_GTE="GTE"
TT_COMMA="COMMA"
TT_STRING="STRING"
TT_LSQUARE="LSQUARE"
TT_RSQUARE="RSQUARE"
TT_NEWLINE="NEWLINE"
TT_DOT="DOT"
#Constants
DIGITS="0123456789"
LETTERS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_"
LETTERS_DIGITS=LETTERS+DIGITS
class Error:
	def __init__(self,type_,note):
		self.type_=type_
		self.note=note
	def toString(self):
		return "[Error] : "+self.type_ + '\n\t' + self.note

class Token:
	def __init__(self,type_,value=None,pos_start=None,pos_end=None):
		self.type=type_
		self.value=value
		if pos_start:
			self.pos_start=pos_start.copy()
			self.pos_end=pos_start.copy().advance()
		if pos_end:
			self.pos_end=pos_end
	def matches(self,type_,value):
		return self.type==type_ and self.value==value
	def __repr__(self):
		if self.value != None: return f"{self.type}:{self.value}"
		return f"{self.type}"


class Position:
	def __init__(self,index,ln,cn,fn,ftxt):
		self.index=index
		self.ln=ln
		self.cn=cn
		self.fn=fn
		self.ftxt=ftxt
	def advance(self,current_char=None):
		self.index+=1
		self.cn+=1
		if current_char=="\n":
			self.ln+=1
			self.cn=0
		return self
	def copy(self):
		return Position(self.index,self.ln,self.cn,self.fn,self.ftxt)

class Lexer:
	token_lookup = {
		";": TT_NEWLINE,
		"+": TT_PLUS,
		"-": TT_MINUS,
		".": TT_DOT,
		"*": TT_MUL,
		"/": TT_DIV,
		"%": TT_MOD,
		"^": TT_POW,
		"(": TT_LPAREN,
		")": TT_RPAREN,
		"[": TT_LSQUARE,
		"]": TT_RSQUARE,
		",": TT_COMMA
	}
	def __init__(self,fn,text):
		self.text=text
		self.fn =fn
		self.pos=Position(-1,0,0,fn,text)
		self.current_char=None
		self.advance()
	def advance(self):
		self.pos.advance(self.current_char)
		self.current_char=self.text[self.pos.index] if self.pos.index<len(self.text) else None
	def make_tokens(self):
		tokens=[]
		while self.current_char!=None:
			if self.current_char in "\t \n":
				self.advance()
			elif self.current_char in DIGITS:
				tokens.append(self.make_number())
			elif self.current_char in LETTERS:
				tokens.append(self.make_identifier())
			elif self.current_char=='"':
				tokens.append(self.make_string())
				self.advance()
			elif self.current_char in self.token_lookup:
				tokens.append(Token(self.token_lookup[self.current_char], pos_start=self.pos))
				self.advance()
			elif self.current_char=="#":
				self.skip_comment()
			elif self.current_char=="!":
				tok,error=self.make_not_equals()
				if error:
					return [],error
				tokens.append(tok)
				#self.advance()
			elif self.current_char=="=":
				tokens.append(self.make_equals())
			elif self.current_char=="<":
				tokens.append(self.make_less_than())
			elif self.current_char==">":
				tokens.append(self.make_greater_than())
			else:
				pos_start=self.pos.copy()

				char = self.current_char
				self.advance()
				return [],CharacterError(pos_start,self.pos,'"'+char+'"')
		tokens.append(Token(TT_EOF,pos_start=self.pos))
		#print(tokens)
		return tokens,None
	def make_number(self):
		num=""
		dot_count=0
		pos_start=self.pos.copy()
		while self.current_char!=None and self.current_char in DIGITS+".":
			if self.current_char==".":
				if dot_count==1: break
				dot_count+=1
				num+="."
			else:
				num+=self.current_char
			self.advance()
		#print(num)
		if dot_count==0:
			return Token(TT_INT,int(num),pos_start,self.pos)
		else:
			return Token(TT_FLOAT,float(num),pos_start,self.pos)
	def make_identifier(self):
		id_str=""
		pos_start=self.pos.copy()
		while self.current_char != None and self.current_char in LETTERS_DIGITS:
			id_str+=self.current_char
			self.advance()
		tok_type=TT_KEYWORD if id_str in KEYWORDS else TT_IDENTIFIER
		return Token(tok_type,id_str,pos_start,self.pos)
	def make_not_equals(self):
		pos_start=self.pos.copy()
		self.advance()
		if self.current_char=="=":
			self.advance()
			return Token(TT_NE,pos_start,self.pos), None
		self.advance()
		return None, ExpectedCharError(pos_start,pos_end,"Expected '='")
	def make_equals(self):
		tok_type=TT_EQ
		pos_start=self.pos.copy()
		self.advance()
		if self.current_char=="=":
			self.advance()
			tok_type=TT_EE
		return Token(tok_type,pos_start,self.pos)
	def make_less_than(self):
		tok_type=TT_LT
		pos_start=self.pos.copy()
		self.advance()
		if self.current_char=="=":
			self.advance()
			tok_type=TT_LTE
		return Token(tok_type,pos_start,self.pos)
	def make_greater_than(self):
		tok_type=TT_GT
		pos_start=self.pos.copy()
		self.advance()
		if self.current_char=="=":
			self.advance()
			tok_type=TT_GTE
		return Token(tok_type,pos_start,self.pos)
	def make_string(self):
		string=""
		pos_start=self.pos.copy()
		escape_char=False
		self.advance()
		escape_chars={"n":"\n","t":"\t"}
		while self.current_char!=None and (self.current_char != '"' or escape_char):
			if escape_char:
				escape_char=False
				string+=escape_chars.get(self.current_char,self.current_char)
			else:
				if self.current_char=="\\":
					escape_char=True
				else:
					string+=self.current_char
			self.advance()
			#if self.current_char==None:
				#return None, ExpectedCharError(pos_start,self.pos,"Expected '\"'")
		#self.advance()

		return Token(TT_STRING,string,pos_start,self.pos)
	def skip_comment(self):
		self.advance()
		while self.current_char!="\n":
			self.advance()
		self.advance()

class Table:
	def __init__(self):
		self.pointer="i"
		self.index=0
		self.data={}
		self.instructions={}
	def get(self,immediate=False):
		if self.pointer=="i":
			value=self.instructions.get(self.index,0)
		if self.pointer=="d":
			value=self.data.get(self.index,0)
		return value
	def set(self,value):
		if self.pointer=="i":
			self.instructions[self.index]=value
		elif self.pointer=="d":
			self.data[self.index]=value
class SymbolTable:
	def __init__(self,parent=None):
		self.symbols={}
		
	def get(self,name):
		value=self.symbols.get(name,None)
		return value
	def set(self,name,value):
		self.symbols[name]=value
	def remove(self,name):
		del self.symbols[name]
def taperead(params):
	block= TAPE.get()
	for i in block:
		if i.type==TT_NEWLINE:
			pass
		elif i.type==TT_RSQUARE:
			pass
		else:
			return i
def tapewrite(params):
	#print("Write Called")
	TAPE.set([params[0]])
TAPE=Table()
BUILTIN=SymbolTable()
BUILTIN.set("read",taperead)
BUILTIN.set("write",tapewrite)
class Noderize:
	def __init__(self,tokens):
		self.tokens=tokens
		self.lines=[]
	def createLines(self):
		temp = []
		for i in self.tokens:
			if i.type==TT_NEWLINE:
				if temp:
					self.lines.append(temp)
					temp=[]
			else:
				temp.append(i)
class BinOp:
	def __init__(self,a,b,op):
		self.a=a
		self.b=b
		self.op=op
	def __repr__(self):
		return f"<BinOp {self.a} {self.op} {self.b}>"
class Call:
	def __init__(self,func,params):
		self.func=func
		self.params=params
class Executor:
	def __init__(self,tokens):
		self.tokens=tokens

	def visit(self):
		#print(TAPE.index)
		nodes=Noderize(TAPE.get())
		nodes.createLines()
		#print(nodes.lines)

		#
		# High Level Calls
		#
		for i in nodes.lines:

			lineIndex=0
			if i[0].type==TT_KEYWORD and i[0].value=="finish":
				return True
			elif i[0].type==TT_KEYWORD and i[0].value=="mov":
				self.move(i,lineIndex)
			elif i[0].type==TT_KEYWORD and i[0].value=="mova":
				self.moveAbsolute(i,lineIndex)
			elif i[0].type==TT_KEYWORD and i[0].value=="print":
				self.print(i,lineIndex)
			else:
				self.assess(i)
		return False

	def move(self,line,lineIndex):
		lineIndex+=1
		if line[lineIndex].type != TT_KEYWORD or not line[lineIndex].value in ("data","instruct"):
			return Error("Type Error","Expected tape identifier")
		TAPE.pointer=line[lineIndex].value[0]
		lineIndex+=1
		if line[lineIndex].type != TT_INT:
			return Error("Type Error","Expected tape index")
		TAPE.index += line[lineIndex].value
	def moveAbsolute(self,line,lineIndex):
		lineIndex+=1
		#print("mopving")
		if line[lineIndex].type != TT_KEYWORD or not line[lineIndex].value in ("data","instruct"):
			return Error("Type Error","Expected tape identifier")
		TAPE.pointer=line[lineIndex].value[0]
		lineIndex+=1
		if line[lineIndex].type != TT_INT:
			return Error("Type Error","Expected tape index")
		TAPE.index = line[lineIndex].value
	def print(self,line,lineIndex):
		lineIndex+=1
		out=self.assess(line[lineIndex:])
		if type(out)==Error:
			return out
		print(out,end="")

	def assess(self,line):
		node= self.noderize(line)
		output = self.evaluate(node)
		if output:
			return output.value
	def evaluate(self,node):
		if type(node)==Call:
			if not node.func in BUILTIN.symbols.keys():
				return Error("Name Error","Unidentified Name:  "+node.func)

			return BUILTIN.get(node.func)(node.params)
		if type(node)==Token:
			return node
		if type(node)==BinOp:
			#print(node)
			a = self.evaluate(node.a)
			b= self.evaluate(node.b)
			op = node.op
			#print("\nBinOP")
			#print(a,b,op)
			invalid = Error("Invalid Operation","Cannot Evaluate " + a.type + " & " + b.type)
			if a.type in (TT_INT,TT_FLOAT):
				if b.type in (TT_FLOAT,TT_INT):
					#print("OPeration : ",self.operate(a,b,op), op.type==TT_PLUS)
					return Token(TT_FLOAT,self.operate(a,b,op.type))
				else:
					return invalid
			if a.type == TT_STRING:
				if b.type==TT_STRING and op==TT_PLUS:
					return Token(TT_STRING,self.operate(a,b,op.type))
				else:
					return invalid
			if a.type == "LIST":
				pass
	def operate(self,a,b,op):
		#print(op)
		if op==TT_PLUS:
			return a.value + b.value
		if op==TT_MINUS:
			return a.value - b.value
		if op==TT_MUL:
			return a.value * b.value
		if op==TT_DIV:
			return a.value / b.value
		if op==TT_MOD:
			return a.value % b.value
		if op==TT_LT:
			return int(a.value < b.value)
		if op==TT_LTE:
			return int(a.value <= b.value)
		if op==TT_GT:
			return int(a.value > b.value)
		if op==TT_GTE:
			return int(a.value >= b.value)

	def noderize(self,line):

		'''temp=[]
		for i in line:
			if i.type == TT_KEYWORD:
				temp.append(SymbolTable.get(i.value))
			else:
				temp.append(i)'''
		'''for i,j in zip(range(len(line)),range(1,len(line))):
			if line[i].type==TT_KEYWORD and line[j].type==TT_LPAREN:
				ind=j
				params=[]
				while 1:
					ind+=1
					if ind==len(line)-1:
						return Error("Syntax Error","Expected ')'")
					if line[ind].type==TT_RPAREN:'''
		if len(line)==1:
			#print(line,type(line[0]))
			return line[0]
		if line[0].type==TT_IDENTIFIER:
			if line[1].type != TT_LPAREN:
				return Error("Syntax Error","Expected '(")
			params = []
			ind=1
			for i in line[2:]:
				ind+=1
				if i.type==TT_RPAREN:
					if ind>=len(line)-1:
						return Call(line[0].value,params)
					else:
						return BinOp(Call(line[0].value,params),self.noderize(line[ind+2:]),line[ind+1])
				else:
					params.append(i)
		#print("LINE",line,)
		#print("L2 ",self.noderize(line[2:]))
		return BinOp(line[0],self.noderize(line[2:]),line[1])

						

	def execute(self):
		errors = self.tape()
		TAPE.pointer="i"
		TAPE.index=0
		if type(errors) == Error:
			return errors
		while 1:
			finish = self.visit()
			if finish:
				break
	def tape(self):
		index=0
		while 1:
			while self.tokens[index].type==TT_NEWLINE:
				index+=1
			if self.tokens[index].type==TT_EOF:
				break
			#print(self.tokens[index])
			if not self.tokens[index].value in ["data",'instruct'] and self.tokens[index].type==TT_KEYWORD:
				return Error("TypeError","Expected tape identifier")
			tapeIdentifier=self.tokens[index].value[0]
			index+=1
			if not self.tokens[index].type==TT_INT:
				return Error("TypeError","Expected tape location")
			tapeLocation = self.tokens[index].value
			index+=1
			tapeBody = []
			while 1:
				if self.tokens[index]==TT_EOF:
					return Error("EOF Error","Reached unexpected EOF while parsing")
				if self.tokens[index].type==TT_KEYWORD and self.tokens[index].value == "close":
					index+=1
					break
				tapeBody.append(self.tokens[index])
				index+=1
			TAPE.pointer=tapeIdentifier
			TAPE.index=tapeLocation
			TAPE.set(tapeBody)
			if self.tokens[index].type==TT_EOF:
				break
		return None


def run(fn,text):
	lexed = Lexer(fn,text)
	tokens = lexed.make_tokens()
	if type(tokens)==Error:
		print(tokens.toString())
		return
	#print(tokens)
	executor = Executor(tokens[0])
	e=executor.execute()

	if type(e)==Error:
		print(e.toString())
		return
	#print(TAPE.data)
	#print(fn)
if __name__=="__main__":
	run("helloworld.mol",open("helloworld.mol",'r').read())
	#print(open("helloworld.mol",'r').read())