#include <iostream>
#include <vector>

typedef std::vector<int> RowVec;
typedef std::vector<RowVec*> BoardVec;

enum Move {
   UP = 1,
   DOWN = 2,
   LEFT = 3,
   RIGHT = 4
};

class Board {
 public:
   Board(int);
   Board(const Board&);
   ~Board();
   void print();
   void setPos(int, int, int);
   int getTileSum();
   int getMaxTile();
   int makeMove(Move);
 private:
   int size;
   BoardVec* boardVec;
};

class ExpectiMaxPlayer {
 public:
   ExpectiMaxPlayer(bool);
   int getMove(Board*);
 private:
   bool debug;
};
