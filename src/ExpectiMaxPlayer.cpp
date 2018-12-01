#include <cmath>
#include <sstream>
#include "ExpectiMaxPlayer.h"

/* ExpectiMaxPlayer interface */

extern "C" {
   ExpectiMaxPlayer* ExpectiMaxPlayer_new(bool debug, int depth,
                                          double probCutoff) {
      return new ExpectiMaxPlayer(debug, depth, probCutoff);
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

   void Board_setScore(Board* board, int score) {
      board->setScore(score);
   }
}

/* Board */

Board::Board(int sizeArg) {
   // set the board size
   size = sizeArg;
   length = size * size;

   // setup the board
   boardByteArray = (char*) malloc(length * sizeof(char));
   for (int i = 0; i < length; i++) {
      boardByteArray[i] = 0;
   }
}

Board::Board(const Board& oldBoard) {
   // set the board size and score
   size = oldBoard.size;
   length = size * size;
   score = oldBoard.score;

   // copy the board contents
   boardByteArray = (char*) malloc(length * sizeof(char));
   char* oldBoardByteArray = oldBoard.boardByteArray;
   for (int i = 0; i < length; i++) {
      boardByteArray[i] = oldBoardByteArray[i];
   }
}

Board::~Board() {
   free(boardByteArray);
}

inline void Board::setRawPos(int row, int col, char val) {
   boardByteArray[getIndex(row, col)] = val;
}

inline char Board::getRawPos(int row, int col) {
   return boardByteArray[getIndex(row, col)];
}

inline void Board::setPos(int row, int col, int val) {
   if (val == 0) {
      setRawPos(row, col, 0);
   } else {
      setRawPos(row, col, (char) std::log2(val));
   }
}

inline int Board::getPos(int row, int col) {
   int val = getRawPos(row, col);
   if (val == 0) {
      return 0;
   } else {
      return std::pow(2.0, float(val));
   }
}

std::string Board::getString() {
   std::ostringstream os;
   for (int i = 0; i < length; i++) {
      os << boardByteArray[i];
   }
   return os.str();
}

int Board::getTileSum() {
   int score = 0;
   for (int row = 0; row < size; row++) {
      for (int col = 0; col < size; col++) {
         score += getPos(row, col);
      }
   }
   return score;
}

int Board::getMaxTile() {
   int maxTile = 0;
   for (int row = 0; row < size; row++) {
      for (int col = 0; col < size; col++) {
         int val = getRawPos(row, col);
         maxTile = val > maxTile ? val : maxTile;
      }
   }
   return std::pow(2.0, maxTile);
}

int Board::getNumOpenSpaces() {
   int numOpenSpaces = 0;
   for (int row = 0; row < size; row++) {
      for (int col = 0; col < size; col++) {
         if (getRawPos(row, col) == 0) {
            numOpenSpaces++;
         }
      }
   }
   return numOpenSpaces;
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
         int val = getRawPos(rowIdx, colIdx);
         if (val > 0) {
            if (val == prevVal) {
               int newVal = val + 1;
               setRawPos(rowPrevIdx, colPrevIdx, newVal);
               moveScore += newVal;
               prevVal = -1;
               boardChanged = true;
            } else {
               setRawPos(rowBackIdx, colBackIdx, val);
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
         setRawPos(rowBackIdx, colBackIdx, 0);
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

   score += moveScore;

   /* return value:
    * -1 = board did not change
    *  0 = no tiles merged
    * >0 = tiles merged
    */
   return boardChanged ? moveScore : -1;
}

/* ExpectiMaxPlayer */

ExpectiMaxPlayer::ExpectiMaxPlayer(bool debugArg, int depthArg,
                                   double probCutoffArg)
   : debug(debugArg),
     depth(depthArg),
     probCutoff(probCutoffArg),
     stateCache() {
}

int tryMove(Board* board, Move move) {
   Board* newBoard = new Board(*board);
   int moveScore = newBoard->makeMove(move);
   delete newBoard;
   return moveScore;
}

float getHeuristicScore(Board* board) {
   int boardSize = board->getSize();
   int start = 0;
   int end = boardSize - 1;

   int score = board->getScore();
   int maxTile = board->getMaxTile();
   int openSpaces = board->getNumOpenSpaces();
   bool maxTileInCorner = (maxTile == board->getPos(start, start) ||
                           maxTile == board->getPos(start, end) ||
                           maxTile == board->getPos(end, start) ||
                           maxTile == board->getPos(end, end));

   // TODO figure out why this is worse than just using score...
   // return (100.0 * score +
   //         10.0 * maxTile +
   //         10.0 * openSpaces +
   //         10.0 * maxTileInCorner);
   return score;
}

Result ExpectiMaxPlayer::getMoveRecursive(Board* board, Player player,
                               int depth, double prob) {
   State state(board->getString(), player, depth);
   StateCache::iterator stateIt = stateCache.find(state);
   if (stateIt != stateCache.end()) {
      return Result(stateIt->second, NO_MOVE);
   }

   if (depth == 0 || prob < probCutoff) {
      int heuristicScore = getHeuristicScore(board);
      stateCache.insert({state, heuristicScore});
      return Result(heuristicScore, NO_MOVE);
   }

   switch (player) {
   case USER:
      {
         Board* newBoard;
         Move move;
         int moveScore;

         Move maxMove = NO_MOVE;
         // this serves as the penalty for reaching
         // game over
         float maxScore = -100;

         // move up
         move = UP;
         newBoard = new Board(*board);
         moveScore = newBoard->makeMove(move);
         if (moveScore != -1) {
            Result result = getMoveRecursive(newBoard, TILE_SPAWN,
                                             depth, prob / 4.0);
            float score = result.score;
            if (score >= maxScore) {
               maxScore = score;
               maxMove = move;
            }
         }
         delete newBoard;

         // move down
         move = DOWN;
         newBoard = new Board(*board);
         moveScore = newBoard->makeMove(move);
         if (moveScore != -1) {
            Result result = getMoveRecursive(newBoard, TILE_SPAWN,
                                             depth, prob / 4.0);
            float score = result.score;
            if (score >= maxScore) {
               maxScore = score;
               maxMove = move;
            }
         }
         delete newBoard;

         // move left
         move = LEFT;
         newBoard = new Board(*board);
         moveScore = newBoard->makeMove(move);
         if (moveScore != -1) {
            Result result = getMoveRecursive(newBoard, TILE_SPAWN,
                                             depth, prob / 4.0);
            float score = result.score;
            if (score >= maxScore) {
               maxScore = score;
               maxMove = move;
            }
         }
         delete newBoard;

         // move right
         move = RIGHT;
         newBoard = new Board(*board);
         moveScore = newBoard->makeMove(move);
         if (moveScore != -1) {
            Result result = getMoveRecursive(newBoard, TILE_SPAWN,
                                             depth, prob / 4.0);
            float score = result.score;
            if (score >= maxScore) {
               maxScore = score;
               maxMove = move;
            }
         }
         delete newBoard;

         stateCache.insert({state, maxScore});
         return Result(maxScore, maxMove);
      }
      break;
   case TILE_SPAWN:
      {
         float expectedScore = 0;
         float twoTileScores = 0;
         float fourTileScores = 0;

         int size = board->getSize();
         int emptySlots = board->getNumOpenSpaces();
         for (int row = 0; row < size; row++) {
            for (int col = 0; col < size; col++) {
               if (board->getRawPos(row, col) == 0) {
                  Board* newBoard;
                  int tile;
                  double newProb;

                  // spawn a 2^1 = 2 tile in the empty position
                  tile = 1;
                  newBoard = new Board(*board);
                  newBoard->setRawPos(row, col, tile);
                  newProb = prob * (1.0 / emptySlots) * 0.9;
                  {
                     Result result = getMoveRecursive(newBoard, USER,
                                                      depth - 1, newProb);
                     twoTileScores += result.score;
                  }
                  delete newBoard;

                  // spawn a 2^2 = 4 tile in the empty position
                  tile = 2;
                  newBoard = new Board(*board);
                  newBoard->setRawPos(row, col, tile);
                  newProb = prob * (1.0 / emptySlots) * 0.1;
                  {
                     Result result = getMoveRecursive(newBoard, USER,
                                                      depth - 1, newProb);
                     fourTileScores += result.score;
                  }
                  delete newBoard;
               }
            }
         }
         if (emptySlots == 0) {
            expectedScore = 0;
         } else {
            expectedScore = (0.9 * (twoTileScores / emptySlots) +
                             0.1 * (fourTileScores / emptySlots));
         }
         stateCache.insert({state, expectedScore});
         return Result(expectedScore, NO_MOVE);
      }
      break;
   }
}

int ExpectiMaxPlayer::getMove(Board* board) {
   stateCache.clear();
   Result result = getMoveRecursive(board, USER, depth, 1.0);
   return result.move;
}
