// $Id: fileLumiGRLCreator.cxx 183599 2011-07-11 11:40:30Z krasznaa $

// ROOT include(s):
#include "TString.h"
#include "TObjString.h"
#include "TFile.h"

// SFrame include(s):
#include "core/include/SLogger.h"

// The option parser code:
#include "anyoption.h"

// Local include(s):
#include "../include/TGoodRunsList.h"
#include "../include/TGoodRunsListReader.h"
#include "../include/TGoodRunsListWriter.h"

/// A global logger object
static SLogger m_logger( "fileLumiGRLCreator" );

/// The luminosity directory name in the D3PDs
static const char* LUMI_DIR_NAME = "Lumi";

namespace {

   /// Helper function for printing vectors
   /**
    * The tool needs to print the contents of a few vectors. This function
    * takes care about doing that conveniently.
    *
    * @param out The SLogger object to write the contents to
    * @param vec The vector that should be printed
    * @returns The SLogger object that was given to the functions
    */
   template< typename T >
   SLogger& operator<< ( SLogger& out, const std::vector< T >& vec ) {
      out << "[";
      typename std::vector< T >::const_iterator itr = vec.begin();
      typename std::vector< T >::const_iterator end = vec.end();
      for( ; itr != end; ++itr ) {
         out << *itr;
         if( ++itr != end ) {
            out << ", ";
         }
         --itr;
      }
      out << "]";
      return out;
   }

} // private namespace

/// Read the XML strings from each file and add it to the GRL reader
static void ReadLumiInfo( Root::TGoodRunsListReader& grlReader,
                          const std::vector< TString >& fileNames );

int main( int argc, char* argv[] ) {

   // Create the command line parser:
   AnyOption opt;

   // Set the usage/help messages:
   opt.addUsage( "Application for creating a lumiblock list in the format of" );
   opt.addUsage( "a GRL file from a list of D3PD files plus an actual GRL file." ); 
   opt.addUsage( "" );
   opt.addUsage( "Usage:" );
   opt.addUsage( "  fileLumiGRLCreator [options] file1 file2 ..." );
   opt.addUsage( "" );
   opt.addUsage( "Options:" );
   opt.addUsage( "  -h  --help         Prints this help" );
   opt.addUsage( "  -g  --grl          GRL to use" );
   opt.addUsage( "  -o  --output       Output file (XML or ROOT)" );

   // Set the options:
   opt.setFlag( "help", 'h' );
   opt.setOption( "dataset", 'd' );
   opt.setOption( "grl",     'g' );
   opt.setOption( "output",  'o' );
   opt.setOption( "server",  's' );

   // Process the command line arguments:
   opt.processCommandArgs( argc, argv );
   if( ! opt.hasOptions() ) {
      opt.printUsage();
      return 1;
   }

   // Check if the user just asked for the help:
   if( opt.getFlag( "help" ) || opt.getFlag( 'h' ) ) {
      opt.printUsage();
      return 0;
   }

   // Check if a GRL was defined:
   if( ! opt.getValue( 'g' ) ) {
      m_logger << WARNING << "You should define a GRL as well. Creating info just based"
               << SLogger::endmsg;
      m_logger << WARNING << "on the D3PD files for now..." << SLogger::endmsg;
   }
   TString grlName( opt.getValue( 'g' ) ? opt.getValue( 'g' ) : "" );

   // Check if an output file was specified:
   if( ! opt.getValue( 'o' ) ) {
      m_logger << INFO << "No output file specified. Using 'grl_output.xml'"
               << SLogger::endmsg;
   }
   TString outputName( opt.getValue( 'o' ) ? opt.getValue( 'o' ) : "grl_output.xml" );
   if( ( ! outputName.EndsWith( ".xml" ) ) &&
       ( ! outputName.EndsWith( ".root" ) ) ) {
      REPORT_ERROR( "Output file name's format not recognised. Should end either in '.root' or '.xml'" );
      return 1;
   }

   // Collect the file names:
   std::vector< TString > fileNames;
   for( int i = 0 ; i < opt.getArgc() ; ++i ) {
      fileNames.push_back( opt.getArgv( i ) );
   }
   if( ! fileNames.size() ) {
      REPORT_ERROR( "You should specify at least one D3PD file name!" );
      return 1;
   }

   // Tell the user what we're about to do:
   m_logger << INFO << "Creating lumiblock list using:" << SLogger::endmsg;
   m_logger << INFO << "  File names  = " << fileNames << SLogger::endmsg;
   m_logger << INFO << "  GRL file    = " << ( grlName == "" ? "NOT DEFINED" : grlName )
            << SLogger::endmsg;
   m_logger << INFO << "  Output file = " << outputName << SLogger::endmsg;

   // Read in the merged lumiblock info from the dataset:
   Root::TGoodRunsListReader lbReader;
   ReadLumiInfo( lbReader, fileNames );
   if( ! lbReader.Interpret() ) {
      REPORT_ERROR( "Couldn't interpret the collected lumiblock information" );
      return 1;
   }
   Root::TGoodRunsList d3pdGRL = lbReader.GetMergedGoodRunsList();

   // Get its overlap with a GRL if one was specified:
   if( grlName != "" ) {
      // Read in the GRL file:
      Root::TGoodRunsListReader grlReader( grlName );
      if( ! grlReader.Interpret() ) {
         REPORT_ERROR( "Couldn't interpret the GRL: " << grlName );
         return 1;
      }
      // Take its overlap with the D3PD lumiblock list:
      Root::TGoodRunsList xmlGRL = grlReader.GetMergedGoodRunsList();
      d3pdGRL = d3pdGRL.GetOverlapWith( xmlGRL );
   }

   // Print the info about the collected lumiblocks:
   d3pdGRL.Summary();

   // Set some additional things on the GRL:
   d3pdGRL.SetVersion( "20" );
   d3pdGRL.AddMetaData( "Description", "Lumiblock list created from D3PD files"
                        " plus GRL '" + grlName + "'" );

   // Turn the GRL into an XML string:
   Root::TGoodRunsListWriter writer;
   writer.SetGoodRunsList( d3pdGRL );

   if( outputName.EndsWith( ".xml" ) ) {
      m_logger << INFO << "Writing out: " << outputName << SLogger::endmsg;
      // Write out the XML file:
      writer.SetFilename( outputName );
      if( ! writer.WriteXMLFile() ) {
         REPORT_ERROR( "Failed to write out: " << outputName );
         return 1;
      }
   } else if( outputName.EndsWith( ".root" ) ) {
      // Write out this merged/overlapped GRL:
      TFile* ofile = TFile::Open( outputName, "RECREATE" );

      // Create the Lumi directory in it:
      TDirectory* lumidir = ofile->mkdir( LUMI_DIR_NAME, LUMI_DIR_NAME );
      lumidir->cd();

      // The object that will be written out:
      TObjString ostring( writer.GetXMLString() );

      // Write out this object string:
      lumidir->WriteObjectAny( &ostring, "TObjString", "physics", "overwrite" );

      // Close and delete the output file:
      ofile->Write();
      ofile->Close();
      delete ofile;
   }

   return 0;
}

