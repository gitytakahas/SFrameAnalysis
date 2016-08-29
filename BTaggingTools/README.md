# BTaggingTools
Tools for b-tagging scale factors and efficiencies
CMSSW80 uses softrop subjets instead of pruned for subjet b-tagging 

## Properties

| Name                             | default              |
| -------------------------------- | -------------------- |
| m_name + "_Tagger"               | "CSVv2" |
| m_name + "_WorkingPoint"         |  "Loose" |
| m_name + "_CsvFile",             | sframe_dir + "/../BTaggingTools/csv/CSVv2.csv" |
| m_name + "_MeasurementType_udsg" | "comb" |
| m_name + "_MeasurementType_bc"   | "mujets" |
| m_name + "_EffHistDirectory"     | "bTagEff" |
| m_name + "_EffFile"              | sframe_dir + "/../BTaggingTools/efficiencies/bTagEffs.root" |

## Usage

### header file

```#include "../BTaggingTools/include/BTaggingScaleTool.h"
[..]

private:
  BTaggingScaleTool m_bTaggingScaleTool;

[..]
```

### implementation

constructor:
```
VHAnalysis::VHAnalysis()
 : SCycleBase()
 , [..]
 , m_bTaggingScaleTool( this )
{
```

In `BeginInputData( const SInputData& id )`:
```
// b-tagging tool initialisation
m_bTaggingScaleTool.BeginInputData( id );

// if you want to fill efficiencies later:
if (m_isSignal) {
  // b-tagging efficiencies
  m_bTaggingScaleTool.bookHistograms();
}
```

In `ExecuteEvent()`, after you've performed some kind of signal selection:
```
if (m_isSignal) {
  std::vector<UZH::Jet> selectedJets;
  selectedJets.push_back(vectorJet);
  selectedJets.push_back(higgsJet);
  m_bTaggingScaleTool.fillEfficiencies(selectedJets);
  m_bTaggingScaleTool.fillSoftdropSubjetEfficiencies(selectedJets);
}
```

Furthermore, it is recommended to use the working points defined in the BTaggingScaleTool to identify if a jet is b-tagged, e.g.:
```
if (m_bTaggingScaleTool.isTagged(higgsJet.subjet_softdrop_csv()[i])) {
  ++nTaggedSubjets;
}
```

To get the scale factor, pass either a vector of `UZH::Jet` or individual `UZH::Jet`, mind the different functions for subjet and normal jet b-tagging:
```
if (!m_isData) {
  b_weight = getEventWeight(); // could be pileup weights etc.
  std::vector<UZH::Jet> selectedJets;
  selectedJets.push_back(vectorJet);
  selectedJets.push_back(higgsJet);
  // b_weightBtag = m_bTaggingScaleTool.getScaleFactor(selectedJets); // event b-tag SF weight
  b_weightBtag = m_bTaggingScaleTool.getSoftdropSubjetScaleFactor(selectedJets); // event b-tag SF weight
    
    b_weight *= b_weightBtag;
  }
}
```

### XML

Don't forget to add the shared library to the XML files!