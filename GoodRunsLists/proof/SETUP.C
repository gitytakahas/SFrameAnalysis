int SETUP() {

   if( gSystem->Load( "libGoodRunsLists" ) == -1 ) return -1;

   return 0;
}
