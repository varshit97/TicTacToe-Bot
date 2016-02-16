#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 varshit <varshit@varshit-Lenovo>
#
# Distributed under terms of the MIT license.

"""

"""

import random

class Game:
    def __init__(self):
        #Blocks to Cells mapping
        self.board={
                (0,0):[[0 for i in range(3)]for i in range(3)],
                (0,1):[[0 for i in range(3)]for i in range(3)],
                (0,2):[[0 for i in range(3)]for i in range(3)],
                (1,0):[[0 for i in range(3)]for i in range(3)],
                (1,1):[[0 for i in range(3)]for i in range(3)],
                (1,2):[[0 for i in range(3)]for i in range(3)],
                (2,0):[[0 for i in range(3)]for i in range(3)],
                (2,1):[[0 for i in range(3)]for i in range(3)],
                (2,2):[[0 for i in range(3)]for i in range(3)]}
        self.boardCopy=self.board
        #Cells to Blocks mapping
        self.goTo={
                (0,0):[(1,0),(0,1)],
                (0,1):[(0,0),(0,2)],
                (0,2):[(0,1),(1,2)],
                (1,0):[(0,0),(2,0)],
                (1,1):[(1,1)],
                (1,2):[(0,2),(2,2)],
                (2,0):[(1,0),(2,1)],
                (2,1):[(2,0),(2,2)],
                (2,2):[(1,2),(2,1)]}
        self.base={
                (0,0):[0,0],
                (0,1):[0,3],
                (0,2):[0,6],
                (1,0):[3,0],
                (1,1):[3,3],
                (1,2):[3,6],
                (2,0):[6,0],
                (2,1):[6,3],
                (2,2):[6,6],
                }
    def makeMove(self,enemyPos,depth,board):
        miniMaxDict={}
        #self.board[(enemyPos[0]/3,enemyPos[1]/3)][enemyPos[0]%3][enemyPos[1]%3]=2
        board[(enemyPos[0]/3,enemyPos[1]/3)][enemyPos[0]%3][enemyPos[1]%3]=2
        ourBlocks=self.goTo[(enemyPos[0]%3,enemyPos[1]%3)]
        if depth==2:
            p=random.randint(-10,10)
            #print p,enemyPos
            return p
        else:
            for i in range(len(ourBlocks)):
                cells=ourBlocks[i]
                base_tuple=self.base[cells]
                cell=self.board[cells]
                for j in range(3):
                    for k in range(3):
                        if cell[j][k]==0:
                            utility=self.makeMove((j+base_tuple[0],k+base_tuple[1]),depth+1,board)
                            print utility,j+base_tuple[0],k+base_tuple[1]
                            miniMaxDict[utility]=(j,k)
        print miniMaxDict
        if depth%2==1 and len(miniMaxDict)!=0:
            return sorted(miniMaxDict.items())[0][0]
        if depth%2==0 and len(miniMaxDict)!=0:
            return sorted(miniMaxDict.items())[len(miniMaxDict)-1][0]



            
board={
            (0,0):[[0 for i in range(3)]for i in range(3)],
            (0,1):[[0 for i in range(3)]for i in range(3)],
            (0,2):[[0 for i in range(3)]for i in range(3)],
                (1,0):[[0 for i in range(3)]for i in range(3)],
                (1,1):[[0 for i in range(3)]for i in range(3)],
                (1,2):[[0 for i in range(3)]for i in range(3)],
                (2,0):[[0 for i in range(3)]for i in range(3)],
                (2,1):[[0 for i in range(3)]for i in range(3)],
                (2,2):[[0 for i in range(3)]for i in range(3)]}
play=Game()
print play.makeMove((7,8),0,board)
