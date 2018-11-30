#include <iostream>
#include <vector>

typedef std::vector<int> Row;
typedef std::vector<Row*> Board;

enum Move {
   UP = 1,
   DOWN = 2,
   LEFT = 3,
   RIGHT = 4
};

class ExpectiMaxPlayer {
 public:
   ExpectiMaxPlayer(bool debugArg) {
      debug = debugArg;
   }

   void printBoard(Board* board) {
      for (Board::iterator rowIt = board->begin(); rowIt != board->end(); rowIt++) {
         Row* row = *rowIt;
         for (Row::iterator valIt = row->begin(); valIt != row->end(); valIt++) {
            int val = *valIt;
            std::cout << val << " ";
         }
         std::cout << std::endl;
      }
      std::cout << std::endl;
   }

   int getMove(Board* board){
      if (debug) {
         printBoard(board);
      }
      return UP;
   }
 private:
   bool debug;
};
