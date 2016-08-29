// Dear emacs, this is -*- c++ -*-
// $Id: TGRLCollection.h 45093 2010-08-20 11:58:27Z krasznaa $
#ifndef SFRAME_GOODRUNSLISTS_TGRLCollection_H
#define SFRAME_GOODRUNSLISTS_TGRLCollection_H

// STL include(s):
#include <vector>

// ROOT include(s):
#include "TObject.h"

// Local include(s):
#include "TGoodRunsList.h"

namespace Root {

   /**
    * @short Types of operations on GRLs
    *
    *        The GRLs can be merged in two different ways: Requiring an AND between
    *        them, or requiring an OR between them. These two different requirements
    *        are described by this simple enumeration.
    *
    * @author Max Baak <mbaak@cern.ch> - CERN, Switzerland
    *
    * $Revision: 45093 $
    * $Date: 2010-08-20 13:58:27 +0200 (Fri, 20 Aug 2010) $
    */
   enum BoolOperation { OR, AND };

   /**
    *  @short A collection of good run lists
    *
    *         This class is used internally by TGoodRunsListReader to merge the information
    *         from multiple GRL XML files.
    *
    * @author Max Baak <mbaak@cern.ch> - CERN, Switzerland
    * @author Attila Krasznahorkay <Attila.Krasznahorkay@cern.ch>
    *
    * $Revision: 45093 $
    * $Date: 2010-08-20 13:58:27 +0200 (Fri, 20 Aug 2010) $
    */
   class TGRLCollection : public std::vector< TGoodRunsList >, public TObject {
      
   public:
      /// Constructor specifying if the GRL infos should be checked
      TGRLCollection( Bool_t checkGRLInfo = kFALSE );

      /// Copy constructor
      TGRLCollection( const Root::TGRLCollection& other );
      /// Assignment operator
      TGRLCollection& operator=( const TGRLCollection& other );

      /// Set the version of the GRL collection
      void SetVersion( const TString& version );
      /// Set the meta-data associated to the GRL collection
      void SetMetaData( const std::map< TString, TString >& metadata );
      /// Set whether to check the info associated to the GRLs
      inline void SetCheckGRLInfo( Bool_t check = kTRUE ) { m_checkGRLInfo = check; }

      /// Check if a run is part of the GRL collection
      Bool_t HasRun( const Int_t& runnr )  const;
      /// Check if a given luminosity block is part of the GRL collection
      Bool_t HasRunLumiBlock( const Int_t& runnr, const Int_t& lumiblocknr ) const;
      /// Check if the GRL collection is empty
      Bool_t IsEmpty() const;
      /// Check if a GRL with a given name is part of this collection
      Bool_t HasGoodRunsList( const TString& name ) const;

      /// Get a merged version of the GRL collection
      const TGoodRunsList
      GetMergedGoodRunsList( const Root::BoolOperation& operation = OR ) const;
      /// Get the GRL with a given index
      const TGoodRunsList GetGoodRunsList( size_t idx ) const;
      /// Find the GRL with a given name
      std::vector< TGoodRunsList >::iterator find( const TString& name );
      /// Find the GRL with a given name
      std::vector< TGoodRunsList >::const_iterator find( const TString& name ) const;
      
      const Root::TGRLCollection
      GetMergedGRLCollection( const Root::BoolOperation& operation = OR ) const;
      const Root::TGRLCollection GetOverlapWith( const TGoodRunsList& other ) const;

      /// Reset (clear) the object
      void Reset();
      /// Print a summary about the object
      void Summary( Bool_t verbose = kFALSE ) const;
      
   private:
      Bool_t m_checkGRLInfo; ///< Check the GRL info during operations

      ClassDef( TGRLCollection, 1 );

   }; // class TGRLCollection

} // namespace Root

#endif // SFRAME_GOODRUNSLISTS_TGRLCollection_H
