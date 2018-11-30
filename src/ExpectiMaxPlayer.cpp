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

int Board::getTileSum() {
   int score = 0;
   for (BoardVec::iterator rowVecIt = boardVec->begin();
        rowVecIt != boardVec->end(); rowVecIt++) {
      RowVec* rowVec = *rowVecIt;
      for (RowVec::iterator valIt = rowVec->begin(); valIt != rowVec->end();
           valIt++) {
         int val = *valIt;
         score += val;
      }
   }
   return score;
}

int Board::getMaxTile() {
   int maxTile = 0;
   for (BoardVec::iterator rowVecIt = boardVec->begin();
        rowVecIt != boardVec->end(); rowVecIt++) {
      RowVec* rowVec = *rowVecIt;
      for (RowVec::iterator valIt = rowVec->begin(); valIt != rowVec->end();
           valIt++) {
         int val = *valIt;
         maxTile = val > maxTile ? val : maxTile;
      }
   }
   return maxTile;
}

int Board::makeMove(Move move) {
   bool boardChanged = false;
   int moveScore = 0;

   int rowIdx = 0;
   int colIdx = 0;
   switch (move) {
   case UP:
      rowIdx = 0;
      colIdx = 0;
      break;
   case DOWN:
      rowIdx = size - 1;
      colIdx = 0;
      break;
   case LEFT:
      rowIdx = 0;
      colIdx = 0;
      break;
   case RIGHT:
      rowIdx = 0;
      colIdx = size - 1;
      break;
   }
   for (int i = 0; i < size; i++) {
      int rowBackIdx = rowIdx;
      int colBackIdx = colIdx;
      int setCount = 0;
      int prevVal = -1;
      int rowPrevIdx = -1;
      int colPrevIdx = -1;

      for (int j = 0; j < size; j++) {
         int val = boardVec->at(rowIdx)->at(colIdx);
         if (val > 0) {
            if (val == prevVal) {
               int newVal = 2 * val;
               boardVec->at(rowPrevIdx)->at(colPrevIdx) = newVal;
               moveScore += newVal;
               prevVal = -1;
               boardChanged = true;
            } else {
               boardVec->at(rowBackIdx)->at(colBackIdx) = val;
               setCount++;
               if (rowBackIdx != rowIdx || colBackIdx != colIdx)
                  boardChanged = true;
               prevVal = val;

               switch (move) {
               case UP:
                  rowBackIdx++;
                  break;
               case DOWN:
                  rowBackIdx--;
                  break;
               case LEFT:
                  colBackIdx++;
                  break;
               case RIGHT:
                  colBackIdx--;
                  break;
               }
            }
         }

         rowPrevIdx = rowIdx;
         colPrevIdx = colIdx;

         switch (move) {
         case UP:
            rowIdx++;
            break;
         case DOWN:
            rowIdx--;
            break;
         case LEFT:
            colIdx++;
            break;
         case RIGHT:
            colIdx--;
            break;
         }
      }

      for (; setCount < size; setCount++) {
         boardVec->at(rowBackIdx)->at(colBackIdx) = 0;
         switch (move) {
         case UP:
            rowBackIdx++;
            break;
         case DOWN:
            rowBackIdx--;
            break;
         case LEFT:
            colBackIdx++;
            break;
         case RIGHT:
            colBackIdx--;
            break;
         }
      }

      switch (move) {
      case UP:
         rowIdx = 0;
         colIdx++;
         break;
      case DOWN:
         rowIdx = size - 1;
         colIdx++;
         break;
      case LEFT:
         rowIdx++;
         colIdx = 0;
         break;
      case RIGHT:
         rowIdx++;
         colIdx = size - 1;
         break;
      }
   }

   /* return value:
    * -1 = board did not change
    *  0 = no tiles merged
    * >0 = tiles merged
    */
   return boardChanged ? moveScore : -1;
}

/* ExpectiMaxPlayer */

ExpectiMaxPlayer::ExpectiMaxPlayer(bool debugArg) {
   debug = debugArg;
}

int tryMove(Board* board, Move move) {
   Board* newBoard = new Board(*board);
   int moveScore = newBoard->makeMove(move);
   delete newBoard;
   return moveScore;
}

int ExpectiMaxPlayer::getMove(Board* board) {
   int maxMove = -1;
   int maxMoveScore = -1;
   int moveScore = -1;
   Move move = UP;

   // check UP
   move = UP;
   moveScore = tryMove(board, move);
   if (moveScore > maxMoveScore) {
      maxMove = move;
      maxMoveScore = moveScore;
   }

   // check DOWN
   move = DOWN;
   moveScore = tryMove(board, move);
   if (moveScore > maxMoveScore) {
      maxMove = move;
      maxMoveScore = moveScore;
   }

   // check LEFT
   move = LEFT;
   moveScore = tryMove(board, move);
   if (moveScore > maxMoveScore) {
      maxMove = move;
      maxMoveScore = moveScore;
   }

   // check RIGHT
   move = RIGHT;
   moveScore = tryMove(board, move);
   if (moveScore > maxMoveScore) {
      maxMove = move;
      maxMoveScore = moveScore;
   }

   if (debug) {
      board->print();
   }
   return maxMove;
}
