#include <functional>
#include <iostream>
#include <unordered_map>
#include <vector>
#ifdef __linux__
#include <mutex>
#include "ctpl_stl.h"
#endif

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

class State {
 public:
   std::string board;
   Player player;
   int depth;

   State(std::string boardArg, Player playerArg, int depthArg) {
      board = boardArg;
      player = playerArg;
      depth = depthArg;
   };
   bool operator==(const State& rhs) const {
      return (rhs.board == board &&
              rhs.player == player &&
              rhs.depth == depth);
   };
};

typedef std::unordered_map<State, int> StateCache;

namespace std {
   template <> struct hash<State> {
      size_t operator()(const State& state) const {
         return hash<int>()(hash<string>()(state.board) +
                            hash<int>()(state.player) +
                            hash<int>()(state.depth));
      }
   };
}

class Board {
 public:
   Board(int);
   Board(const Board&);
   ~Board();

   // byte-array direct interface
   inline void setRawPos(int, int, char);
   inline char getRawPos(int, int);

   // byte-array wrapped interface
   inline void setPos(int, int, int);
   inline int getPos(int, int);
   std::string getString();

   // output helpers
   void printBoard();

   int getSize() { return size; };
   int getTileSum();
   int getMaxTile();
   void setScore(int scoreArg) { score = scoreArg; };
   bool isMonotonicIncreasingCol(int i);
   bool isMonotonicDecreasingCol(int i);
   bool isMonotonicIncreasingRow(int i);
   bool isMonotonicDecreasingRow(int i);
   int isMonotonicRows();
   bool maxTilePenalty();
   int getSnakeBonus();
   int getTopLeftMonotonicity();
   int getTopRightMonotonicity();
   int getBotLeftMonotonicity();
   int getBotRightMonotonicity();
   int getAdjacentTiles();
   int getScore() { return score; };
   int getNumOpenSpaces();
   int makeMove(Move);
 private:
   int size;
   int length;
   int score;
   char* boardByteArray;

   inline int getIndex(int row, int col) { return row * size + col; };
};

class ExpectiMaxPlayer {
 public:
   ExpectiMaxPlayer(bool, int, double);
   Result getMoveRecursive(Board*, Player, int, double);
   int getMove(Board*);
 private:
#ifdef __linux__
   ctpl::thread_pool pool;
   std::mutex cacheLock;
#endif
   const bool debug;
   const int depth;
   const double probCutoff;
   StateCache stateCache;
};
