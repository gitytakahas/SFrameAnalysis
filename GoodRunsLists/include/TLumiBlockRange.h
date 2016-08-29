// Dear emacs, this is -*- c++ -*-
// $Id: TLumiBlockRange.h 45093 2010-08-20 11:58:27Z krasznaa $
#ifndef SFRAME_GOODRUNSLISTS_TLumiBlockRange_H
#define SFRAME_GOODRUNSLISTS_TLumiBlockRange_H

// STL include(s):
#include <vector>

// ROOT include(s):
#include "TObject.h"

namespace Root {

   /**
    *  @short Class describing a continous luminosity block range
    *
    *         The class is basically a container for two integer numbers: The beginning
    *         and the end of the luminosity block. It also has some convenience functions.
    *
    * @author Max Baak <mbaak@cern.ch> - CERN, Switzerland
    * @author Attila Krasznahorkay <Attila.Krasznahorkay@cern.ch>
    *
    * $Revision: 45093 $
    * $Date: 2010-08-20 13:58:27 +0200 (Fri, 20 Aug 2010) $
    */
   class TLumiBlockRange : public TObject {

   public:
      /// Default constructor
      TLumiBlockRange();
      /// Constructor specifying the start and end of the lumiblock range
      TLumiBlockRange( const Int_t& start, const Int_t& end = 2147483647 );

      /// Copy constructor
      TLumiBlockRange( const Root::TLumiBlockRange& other );
      /// Assignment operator
      TLumiBlockRange& operator=( const TLumiBlockRange& other );

      /// Get the lumiblock range that is in both objects
      const Root::TLumiBlockRange GetOverlapWith( const TLumiBlockRange& other ) const;
      /// Get the lumiblock range that is in the other one and not in this one
      const std::vector< Root::TLumiBlockRange >
      GetPartOnlyIn( const TLumiBlockRange& other ) const;
      /// Get the lumiblock range that is in this one and not in the other one
      const std::vector< Root::TLumiBlockRange >
      GetPartNotIn( const TLumiBlockRange& other ) const;

      /// Check if a luminosity block is inside this range
      Bool_t Contains( const Int_t& number ) const;

      /// The beginning of the luminosity block range
      inline Int_t Begin() const { return m_begin; }
      /// The end of the luminosity block range
      inline Int_t End() const { return m_end; }
      /// Check if the range is empty
      inline Bool_t IsEmpty() const { return Begin() > End(); }

      /// Set the beginning of the luminosity block range
      inline void SetBegin( const Int_t& begin ) { m_begin = begin; }
      /// Set the end of the luminosity block range
      inline void SetEnd( const Int_t& end ) { m_end = end; }

      /// Print a summary of the luminosity block range
      void Summary() const;
      
   private:
      Int_t m_begin; ///< The first luminosity block in this range
      Int_t m_end; ///< The last luminosity block in this range

      ClassDef( TLumiBlockRange, 1 );

   }; // class TLumiBlockRange

} // namespace Root

#endif // SFRAME_GOODRUNSLISTS_TLumiBlockRange_H
