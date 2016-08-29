# GoodRunsLists
JSON file parser for CMS data quality in SFrame

## Instructions

### implementation (*.cxx)

This assumes that you have a variable called `m_jsonName` that contains the location of your JSON file and also a flag `m_isData` that tells whether you're running on data or not.

```
// External include(s):
#include "../../GoodRunsLists/include/TGoodRunsListReader.h"
...
void MyAnalysis::BeginCycle() throw( SError ) {

  //
  // Load the GRL:
  //
  if (m_isData) {
    m_logger << INFO << "Loading GoodRunsList from file: " << m_jsonName << SLogger::endmsg;
    Root::TGoodRunsListReader reader( TString( m_jsonName.c_str() ) );
    if( ! reader.Interpret() ) {
      m_logger << FATAL << "Couldn't read in the GRL!" << SLogger::endmsg;
      throw SError( ( "Couldn't read in file: " + m_jsonName ).c_str(), SError::SkipCycle );
    }
    m_grl = reader.GetMergedGoodRunsList();
    m_grl.Summary();
    m_grl.SetName( "MyGoodRunsList" );
  
    //
    // Add it as a configuration object, so that the worker nodes will receive it:
    //
    AddConfigObject( &m_grl );
  }
  
   return;

}

...

void MyAnalysis::BeginInputData( const SInputData& ) throw( SError ) {

  if (m_isData) {
    TObject* grl;
    if( ! ( grl = GetConfigObject( "MyGoodRunsList" ) ) ) {
      m_logger << FATAL << "Can't access the GRL!" << SLogger::endmsg;
      throw SError( "Can't access the GRL!", SError::SkipCycle );
    }
    m_grl = *( dynamic_cast< Root::TGoodRunsList* >( grl ) );
  }
  
   return;

}

...

void MyAnalysis::ExecuteEvent( const SInputData&, Double_t ) throw( SError ) {
  
  // might be better in a separate function (e.g. bool MyAnalysis::isGoodEvent(runNumber, lumiSection))
  if (m_isData) {
    bool isGood = m_grl.HasRunLumiBlock( runNumber, lumiSection );
    if( !isGood ) {
      m_logger << DEBUG << "Bad event! Run: " << runNumber <<  " - Lumi Section: " << lumiSection << SLogger::endmsg;
      throw SError( SError::SkipEvent );
    }
    else m_logger << DEBUG << "Good event! Run: " << runNumber <<  " - Lumi Section: " << lumiSection << SLogger::endmsg;
  }
  
}

```

### header file


```
// External include(s):
#include "../../GoodRunsLists/include/TGoodRunsList.h"
...
class MyAnalysis : public SCycleBase {

public:

...

private:

  //
  // Further objects
  //
  Root::TGoodRunsList m_grl;
...
```

### XML config

In the `JobConfiguration` part, add before the `Library` of your analysis code:
`<Library Name="libGoodRunsLists" />`

## Acknowledgements

The JSON parser is taken from https://github.com/open-source-parsers/jsoncpp
Most of the other code is taken from Max Baak and Attila Krasznahorkay, who developed this code for ATLAS analyses.