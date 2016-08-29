#include "../include/ContainerBase.h"


using namespace std;
using namespace UZH;

void ContainerBase::Set(string name, int value) {

  map_int[name]=value;

}


void ContainerBase::Set(string name, double value) {

  map_double[name]=value;

}


int ContainerBase::GetInt(string name) const {

  int prop = -999;
  map<string, int>::const_iterator iter = map_int.find(name);
  if(iter != map_int.end())
    prop = iter->second;
  return prop;

}



double ContainerBase::GetDouble(string name) const {

  double prop = -999.;
  map<string, double>::const_iterator iter = map_double.find(name);
  if(iter != map_double.end())
    prop = iter->second;
  return prop;

}


vector<string> ContainerBase::GetIntKeys() {

  vector<string> keys;
  for(map<string,int>::iterator it = map_int.begin(); it!=map_int.end(); ++it)
    keys.push_back(it->first);
  return keys;

}


vector<string> ContainerBase::GetDoubleKeys() {

  vector<string> keys;
  for(map<string,double>::iterator it = map_double.begin(); it!=map_double.end(); ++it)
    keys.push_back(it->first);
  return keys;

}


void ContainerBase::Reset() {

  //empty maps
  map_int.clear();
  map_double.clear();

}


ContainerBase::ContainerBase() {

  //initianalize everything with default values
  Reset();

}


ContainerBase::~ContainerBase() {

  //cleanup - currently nothing to do

}


std::ostream& ContainerBase::print(std::ostream& out) {

  /*ostream& operator<<( ostream& out,
                     ContainerBase& rhs ) {
*/
  vector<string> intKeys = GetIntKeys();
  out << " integer map:";
  for(vector<string>::iterator it = intKeys.begin(); it!=intKeys.end(); ++it)
    out << " " << *it << ":" << GetInt(*it);
  vector<string> doubleKeys = GetDoubleKeys();
  out << " double map:";
  for(vector<string>::iterator it = doubleKeys.begin(); it!=doubleKeys.end(); ++it)
    out << " " << *it << ":" << GetDouble(*it);
  return out;

}


// with overloaded operators:
// std::ostream& operator<<(std::ostream & out, printable & rhs) {
// 
//   return rhs.print(out); //simply call the print method.
// 
// }

