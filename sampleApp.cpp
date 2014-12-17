#include "example/cpp/tinyxml2.h"
#include "example/cpp/xml.hpp"
#include "example/cpp/A.hpp"
#include "example/cpp/B.hpp"
#include "example/cpp/C.hpp"

#include <iostream>

int main(){
	tinyxml2::XMLDocument doc;
	doc.LoadFile("example.xml");

	tinyxml2::XMLElement *elem = doc.FirstChildElement("xml");

	Xml xml;

	std::cout << xml.moduleName << std::endl;

	xml.loadXml(elem);

	for(auto iter: xml.get_A()){
		for(auto iter2: iter.get_B()){
			std::cout << iter2.get_id() << std::endl;
		}
	}

	std::cout << elem << std::endl;
}