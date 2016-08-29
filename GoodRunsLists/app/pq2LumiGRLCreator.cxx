// $Id: pq2LumiGRLCreator.cxx 183599 2011-07-11 11:40:30Z krasznaa $

// ROOT include(s):
#include "TString.h"
#include "TProof.h"
#include "TFileCollection.h"
#include "TFileInfo.h"
#include "THashList.h"
#include "TFile.h"
#include "TDirectoryFile.h"

// SFrame include(s):
#include "core/include/SLogger.h"
#include "core/include/SError.h"
#include "core/include/SProofManager.h"

// The option parser code:
#include "anyoption.h"

// Local include(s):
#include "../include/TGoodRunsList.h"
#include "../include/TGoodRunsListReader.h"
#include "../include/TGoodRunsListWriter.h"

/// A global logger object
static SLogger m_logger( "pq2LumiGRLCreator" );

/// The luminosity directory name in the D3PDs
static const char* LUMI_DIR_NAME = "Lumi";

/// Read the XML strings from each file and add it to the GRL reader
static void ReadLumiInfo( Root::TGoodRunsListReader& grlReader, const TString& server,
                          const TString& dataset ) throw( SError );

/**
 *  @short Application for creating lumiblock lists off of PQ2 datasets
 *
 *         This application can be used to collect information about PROOF (PQ2)
 *         datasets. The PQ2 dataset is expected to contain only D3PD files that
 *         have luminosity metadata in them.
 *
 *         The application opens each file in a given dataset, collects the
 *         lumiblock information from each of them, possibly ANDs it with
 *         a GRL, and writes out the results into a ROOT or XML file.
 *
 *         The resulting file can then be used to calculate the exact luminosity
 *         for processing the PQ2 dataset using the GRL file that was used
 *         with this application.
 *
 * @author Attila Krasznahorkay <Attila.Krasznahorkay@cern.ch>
 *
 * $Revision: 183599 $
 * $Date: 2011-07-11 13:40:30 +0200 (Mon, 11 Jul 2011) $
 */
int main( int argc, char* argv[] ) {

   // Create the command line parser:
   AnyOption opt;

   // Set the usage/help messages:
   opt.addUsage( "Application for creating a lumiblock list in the format of" );
   opt.addUsage( "a GRL file from a PQ2 dataset plus an actual GRL file." ); 
   opt.addUsage( "" );
   opt.addUsage( "Usage:" );
   opt.addUsage( "" );
   opt.addUsage( "  -h  --help         Prints this help" );
   opt.addUsage( "  -d  --dataset      PQ2 dataset to use" );
   opt.addUsage( "  -g  --grl          GRL to use" );
   opt.addUsage( "  -o  --output       Output file (XML or ROOT)" );
   opt.addUsage( "  -s  --server       PROOF server name" );

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

   // Check if a dataset was defined:
   if( ! opt.getValue( 'd' ) ) {
      REPORT_FATAL( "You have to define a PQ2 dataset name" );
      opt.printUsage();
      return 1;
   }
   TString dsetName( opt.getValue( 'd' ) );

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

   // Remove the extension from the file name:
   if( ( ! outputName.EndsWith( ".xml" ) ) &&
       ( ! outputName.EndsWith( ".root" ) ) ) {
      REPORT_ERROR( "Output file name's format not recognised. Should end either in '.root' or '.xml'" );
      return 1;
   }

   // Check if a PROOF server was specified:
   if( ! opt.getValue( 's' ) ) {
      REPORT_FATAL( "You have to specify a PROOF server name!" );
      return 1;
   }
   TString serverName( opt.getValue( 's' ) );

   // Tell the user what we're about to do:
   m_logger << INFO << "Creating lumiblock list using:" << SLogger::endmsg;
   m_logger << INFO << "  PQ2 dataset = " << dsetName << SLogger::endmsg;
   m_logger << INFO << "  GRL file    = " << ( grlName == "" ? "NOT DEFINED" : grlName )
            << SLogger::endmsg;
   m_logger << INFO << "  Output file = " << outputName << SLogger::endmsg;

   // Read in the merged lumiblock info from the dataset:
   Root::TGoodRunsListReader lbReader;
   ReadLumiInfo( lbReader, serverName, dsetName );
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
   d3pdGRL.AddMetaData( "Description", "Lumiblock list created from dataset '" +
                        dsetName + "' plus GRL '" + grlName + "'" );

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

   // Close the PROOF connection(s):
   SProofManager::Instance()->Cleanup();

   return 0;
}

/**
 * This function is used to extract the XML strings out of all the files that are in
 * a PQ2 dataset.
 *
 * @param grlReader The GRL reader to which the XML strings should be defined
 * @param server The name of the PROOF server
 * @param dataset The name of the dataset on the PROOF server
 */
void ReadLumiInfo( Root::TGoodRunsListReader& grlReader, const TString& server,
                   const TString& dataset ) throw( SError ) {

   // Connect to the PROOF server:
   TProof* pserver = SProofManager::Instance()->Open( server, "masteronly" );
   if( ! pserver ) {
      REPORT_FATAL( "Couldn't connect to PROOF server: " << server );
      throw SError( "Couldn't connect to PROOF server",
                    SError::StopExecution );
   }

   // Check if the dataset even exists:
   if( ! pserver->ExistsDataSet( dataset ) ) {
      REPORT_ERROR( "The dataset (" << dataset << ") doesn't exist" );
      return;
   }

   // Access the dataset:
   TFileCollection* dset = pserver->GetDataSet( dataset );
   // Get the file list out of it:
   THashList* flist = dset->GetList();

   // Give some info:
   m_logger << INFO << "Extracting lumiblock information out of "
            << flist->GetEntries() << " files" << SLogger::endmsg;

   // List the file names:
   for( Int_t i = 0; i < flist->GetEntries(); ++i ) {
      TFileInfo* finfo = dynamic_cast< TFileInfo* >( flist->At( i ) );
      if( ! finfo ) {
         REPORT_FATAL( "The dataset doesn't have the expected format" );
         throw SError( "The dataset doesn't have the expected format",
                       SError::StopExecution );
      }
      TUrl* url = finfo->GetCurrentUrl();
      m_logger << DEBUG << "Processing file: " << url->GetUrl() << SLogger::endmsg;

      // Open the file:
      TFile* file = TFile::Open( url->GetUrl(), "READ" );

      // Access the Lumi directory in the file:
      TDirectoryFile* dir =
         dynamic_cast< TDirectoryFile* >( file->GetDirectory( LUMI_DIR_NAME ) );
      if( ! dir ) {
         REPORT_ERROR( "Lumi information not found in file: " << url->GetUrl() );
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
