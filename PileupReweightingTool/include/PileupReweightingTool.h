#ifndef __PILEUPREWEIGHTINGTTOOL_H__
#define __PILEUPREWEIGHTINGTTOOL_H__

// SFrame include(s):
#include "core/include/SError.h"
#include "plug-ins/include/SToolBase.h"

#include "PUWeight.h"

namespace Root{
  class TPileupReweighting;
}

class PileupReweightingTool : public SToolBase {

 public:
  /// constructor
  PileupReweightingTool( SCycleBase* parent, const char* name = "PileupReweightingTool" );

  /// destructor
  ~PileupReweightingTool();

  /// open input file
  void BeginInputData( const SInputData& id ) throw( SError );

 /// get weight
 double getPileUpweight( float mu );


 private:
  std::string m_name;                 ///< name of the tool
  PUWeight m_puWeight;      ///< instance of PUWeight class
  
  // tool properties
  std::string m_histoPath;
  std::string m_dataRootFileName;
  std::string m_dataRootHistName;
  std::string m_mcScenario;
  
};


#endif //  __PILEUPREWEIGHTINGTTOOL_H__
