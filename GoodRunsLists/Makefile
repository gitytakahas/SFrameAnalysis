# Package information
LIBRARY = GoodRunsLists
OBJDIR  = obj
DEPDIR  = $(OBJDIR)/dep
SRCDIR  = src
INCDIR  = include

# Overwrite the default rule defined in Makefile.common
grldefault: default $(SFRAME_BIN_PATH)/pq2LumiGRLCreator $(SFRAME_BIN_PATH)/fileLumiGRLCreator

# Disable the following line if you don't have libxml2-devel
# installed locally and/or don't need XML writing capabilities.
INCLUDES += -I/usr/include/libxml2 -D__WITHLIBXML__

# Include the generic compilation rules
include $(SFRAME_DIR)/Makefile.common

$(SFRAME_BIN_PATH)/pq2LumiGRLCreator: pq2LumiGRLCreator.o anyoption.o $(SHLIBFILE)
	@echo "Linking $@"
	@$(LD) $(LDFLAGS) -O2 $(OBJDIR)/pq2LumiGRLCreator.o $(OBJDIR)/anyoption.o \
		-L$(SFRAME_LIB_PATH) -lSFrameCore -lGoodRunsLists \
		$(ROOTLIBS) -lTreePlayer -lXMLParser -lPyROOT -lProof -lProofPlayer -lutil -o $@

$(SFRAME_BIN_PATH)/fileLumiGRLCreator: fileLumiGRLCreator.o anyoption.o $(SHLIBFILE)
	@echo "Linking $@"
	@$(LD) $(LDFLAGS) -O2 $(OBJDIR)/fileLumiGRLCreator.o $(OBJDIR)/anyoption.o \
		-L$(SFRAME_LIB_PATH) -lSFrameCore -lGoodRunsLists \
		$(ROOTLIBS) -lTreePlayer -lXMLParser -lPyROOT -lProof -lProofPlayer -lutil -o $@

pq2LumiGRLCreator.o: app/pq2LumiGRLCreator.cxx app/anyoption.h
	@echo "Compiling $<"
	@mkdir -p $(OBJDIR)
	@$(CXX) $(CXXFLAGS) -O2 -c $< -o $(OBJDIR)/$(notdir $@) $(INCLUDES)

fileLumiGRLCreator.o: app/fileLumiGRLCreator.cxx app/anyoption.h
	@echo "Compiling $<"
	@mkdir -p $(OBJDIR)
	@$(CXX) $(CXXFLAGS) -O2 -c $< -o $(OBJDIR)/$(notdir $@) $(INCLUDES)

anyoption.o: app/anyoption.cxx app/anyoption.h
	@echo "Compiling $<"
	@mkdir -p $(OBJDIR)
	@$(CXX) $(CXXFLAGS) -O2 -c $< -o $(OBJDIR)/$(notdir $@) $(INCLUDES)
