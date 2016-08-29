// $Id: StrUtil.cxx 45093 2010-08-20 11:58:27Z krasznaa $

// Local include(s):
#include "../include/StrUtil.h"

namespace GRLStrUtil {

   void trim( std::string& input ) {

      // trim leading and trailing whitespace
      std::string::size_type position = input.find_first_not_of( " \t\n" );
      if( position == std::string::npos ) return; // skip, it's all whitespace
      input.erase( 0, position );
      position = input.find_last_not_of( " \t\n" );
      if( position != std::string::npos )
         input.erase( position+1 );

      return;
  }

  void split( const std::string& input, std::string& first, std::string& second ) {

     // split input in two
     std::string::size_type position = input.find_first_of( " \t\n" );
     if( position == std::string::npos ) {
        first  = input;
        second = "";
     } else {
        first  = input.substr( 0, position );
        second = input.substr( position + 1, input.size() - position );
        // trim leading whitespace of second
        position = second.find_first_not_of( " \t\n" );
        second.erase( 0, position );
     }

     return;
  }

   std::vector< std::string > split( std::string input ) {

      trim( input );
      std::vector< std::string > splitVec;
      std::string first, second;
      do {
         split( input, first, second );
         if( ! first.empty() ) splitVec.push_back( first );
         input = second;
      } while( ! input.empty() );

      return splitVec;
   }

} // namespace GRLStrUtil
