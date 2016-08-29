// Dear emacs, this is -*- c++ -*-
// $Id: StrUtil.h 45093 2010-08-20 11:58:27Z krasznaa $
#ifndef SFRAME_GOODRUNSLISTS_StrUtil_H
#define SFRAME_GOODRUNSLISTS_StrUtil_H

// STL include(s):
#include <string>
#include <vector>

namespace GRLStrUtil {

   void trim( std::string& input );
   void split( const std::string& input, std::string& first, std::string& second );
   std::vector< std::string > split( std::string input );

} // namespace GRLStrUtil

#endif // SFRAME_GOODRUNSLISTS_StrUtil_H