void ReadLumiInfo( Root::TGoodRunsListReader& grlReader,
                   const std::vector< TString >& fileNames ) {

   std::vector< TString >::const_iterator file_itr = fileNames.begin();
   std::vector< TString >::const_iterator file_end = fileNames.end();
   for( ; file_itr != file_end; ++file_itr ) {

      // Open the file:
      TFile* file = TFile::Open( *file_itr, "READ" );

      // Access the Lumi directory in the file:
      TDirectoryFile* dir =
         dynamic_cast< TDirectoryFile* >( file->GetDirectory( LUMI_DIR_NAME ) );
      if( ! dir ) {
         REPORT_ERROR( "Lumi information not found in file: " << *file_itr );
         file->Close();
         delete file;
         continue;
      }

      // Get a list of all objects in this file:
      TList* keyList = dir->GetListOfKeys();

      // Loop over all these objects:
      for( Int_t j = 0; j < keyList->GetEntries(); ++j ) {

         TObjString* ostring =
            dynamic_cast< TObjString* >( dir->Get( keyList->At( j )->GetName() ) );
         if( ! ostring ) continue;

         // Check that it has the right format:
         if( ostring->GetString().BeginsWith( "<?xml version=\"1.0\"?" ) &&
             ostring->GetString().Contains( "DOCTYPE LumiRangeCollection" ) ) {

            // If it is, let's add it to the reader:
            grlReader.AddXMLString( ostring->GetString() );
         } else {
            m_logger << WARNING << "Lumi string not in the expected format: "
                     << ostring->GetString() << SLogger::endmsg;
         }

      }

      // Close and delete the file:
      file->Close();
      delete file;
   }

   return;
}
