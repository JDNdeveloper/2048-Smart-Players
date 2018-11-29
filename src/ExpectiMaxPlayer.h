#include <iostream>
#include <vector>

typedef std::vector< std::vector<int> > Board;

enum Move {
   UP = 1,
   DOWN = 2,
   LEFT = 3,
   RIGHT = 4
};

class ExpectiMaxPlayer {
 public:
   // TODO take in "Board board"
   int getMove(){
      return UP;
   }
};
