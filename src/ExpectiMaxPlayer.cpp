#include <vector>
#include "ExpectiMaxPlayer.h"

extern "C" {
   ExpectiMaxPlayer* ExpectiMaxPlayer_new(){
      return new ExpectiMaxPlayer();
   }

   int ExpectiMaxPlayer_getMove(ExpectiMaxPlayer* p){
      return p->getMove();
   }
}
