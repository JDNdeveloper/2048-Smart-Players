#include <iostream>
#include <vector>

typedef std::vector<int> RowVec;
typedef std::vector<RowVec*> BoardVec;

enum Move {
   NO_MOVE = -1,
   UP = 1,
   DOWN = 2,
   LEFT = 3,
   RIGHT = 4
};

enum Player {
   USER,
   TILE_SPAWN
};

class Result {
 public:
   float score;
   Move move;

   Result(float scoreArg, Move moveArg) {
      score = scoreArg;
      move = moveArg;
   };
};

class Board {
 public:
   Board(int);
   Board(const Board&);
   ~Board();
   void print();
   void setPos(int, int, int);
   int getPos(int row, int col) { return boardVec->at(row)->at(col); };
   int getSize() { return size; };
   int getTileSum();
   int getMaxTile();
   void setScore(int scoreArg) { score = scoreArg; };
   int getScore() { return score; };
   int makeMove(Move);
 private:
   int size;
   int score;
   BoardVec* boardVec;
};

class ExpectiMaxPlayer {
 public:
   ExpectiMaxPlayer(bool, int);
   int getMove(Board*);
 private:
   bool debug;
   int depth;
};
