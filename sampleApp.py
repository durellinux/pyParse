import sys

#Add path to desired parser
sys.path.append("./example/python")

#Import xml minidom parse
from xml.dom.minidom import parse

#Import faster class
from Xml import Xml

xmlFileIn="example.xml"
xmlFileOut="exampleOut.xml"

xml=open(xmlFileIn,"r")
dom=parse(xml)
xml.close()

#Initialize Main Class
xmlClass=Xml()

#Parse XML
xmlClass.loadXml(dom)

#Get Text in the first tag C
CTag=xmlClass.get_C()[0]
cText=CTag._text

#Change tag C text
newcText=cText+"_new"
CTag._text=newcText

print "Old text: "+cText+"\tNew text: "+newcText

#Write information back
outFile=open(xmlFileOut,"w")
xmlClass.writeXml(outFile,"")
outFile.close()