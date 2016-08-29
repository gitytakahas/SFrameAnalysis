// Dear emacs, this is -*- c++ -*-
// $Id: TGoodRunsList.h 45093 2010-08-20 11:58:27Z krasznaa $
#ifndef SFRAME_GOODRUNSLISTS_TGoodRunsList_H
#define SFRAME_GOODRUNSLISTS_TGoodRunsList_H

// STL include(s):
#include <map>
#include <vector>
#include <string>

// ROOT include(s):
#include "TNamed.h"
#include "TString.h"

// Local include(s):
#include "TGoodRun.h"

namespace Root {

   /**
    *  @short Class describing a list of good runs
    *
    *         This class should be used in an analysis to decide if a specific luminosity
    *         block should enter the analysis or not. To decide that, use the function
    *         called TGoodRunsList::HasRunLumiBlock(...).
    *
    * @author Max Baak <mbaak@cern.ch> - CERN, Switzerland
    * @author Attila Krasznahorkay <Attila.Krasznahorkay@cern.ch>
    *
    * $Revision: 45093 $
    * $Date: 2010-08-20 13:58:27 +0200 (Fri, 20 Aug 2010) $
    */
   class TGoodRunsList : public std::map< Int_t, TGoodRun >, public TNamed {
      
   public:
      /// Default constructor
      TGoodRunsList();
      /// Constructor with an object name
      TGoodRunsList( const char* name );

      /// Copy constructor
      TGoodRunsList( const Root::TGoodRunsList& other );
      /// Assignment operator
      TGoodRunsList& operator=( const TGoodRunsList& other );

      /// Add a GRL object to this one
      void AddGRL( const TGoodRunsList& other );
      /// Get common GRL between two objects
      const Root::TGoodRunsList GetOverlapWith( const TGoodRunsList& other ) const;
      /// Get the union of two GRL objects
      const Root::TGoodRunsList GetSumWith( const TGoodRunsList& other ) const;
      /// Get the GRL that is only part of other and not this one
      const Root::TGoodRunsList GetPartOnlyIn( const TGoodRunsList& other ) const;
      /// Get the GRL that is only part of this one and not of other
      const Root::TGoodRunsList GetPartNotIn( const TGoodRunsList& other ) const;

      /// Does the GRL have trigger information?
      Bool_t HasTriggerInfo() const;
      /// Query whether the GRL contains a given run
      Bool_t HasRun( const Int_t& runnr ) const;
      /// Query whether the GRL contains a given run and luminosity block
      Bool_t HasRunLumiBlock( const Int_t& runnr, const Int_t& lumiblocknr ) const;
      /// Compare the GRL info of two objects
      Bool_t HasSameGRLInfo( const TGoodRunsList& other ) const;
      /// Check if there is an overlap between two GRL objects
      Bool_t HasOverlapWith( const TGoodRunsList& other, bool verb = false ) const;

      /// Add a single luminosity block to the object
      void AddRunLumiBlock( const Int_t& runnr, const Int_t& lumiblocknr );
      /// Set the version of the object
      inline void SetVersion( const TString& version ) { m_version = version; }
      /// Add a meta-data element
      inline void AddMetaData( const TString& key, const TString& value ) {
         m_metadata[ key ] = value;
      }
      /// Set the value of a meta-data element
      inline void SetMetaData( const std::map< TString, TString >& metadata ) {
         m_metadata = metadata;
      }
      /// Set whether the GRL info should be checked when merging/comparing objects
      inline void SetCheckGRLInfo( Bool_t check = kFALSE ) { m_checkGRLInfo = check; }

      /// Check whether the GRL info should be checked when merging/comparing objects
      inline const Bool_t& GetCheckGRLInfo() const { return m_checkGRLInfo; }
      /// Get the version of the object
      inline const TString& GetVersion() const { return m_version; }
      /// Get the meta-data associated to the GRL
      inline const std::map< TString, TString >& GetMetaData() const { return m_metadata; }
      /// Get the size of the meta-data container
      inline size_t GetMetaDataSize() const { return m_metadata.size(); }

      /// Print a summary about the GRL
      void Summary( Bool_t verbose = kFALSE ) const;
      /// Check if the GRL is empty
      Bool_t IsEmpty() const;

      /// Get a list of the good run numbers
      const std::vector< int > GetRunlist() const;
      /// Get a list of the good runs
      const std::vector< Root::TGoodRun > GetGoodRuns() const;
      /// Get a list of the selected triggers
      const std::vector< std::string > GetTriggerList() const;
      /// Get a list of the selected streams
      const std::vector< std::string > GetStreamList() const;

      /// Compose a suggested name for the object
      const TString GetSuggestedName() const;
      /// Compress each TGoodRun in the list
      void Compress();

   private:
      TString m_version; ///< Version of the GRL
      std::map< TString, TString > m_metadata; ///< Meta-data associated to the GRL
      Bool_t m_checkGRLInfo; ///< Flag telling whether GRL infos should be checked on compare/merge

      mutable Bool_t m_hasRun;
      mutable Bool_t m_hasLB; 
      mutable Int_t m_prevRun; 
      mutable Int_t m_prevLB;  

      ClassDef( TGoodRunsList, 1 );

   }; // class TGoodRunsList

} // namespace Root

#endif // SFRAME_GOODRUNSLISTS_TGoodRunsList_H

