#include "ExpectiMaxPlayer.h"

/* ExpectiMaxPlayer interface */

extern "C" {
   ExpectiMaxPlayer* ExpectiMaxPlayer_new(bool debug) {
      return new ExpectiMaxPlayer(debug);
   }

   void ExpectiMaxPlayer_delete(ExpectiMaxPlayer* player) {
      delete player;
   }

   int ExpectiMaxPlayer_getMove(ExpectiMaxPlayer* player, Board* board) {
      return player->getMove(board);
   }
}

/* Board interface */

extern "C" {
   Board* Board_new(int size) {
      return new Board(size);
   }

   void Board_delete(Board* board) {
      delete board;
   }

   void Board_setPos(Board* board, int row, int col, int val) {
      board->setPos(row, col, val);
   }
}

/* Board */

Board::Board(int sizeArg) {
   // set the board size
   size = sizeArg;

   // setup the board
   boardVec = new BoardVec;
   for (int i = 0; i < size; i++) {
      RowVec* rowVec = new RowVec;
      for (int j = 0; j < size; j++) {
         rowVec->push_back(0);
      }
      boardVec->push_back(rowVec);
   }
}

Board::Board(const Board& oldBoard) {
   // set the board size
   size = oldBoard.size;

   // copy the board contents
   boardVec = new BoardVec;
   BoardVec* oldBoardVec = oldBoard.boardVec;
   for (BoardVec::iterator rowVecIt = oldBoardVec->begin();
        rowVecIt != oldBoardVec->end(); rowVecIt++) {
      RowVec* oldRowVec = *rowVecIt;
      RowVec* rowVec = new RowVec;
      for (RowVec::iterator valIt = oldRowVec->begin(); valIt != oldRowVec->end();
           valIt++) {
         rowVec->push_back(*valIt);
      }
      boardVec->push_back(rowVec);
   }
}

Board::~Board() {
   while(!boardVec->empty()) {
      delete boardVec->back();
      boardVec->pop_back();
   }
   delete boardVec;
}

void Board::print() {
   for (BoardVec::iterator rowVecIt = boardVec->begin();
        rowVecIt != boardVec->end(); rowVecIt++) {
      RowVec* rowVec = *rowVecIt;
      for (RowVec::iterator valIt = rowVec->begin(); valIt != rowVec->end();
           valIt++) {
         int val = *valIt;
         std::cout << val << " ";
      }
      std::cout << std::endl;
   }
   std::cout << std::endl;
}

void Board::setPos(int row, int col, int val) {
   if (row < 0 || row >= size || col < 0 || col >= size)
      return;

   boardVec->at(row)->at(col) = val;
}

void Board::makeMove(Move move) {
   // TODO
}

/* ExpectiMaxPlayer */

ExpectiMaxPlayer::ExpectiMaxPlayer(bool debugArg) {
   debug = debugArg;
}

int ExpectiMaxPlayer::getMove(Board* board) {
   if (debug) {
      board->print();
   }
   return UP;
}
