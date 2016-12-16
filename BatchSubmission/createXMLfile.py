#!/usr/bin/env python
# -*- coding: utf-8 -*-
#***************************************************************************
#* @Project: creating XML files for SFrame
#* @author Clemens Lange    <clange@physik.uzh.ch>        - UZH
#*
#***************************************************************************
#

import os
import sys
import re
import optparse
import thread
import subprocess
import math

dCacheInstances={}
#Xrootd and dcap prefixes
dCacheInstances["PSI"]=["root://t3dcachedb.psi.ch:1094/", "dcap://t3se01.psi.ch:22125/"]

def main():
  # parse the command line
  parser=optparse.OptionParser(usage="%prog sampleListFile")
  parser.add_option("-s", "--site", action="store",
                    dest="site", default="PSI",
                    help="grid site [default = %default]")
  parser.add_option("-v", "--verbose", action="store_true",
                    dest="verbose", default=False,
                    help="verbose output [default = %default]")
  parser.add_option("-x", "--xrootd", action="store_true",
                    dest="useXrootd", default=False,
                    help="use Xrootd [default = %default]")
  parser.add_option("-t", "--tree", action="store",
                    dest="treeName", default="ntuplizer/tree",
                    help="Tree to be scanned by SFrame for number of input events [default = %default]")
  parser.add_option("-m", "--maxFiles", action="store",
                    dest="maxFiles", default="500",
                    help="Maximum number of files [default = %default]")
  parser.add_option("-o", "--outDir", action="store",
                    dest="outDir", default="xmls_Izaak",
                    help="Output directory for xml files [default = %default]")



  (options, args) = parser.parse_args()
  
  if len(args) != 1:
    parser.error("Please provide at file list name")

  sampleListName = args[0]
  site=options.site
  verbose=options.verbose
  useXrootd=options.useXrootd
  treeName=options.treeName
  maxFiles=int(options.maxFiles)
  outDir=options.outDir

  if not os.path.exists(outDir):
    print "Creating output directory", outDir
    os.makedirs(outDir)
  
  with open(sampleListName) as sampleList:
    for sample in sampleList:
      if sample.startswith("#") or sample.isspace():
        continue
      print "- "*10
      sample = sample.strip("\n")
      sampleName = (sample.strip("/")).rsplit("/",1)[1]
      sampleName_file=(sample.strip("/")).rsplit("/",3)[1]
      sampleName_file+="_"+sampleName
      print "Sample: %s in location: %s producing file with list %s" %(sampleName,sample,sampleName_file )
      fileList=[]
      if not os.path.isdir(sample):
        print sample,"is not a directory."
      else:
        prefix = ""
        if (sample.startswith("/pnfs")):
          if (site not in dCacheInstances):
            print "Gridsite doesn't have dCache instances defined."
            sys.exit(1)
          if (useXrootd):
            prefix = dCacheInstances[site][0]
          else:
            prefix = dCacheInstances[site][1]
        if verbose:
          print "Using prefix:",prefix
        for subdir, dirs, files in os.walk(sample):
          for file in files:
            if (file.find(".root") >= 0):
              if (verbose):
                print prefix + os.path.join(sample, subdir, file)
              fileList.append(prefix + os.path.join(sample, subdir, file))
      
        print "Processing %d files" %len(fileList)
        nFiles=int(math.ceil(len(fileList)/float(maxFiles)))
        if (nFiles > 1):
          maxFiles = int(math.ceil(len(fileList)/float(nFiles)))
          print "splitting file into %d subfiles of max. %d input files each" %(nFiles, maxFiles)
        if (len(fileList) == 0):
          print "No files found."
        for i in range(nFiles):
          if (nFiles > 1):
            outName = "%s_%d" %(sampleName_file, i)
          else:
            outName = sampleName_file
          csvList = ""
          for fileIndex in range(i*maxFiles,min((i+1)*maxFiles,len(fileList))):
            csvList = csvList+fileList[fileIndex]+","
          csvList = csvList.strip(",")
          lock=thread.allocate_lock()
          lock.acquire()
          commandMC="sframe_input.py -r -d -o %s/%s.xml %s -t %s" %(outDir, outName, csvList, treeName)
          if verbose:
            print commandMC
          processMC=subprocess.Popen(commandMC, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
          lock.release()
          output=processMC.stdout.read()
          if verbose:
            print output
          else:
            for line in output.split("\n"):
              if "events processed" in line:
                print line.strip("\n")
          outerr=processMC.stderr.read()
          print outerr


if __name__ == "__main__":
  main()
