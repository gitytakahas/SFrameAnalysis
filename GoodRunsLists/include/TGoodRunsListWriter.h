// Dear emacs, this is -*- c++ -*-
// $Id: TGoodRunsListWriter.h 173077 2011-06-22 20:17:18Z krasznaa $
#ifndef SFRAME_GOODRUNSLISTS_TGoodRunsListWriter_H
#define SFRAME_GOODRUNSLISTS_TGoodRunsListWriter_H

// STL include(s):
#include <vector>

// ROOT include(s):
#include "TObject.h"
#include "TString.h"

// SFrame include(s):
#include "core/include/SLogger.h"

// Local include(s):
#include "TGoodRunsList.h"
#include "TGRLCollection.h"

// Type definitions:                                                                                                                                                          
typedef unsigned char xmlChar;
typedef struct _xmlTextWriter xmlTextWriter;
typedef xmlTextWriter* xmlTextWriterPtr;

namespace Root {

   // Forward declaration(s):
   class TLumiBlockRange;
   class TGoodRun;
   class TGoodRunsList;

   /**
    *  @short Class capable of writing GRL XMLs
    *
    *         This class should be used to write out GRL XML files. Should only be used
    *         in special circumstances in an analysis. (Analyses usually only want to
    *         read GRLs, and not write them.)
    *
    *         Didn't clean up the source code quite as much as I did on the other classes.
    *         If anyone's willing to work on it, be my guest. But the code is fully
    *         functional in its current form, so that's good enough for me at the
    *         moment.
    *
    * @author Max Baak <mbaak@cern.ch> - CERN, Switzerland
    * @author Attila Krasznahorkay <Attila.Krasznahorkay@cern.ch>
    *
    * $Revision: 173077 $
    * $Date: 2011-06-22 22:17:18 +0200 (Wed, 22 Jun 2011) $
    */
   class TGoodRunsListWriter : public TObject {

   public:
      /// Default constructor
      TGoodRunsListWriter();
      /// Constructor with a GRL object and an XML name
      TGoodRunsListWriter( const TGoodRunsList& goodrunslist, const TString& dataCardName );
      /// Destructor
      ~TGoodRunsListWriter();

      /// Write a single XML file from the information
      Bool_t WriteXMLFile();
      /// Write XML files from the information
      Bool_t WriteXMLFiles();
      /// Turn the GRL info into a single XML string
      const TString& GetXMLString();
      /// Turn the GRL info into XML strings
      const std::vector< TString >& GetXMLStrings();

      /// Get the output file name
      inline const TString& GetFilename() const { return m_dataCardName; }
      /// Get the merged GRL
      inline const TGoodRunsList
      GetMergedGoodRunsList( const Root::BoolOperation& operation = OR ) const {
         return m_grlvec.GetMergedGoodRunsList( operation );
      }
      /// Get the full GRL collection
      inline const TGRLCollection& GetGRLCollection() const { return m_grlvec; }

      /// Merge the good runs lists?
      inline void SetMergeGoodRunsLists( bool merge = true ) { m_mergegrls=merge; }
      /// Check the GRL metadata info?
      inline void SetCheckGRLInfo( bool check = true ) { m_grlvec.SetCheckGRLInfo( check ); }
      inline void  SetIndividuals( bool indf = true ) { m_individuals=indf; }

      void SetGRLCollection( const TGRLCollection& grlvec )     { reset(); m_grlvec=grlvec; } 
      void SetGoodRunsList( const TGoodRunsList& goodrunslist ) { reset(); m_grlvec.push_back(goodrunslist); } 
      void SetFilename( const TString& dataCardName )           { m_dataCardName=dataCardName; }
      void SetPrefix( const TString& prefix )                   { m_prefix=prefix; }
      void AddGoodRunsList( const TGoodRunsList& goodrunslist ) { m_grlvec.push_back(goodrunslist); }

   private: 
      // aux method
      void reset();

      Bool_t WriteLumiRangeCollection(xmlTextWriterPtr writer);
      Bool_t WriteNamedLumiRange(xmlTextWriterPtr writer);
      Bool_t WriteMetadata(xmlTextWriterPtr writer);
      Bool_t WriteLumiBlockCollection(xmlTextWriterPtr writer, const TGoodRun& goodrun);
      Bool_t WriteElement(xmlTextWriterPtr writer, const char* name, const char* value=0, 
                          const char* atr1=0, const char* val1=0, const char* atr2=0,
                          const char* val2=0);

      xmlChar* ConvertInput(const char *in, const char *encoding);

      TGRLCollection m_grlvec;
      TGoodRunsList m_grl;

      std::vector< TString > m_xmlstringVec;
      TString m_xmlstring;
      TString m_dataCardName;
      TString m_prefix;

      mutable SLogger m_logger;

      Bool_t m_mergegrls;
      Bool_t m_individuals;

   }; // class TGoodRunsListWriter

} // namespace Root

#endif // SFRAME_GOODRUNSLISTS_TGoodRunsListWriter_H
