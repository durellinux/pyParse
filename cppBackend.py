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
			h.write("#include \""+c+".hpp\""+"\n")

	h.write("#include <vector>\n")
	h.write("#include <string>\n")
	h.write("#include <iostream>\n")
	f.write("#include \""+curClassName+".hpp\""+"\n")
	h.write("#include \"tinyxml2.h\"\n")

	# f.write("from xml.dom.minidom import Node\n")

def printClass(name):
	global f
	h.write("class "+name)
	#print "class "+name+"():"

def printMethod(name,params,curClassName="TODO", returnType="void"):
	h.write("\t\t\t"+returnType+" "+name+"("+params+");\n")
	f.write(returnType+" "+curClassName+"::"+name+"("+params+")\n")
	#print "\tdef "+name+"("+params+"):"

def printInstruction(instruction, hpp = 0):
	if hpp:
		h.write("\t\t"+instruction+"\n")
	else:
		f.write("\t\t"+instruction+"\n")
	#print "\t\t"+instruction

class CppBackend(object):
	def __init__(self, path):
		self.path=path+os.sep+"cpp"+os.sep
		pass

	def write(self, classes, classesName, firstTag):

		os.system("mkdir -p "+self.path)

		global f
		global h

		for c in classes:
			f=open(self.path+cleanName(c.name)+".cpp","w")
			h=open(self.path+cleanName(c.name)+".hpp","w")

			printInstruction("#ifndef "+c.moduleName+"_INCLUDE", 1)
			printInstruction("#define "+c.moduleName+"_INCLUDE", 1)

			printIncludes(c.tags, c.moduleName)
			
			printInstruction("", 1)
			printInstruction("", 1)
			printClass(cleanName(c.name))			
			printInstruction("{", 1)
			printInstruction("public:", 1)
			printInstruction("\tstd::string moduleName = \"" + c.moduleName + "\";", 1)
			printInstruction("\t" + cleanName(c.moduleName) + "(){};", 1)
			printInstruction("", 1)

			for attr in c.attrs:
				printInstruction("\tstd::string "+cleanName(attr)+" = \"\";", 1)
			
			for tagId in range(0,len(c.tags)):
				tag=c.tags[tagId]
				printInstruction("\tstd::vector<"+cleanName(tag)+"> "+cleanName(tag)+"list;", 1)

			printInstruction("\tstd::string _text = \"\";", 1)

			# if len(c.tags)+len(c.attrs)==0:
			# 	print "\t\tpass"

			# #CLEAN NAME
			# printMethod("cleanName","self, string")
			# printInstruction("newName=string")
			# printInstruction("if newName=='class' or newName=='xml':")
			# printInstruction("	newName=newName.capitalize()")
			# printInstruction("newName=newName.replace('-','_')")
			# printInstruction("newName=newName.replace(':','_')")
			# printInstruction("")
			# printInstruction("return newName")


			#ATTRIBUTES GETTERS
			for attr in c.attrs:
				printMethod("get_"+cleanName(attr),"", cleanName(c.moduleName), "std::string")
				printInstruction("{")
				printInstruction("return this->"+cleanName(attr) + ";")
				printInstruction("}")
				printInstruction("")

			#ATTRIBUTES SETTERS
			for attr in c.attrs:
				printMethod("set_"+cleanName(attr),"std::string value", cleanName(c.moduleName), "void")
				printInstruction("{")
				printInstruction("this->"+cleanName(attr)+"= value;")
				printInstruction("}")
				printInstruction("")

			#SUBLCASS GETTER:
			for tag in c.tags:
				printMethod("get_"+cleanName(tag),"", cleanName(c.moduleName), "std::vector<"+cleanName(tag)+">")
				printInstruction("{")
				printInstruction("return this->"+cleanName(tag) + "list;")
				printInstruction("}")
				printInstruction("")

			#SUBLCASS SETTER:
			for tag in c.tags:
				printMethod("set_"+cleanName(tag), cleanName(tag)+" tag", cleanName(c.moduleName), "void")
				printInstruction("{")
				printInstruction("this->"+cleanName(tag)+"list.push_back(tag);")
				printInstruction("}")
				printInstruction("")

			# #GET_BY_ID:
			# printMethod("getById","self,id")
			# printInstruction("if hasattr(self,\"id\") and self.id==id:")
			# printInstruction("\treturn self")
			# printInstruction("")
			# printInstruction("result=None")
			# for tag in c.tags:
			# 	printInstruction("for el in self."+cleanName(tag)+":")
			# 	printInstruction("\tresult=el.getById(id)")
			# 	printInstruction("\tif result!=None:")
			# 	printInstruction("\t\treturn result")
			# 	printInstruction("")

			# printInstruction("return None")
			# printInstruction("")
			# printInstruction("")

			# #GET_BY_ATTR_VALUES:
			# printMethod("getByAttrValues","self,className,tuples,foundList=None")
			
			# printInstruction("if foundList==None:")
			# printInstruction("\tfoundList=list()")
			
			# printInstruction("found=True")

			# printInstruction("if self.moduleName==self.cleanName(className):")
			# printInstruction("\tfor t in tuples:")
			# printInstruction("\t\tattrName=self.cleanName(t[0])")
			# printInstruction("\t\tattrVal=t[1]")
			# printInstruction("\t\tif not(hasattr(self,attrName) and eval('self.'+attrName)==attrVal):")
			# printInstruction("\t\t\tfound=found and False")
			# printInstruction("\tif found:")
			# printInstruction("\t\tfoundList.append(self)")
			# printInstruction("")
			# for tag in c.tags:
			# 	printInstruction("for el in self."+cleanName(tag)+":")
			# 	printInstruction("\tel.getByAttrValues(className, tuples, foundList)")
			# 	printInstruction("")

			# printInstruction("return foundList")
			# printInstruction("")

			# #GET SPECS:
			# if "specs" in c.tags:
			# 	printMethod("getSpecValue","self,specName")
			# 	printInstruction("for spec in self.get_specs():")
			# 	printInstruction("\tif spec.name==specName:")
			# 	printInstruction("\t\treturn spec.value")
			# 	printInstruction("return None")
			# 	printInstruction("")

			#LOAD TEXT CONTENT:
			# printMethod("getText","self,nodeList")
			# printInstruction("for node in nodeList:")
			# printInstruction("\tif node.nodeType == node.TEXT_NODE:")
			# printInstruction("\t\tif self._text == None:")
			# printInstruction("\t\t\tself._text=''")
			# printInstruction("\t\tself._text+=node.data")
			# printInstruction("")
			# printInstruction("")
	
			#LOAD XML:
			printMethod("loadXml","tinyxml2::XMLElement *elem", cleanName(c.moduleName), "void")
			printInstruction("{")
			# printInstruction("self.getText(node.childNodes)")
			# printInstruction("if node.nodeType!=Node.ELEMENT_NODE:")
			# printInstruction("\tfor n in node.childNodes:")
			# printInstruction("\t\tif n.nodeType==Node.ELEMENT_NODE and n.localName == '"+firstTag+"':")
			# printInstruction("\t\t\tself.loadXml(n)")

			# if len(c.attrs)+len(c.tags)>0:
			# 	printInstruction("else:")

			if len(c.tags) > 0:
				for tag in c.tags:
					printInstruction("\tfor (tinyxml2::XMLElement* child = elem->FirstChildElement(); child != NULL; child = child->NextSiblingElement()){")
					printInstruction("\t\tstd::string nodeName = child->Name();")
					printInstruction("\t\tif(nodeName.compare(\""+tag+"\") == 0){")
					printInstruction("\t\t\t"+cleanName(tag)+" temp;")
					printInstruction("\t\t\ttemp.loadXml(child);");
					printInstruction("\t\t\tthis->set_"+cleanName(tag)+"(temp);")
					printInstruction("\t\t}")
					printInstruction("\t}")
					# printInstruction("\tfor n in node.childNodes:")
					# printInstruction("\t\tif n.nodeType==Node.ELEMENT_NODE and n.localName == '"+tag+"':")
					# printInstruction("\t\t\tel="+cleanName(tag)+"()")
					# printInstruction("\t\t\tel.loadXml(n)")
					# printInstruction("\t\t\tself.set_"+cleanName(tag)+"(el)")
					# printInstruction("")			
			
			if len(c.attrs)>0:
				for attr in c.attrs:
					printInstruction("\tthis->"+cleanName(attr)+" = elem->Attribute(\""+attr+"\");")

			printInstruction("")
			printInstruction("")

			printInstruction("}")


			# #WRITE XML:

			# printMethod("addToXmlString","self, attr, name, string")
			# printInstruction("if attr!=None:")
			# printInstruction("\tstring+=' '+name+'=\"'+attr+'\"'")
			# printInstruction("return string")
			# printInstruction("")
			# printInstruction("")

			# printMethod("writeXml","self,outFile,indent")
			# printInstruction("string='<'+self.moduleName")

			# for attr in c.attrs:
			# 	printInstruction("string=self.addToXmlString(self."+cleanName(attr)+",'"+attr+"',string)")
			
			# if len(c.tags)==0:
			# 	printInstruction("if self._text==None:")
			# 	printInstruction("\tstring+='/>'")
			# 	printInstruction("else:")
			# 	printInstruction("\tstring+='>'+self._text+'</'+self.moduleName+'>'")
			# 	printInstruction("outFile.write(indent+string+'\\n')")
			# 	printInstruction("")

			# else:
			# 	printInstruction("string+='>'")
			# 	printInstruction("outFile.write(indent+string+'\\n')")
			# 	printInstruction("")
			# 	printInstruction("indent+='\t'")
			# 	for tag in c.tags:
			# 		printInstruction("for el in self."+cleanName(tag)+":")
			# 		printInstruction("\tif hasattr(el, 'writeXml'):")
			# 		printInstruction("\t\tel.writeXml(outFile,indent)")
			# 		printInstruction("")
			# 	printInstruction("indent=indent[:-1]")

			# 	printInstruction("outFile.write(indent+'</'+self.moduleName+'>\\n')")
			# 	printInstruction("")
			# 	printInstruction("")

			# f.close()

			printInstruction("};", 1)

			printInstruction("#endif", 1)