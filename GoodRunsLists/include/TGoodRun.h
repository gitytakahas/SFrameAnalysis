// Dear emacs, this is -*- c++ -*-
// $Id: TGoodRun.h 45093 2010-08-20 11:58:27Z krasznaa $
#ifndef SFRAME_GOODRUNSLISTS_TGoodRun_H
#define SFRAME_GOODRUNSLISTS_TGoodRun_H

// STL include(s):
#include <vector>

// ROOT include(s):
#include "TObject.h"

// Local include(s):
#include "TLumiBlockRange.h"

namespace Root {

   /**
    *  @short Class describing a "good run"
    *
    *         This class describes the luminosity block ranges within a run which
    *         should be used in the analysis.
    *
    * @author Max Baak <mbaak@cern.ch> - CERN, Switzerland
    * @author Attila Krasznahorkay <Attila.Krasznahorkay@cern.ch>
    *
    * $Revision: 45093 $
    * $Date: 2010-08-20 13:58:27 +0200 (Fri, 20 Aug 2010) $
    */
   class TGoodRun : public std::vector< TLumiBlockRange >, public TObject {
      
   public:
      /// Default constructor
      TGoodRun();
      /// Constructor specifying the run number
      TGoodRun( const Int_t& runnr );      

      /// Copy constructor
      TGoodRun( const Root::TGoodRun& other );
      /// Assignment operator
      TGoodRun& operator=( const TGoodRun& other );

      /// Get the overlap between two good run objects
      const Root::TGoodRun GetOverlapWith( const TGoodRun& other ) const;
      /// Get the union of two good run objects
      const Root::TGoodRun GetSumWith( const TGoodRun& other ) const;
      /// Get the lumiblock range in other that's not in this object
      const Root::TGoodRun GetPartOnlyIn( const TGoodRun& other ) const;
      /// Get the lumiblock range in this object that's not in other
      const Root::TGoodRun GetPartNotIn( const TGoodRun& other ) const;

      /// Test whether the range is empty
      Bool_t IsEmpty() const;
      /// Test whether a given luminosity block is part of the selection
      Bool_t HasLB( const Int_t& lumiblocknr ) const;
      /// Find the luminosity block range that holds a given luminosity block
      std::vector< Root::TLumiBlockRange >::iterator Find( const Int_t& lumiblocknr );
      /// Find the luminosity block range that holds a given luminosity block
      std::vector< Root::TLumiBlockRange >::const_iterator
      Find( const Int_t& lumiblocknr ) const;

      /// Get the run number
      inline Int_t GetRunNumber() const { return m_runnr; }
      /// Set the run number
      inline void SetRunNumber( const Int_t& runnr ) { m_runnr = runnr; } 

      /// Print a summary about the object
      void Summary() const ;

      /// Sort the luminosity block ranges in ascending order
      void Sort();
      /// Merge overlapping luminosity block ranges
      void Compress();
      /// Add a luminosity block to the run
      void AddLB( const Int_t& lumiblocknr );
      
   private:
      Int_t m_runnr; ///< Run number

      /// Sorter function for lumiblock ranges
      struct SorterL2H {
         bool operator() ( const TLumiBlockRange& p1, const TLumiBlockRange& p2 ) {
            return ( p1.Begin() < p2.Begin() );
         }
      }; // struct SorterL2H

      ClassDef( TGoodRun, 1 );

   }; // class TGoodRun

} // namespace Root

#endif // SFRAME_GOODRUNSLISTS_TGoodRun_H
