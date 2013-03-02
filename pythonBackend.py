import os

def cleanName(string):
	newName=string
	if newName=="class" or newName=="xml":
		newName=newName.capitalize()
	newName=newName.replace("-","_")
	newName=newName.replace(":","_")

	return newName

def printIncludes(classesName, curClassName):
	global f
	for c in classesName:
		if c!=curClassName:
			f.write("from "+c+" import "+c+"\n")

	f.write("from xml.dom.minidom import Node\n")

def printClass(name):
	global f
	f.write("class "+name+"():\n")
	#print "class "+name+"():"

def printMethod(name,params):
	f.write("\tdef "+name+"("+params+"):\n")
	#print "\tdef "+name+"("+params+"):"

def printInstruction(instruction):
	f.write("\t\t"+instruction+"\n")
	#print "\t\t"+instruction

class PythonBackend(object):
	def __init__(self, path):
		self.path=path+os.sep+"python"+os.sep
		pass

	def write(self, classes, classesName, firstTag):

		os.system("mkdir -p "+self.path)

		global f

		for c in classes:
			f=open(self.path+cleanName(c.name)+".py","w")

			printIncludes(c.tags,c.moduleName)
			printInstruction("")
			printInstruction("")

			printClass(cleanName(c.name))

			#INIT METHOD
			printMethod("__init__","self")
			printInstruction("self.moduleName='"+c.name+"'")

			print c.name+": "
			print "\t"+str(c.attrs)
			print "\t"+str(c.tags)

			for attr in c.attrs:
				printInstruction("self."+cleanName(attr)+"=None")
			
			for tagId in range(0,len(c.tags)):
				tag=c.tags[tagId]
				printInstruction("self."+cleanName(tag)+"=list()")

			printInstruction("self._text=None")

			printInstruction("")
			printInstruction("")
			
			# if len(c.tags)+len(c.attrs)==0:
			# 	print "\t\tpass"

			#CLEAN NAME
			printMethod("cleanName","self, string")
			printInstruction("newName=string")
			printInstruction("if newName=='class' or newName=='xml':")
			printInstruction("	newName=newName.capitalize()")
			printInstruction("newName=newName.replace('-','_')")
			printInstruction("newName=newName.replace(':','_')")
			printInstruction("")
			printInstruction("return newName")


			#ATTRIBUTES GETTERS
			for attr in c.attrs:
				printMethod("get_"+cleanName(attr),"self")
				printInstruction("return self."+cleanName(attr))
				printInstruction("")
				printInstruction("")

			#ATTRIBUTES SETTERS
			for attr in c.attrs:
				printMethod("set_"+cleanName(attr),"self,value")
				printInstruction("self."+cleanName(attr)+"=str(value)")
				printInstruction("")
				printInstruction("")

			#SUBLCASS GETTER:
			for tag in c.tags:
				printMethod("get_"+cleanName(tag),"self")
				printInstruction("return self."+cleanName(tag))
				printInstruction("")
				printInstruction("")

			#SUBLCASS SETTER:
			for tag in c.tags:
				printMethod("set_"+cleanName(tag),"self,tag")
				printInstruction("self."+cleanName(tag)+".append(tag)")
				printInstruction("")
				printInstruction("")


			#GET_BY_ID:
			printMethod("getById","self,id")
			printInstruction("if hasattr(self,\"id\") and self.id==id:")
			printInstruction("\treturn self")
			printInstruction("")
			printInstruction("result=None")
			for tag in c.tags:
				printInstruction("for el in self."+cleanName(tag)+":")
				printInstruction("\tresult=el.getById(id)")
				printInstruction("\tif result!=None:")
				printInstruction("\t\treturn result")
				printInstruction("")

			printInstruction("return None")
			printInstruction("")
			printInstruction("")

			#GET_BY_ATTR_VALUES:
			printMethod("getByAttrValues","self,className,tuples,foundList=None")
			
			printInstruction("if foundList==None:")
			printInstruction("\tfoundList=list()")
			
			printInstruction("found=True")

			printInstruction("if self.moduleName==self.cleanName(className):")
			printInstruction("\tfor t in tuples:")
			printInstruction("\t\tattrName=self.cleanName(t[0])")
			printInstruction("\t\tattrVal=t[1]")
			printInstruction("\t\tif not(hasattr(self,attrName) and eval('self.'+attrName)==attrVal):")
			printInstruction("\t\t\tfound=found and False")
			printInstruction("\tif found:")
			printInstruction("\t\tfoundList.append(self)")
			printInstruction("")
			for tag in c.tags:
				printInstruction("for el in self."+cleanName(tag)+":")
				printInstruction("\tel.getByAttrValues(className, tuples, foundList)")
				printInstruction("")

			printInstruction("return foundList")
			printInstruction("")



			#GET SPECS:
			if "specs" in c.tags:
				printMethod("getSpecValue","self,specName")
				printInstruction("for spec in self.get_specs():")
				printInstruction("\tif spec.name==specName:")
				printInstruction("\t\treturn spec.value")
				printInstruction("return None")
				printInstruction("")

			#LOAD TEXT CONTENT:
			printMethod("getText","self,nodeList")
			printInstruction("for node in nodeList:")
			printInstruction("\tif node.nodeType == node.TEXT_NODE:")
			printInstruction("\t\tif self._text == None:")
			printInstruction("\t\t\tself._text=''")
			printInstruction("\t\tself._text+=node.data")
			printInstruction("")
			printInstruction("")
	
			#LOAD XML:
			printMethod("loadXml","self,node")
			printInstruction("self.getText(node.childNodes)")
			printInstruction("if node.nodeType!=Node.ELEMENT_NODE:")
			printInstruction("\tfor n in node.childNodes:")
			printInstruction("\t\tif n.nodeType==Node.ELEMENT_NODE and n.localName == '"+firstTag+"':")
			printInstruction("\t\t\tself.loadXml(n)")

			if len(c.attrs)+len(c.tags)>0:
				printInstruction("else:")

			for tag in c.tags:
				printInstruction("\tfor n in node.childNodes:")
				printInstruction("\t\tif n.nodeType==Node.ELEMENT_NODE and n.localName == '"+tag+"':")
				printInstruction("\t\t\tel="+cleanName(tag)+"()")
				printInstruction("\t\t\tel.loadXml(n)")
				printInstruction("\t\t\tself.set_"+cleanName(tag)+"(el)")
				printInstruction("")			
			
			if len(c.attrs)>0:
				printInstruction("\tif node.hasAttributes():")
				printInstruction("\t\tattrs=node.attributes")
				for attr in c.attrs:
					printInstruction("\t\tattrId='"+attr+"'")
					printInstruction("\t\tif attrId in attrs.keys():")
					printInstruction("\t\t\tself."+cleanName(attr)+"=str(attrs[attrId].value)")
					printInstruction("")
			printInstruction("")
			printInstruction("")


			#WRITE XML:

			printMethod("addToXmlString","self, attr, name, string")
			printInstruction("if attr!=None:")
			printInstruction("\tstring+=' '+name+'=\"'+attr+'\"'")
			printInstruction("return string")
			printInstruction("")
			printInstruction("")

			printMethod("writeXml","self,outFile,indent")
			printInstruction("string='<'+self.moduleName")

			for attr in c.attrs:
				printInstruction("string=self.addToXmlString(self."+cleanName(attr)+",'"+attr+"',string)")
			
			if len(c.tags)==0:
				printInstruction("if self._text==None:")
				printInstruction("\tstring+='/>'")
				printInstruction("else:")
				printInstruction("\tstring+='>'+self._text+'</'+self.moduleName+'>'")
				printInstruction("outFile.write(indent+string+'\\n')")
				printInstruction("")

			else:
				printInstruction("string+='>'")
				printInstruction("outFile.write(indent+string+'\\n')")
				printInstruction("")
				printInstruction("indent+='\t'")
				for tag in c.tags:
					printInstruction("for el in self."+cleanName(tag)+":")
					printInstruction("\tif hasattr(el, 'writeXml'):")
					printInstruction("\t\tel.writeXml(outFile,indent)")
					printInstruction("")
				printInstruction("indent=indent[:-1]")

				printInstruction("outFile.write(indent+'</'+self.moduleName+'>\\n')")
				printInstruction("")
				printInstruction("")

			f.close()
