from xml.dom.minidom import parse,Node,NamedNodeMap

from pythonBackend import PythonBackend
from cppBackend import CppBackend

import sys
import os

if len(sys.argv)!=4:
	print "USAGE: python pyparse.py fileName(No extension) extension firstTag"
	sys.exit(1)

xmlFile=sys.argv[1]
extension=sys.argv[2]
firstTag=sys.argv[3]

xmlName=xmlFile+"."+extension

xml=open(xmlName,"r")

class xmlObj(object):
	def __init__(self, name):
		self.name=str(name)
		self.moduleName=str(name)
		self.tags=list()
		self.tagsCount=list()
		self.attrs=list()

	def addTag(self,tag):
		if tag in self.tags:
			self.tagsCount[self.tags.index(tag)]+=1
		else:
			self.tags.append(str(tag))
			self.tagsCount.append(1)

	def addAttribute(self, name):
		if name not in self.attrs:
			self.attrs.append(str(name))

classes=list()
classNames=list()

def getNode(node):
	for n in node.childNodes:
		if n.nodeType==Node.ELEMENT_NODE:
			nodeName=n.localName
			
			nodeClass=None

			if nodeName in classNames:
				nodeClass=classes[classNames.index(nodeName)]
			else:
				nodeClass=xmlObj(nodeName)
				classes.append(nodeClass)
				classNames.append(nodeName)

			if n.hasAttributes():
				attrs=n.attributes
				for k in attrs.keys():
					nodeClass.addAttribute(attrs[k].name)

			for n1 in n.childNodes:
				if n1.nodeType==Node.ELEMENT_NODE:
					subNodeName=n1.localName
					nodeClass.addTag(subNodeName)

			getNode(n)

dom=parse(xml)

getNode(dom)

xml.close()


os.system("rm "+xmlFile+" -rf")

pyWriter=PythonBackend(xmlFile)
pyWriter.write(list(classes), list(classNames), firstTag)

cppWriter = CppBackend(xmlFile)
cppWriter.write(list(classes), list(classNames), firstTag)

#C++ backend?
#C# backend?