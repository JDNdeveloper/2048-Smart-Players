#include "ExpectiMaxPlayer.h"

// ExpectiMaxPlayer interface
extern "C" {
   ExpectiMaxPlayer* ExpectiMaxPlayer_new(bool debug) {
      return new ExpectiMaxPlayer(debug);
   }

   int ExpectiMaxPlayer_getMove(ExpectiMaxPlayer* p, Board* board) {
      return p->getMove(board);
   }

   void ExpectiMaxPlayer_delete(ExpectiMaxPlayer* p) {
      delete p;
   }
}

// Board interface
extern "C" {
   Board* Board_new(int size) {
      Board* board = new Board;
      for (int i = 0; i < size; i++) {
         Row* row = new Row;
         for (int j = 0; j < size; j++) {
            row->push_back(0);
         }
         board->push_back(row);
      }
      return board;
   }

   void Board_setPos(Board* b, int row, int col, int val) {
      if (row < 0 || row >= b->size() || col < 0 || col >= b->at(row)->size())
         return;

      b->at(row)->at(col) = val;
   }

   void Board_delete(Board* b) {
      while(!b->empty()) {
         delete b->back();
         b->pop_back();
      }
      delete b;
   }
}
