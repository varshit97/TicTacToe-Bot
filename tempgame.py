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
#import sys

class Player36:

    def __init__(self):

        #Valid moves
        self.goTo={
                (0,0):[(1,0),(0,1)],
                (0,1):[(0,0),(0,2)],
                (0,2):[(0,1),(1,2)],
                (1,0):[(0,0),(2,0)],
                (1,1):[(1,1)],
                (1,2):[(0,2),(2,2)],
                (2,0):[(1,0),(2,1)],
                (2,1):[(2,0),(2,2)],
                (2,2):[(1,2),(2,1)]
                }

        #Offset for block to cell mapping
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

    def makeMove(self,board,block,enemyPos,depth,flag,parentvalues):

        # childvalues = (float("-inf"),float("inf"))
        childvalues = parentvalues
        if((depth%2)==0):
            temp = (parentvalues[0],parentvalues[1],float("inf"))
            childvalues = temp
        else:
            temp = (parentvalues[0],parentvalues[1],float("-inf"))
            childvalues = temp
        #First move
        miniMaxDict={}
        if enemyPos[0]==-1:
            pos=(4,(2,2))
            return pos

        # glaf var to determine draw of a block
        glaf=0
        #Assigning signs
        if(flag=='x' and depth!=0):
          board[enemyPos[0]][enemyPos[1]]='x'
        if(flag=='o' and depth!=0):
          board[enemyPos[0]][enemyPos[1]]='o'
        base_tuple=self.base[(enemyPos[0]/3,enemyPos[1]/3)]
        for j in range(3):
            for k in range(3):
                if board[j+base_tuple[0]][k+base_tuple[1]]=='-':
                    glaf=1
                    break
        if glaf==0:
            block[(enemyPos[0]/3)*3+(enemyPos[1]/3)]='D'

        ourBlocks=self.goTo[(enemyPos[0]%3,enemyPos[1]%3)]
        
        #Checking for moves
        templist=[]
        for iters in range(len(ourBlocks)):
            if(block[ourBlocks[iters][0]*3+ourBlocks[iters][1]]=='-'):
                templist.append(ourBlocks[iters])

        #Block empty or not to get a free move
        ourBlocks = templist
        if(len(ourBlocks)==0):
            templist=[]
            for position in range(9):
                if(block[position]=='-'):
                    templist.append((position/3,position%3))
        ourBlocks = templist

        #leaf node
        if(len(ourBlocks)==0):
            p = random.randint(-100,100)
            return ((p,p,p),0)

        #Final return of heuristic
        if depth==4:
            p=random.randint(-100,100)
            return ((p,p,p),0)
        else:
            for i in range(len(ourBlocks)):
                cells=ourBlocks[i]
                base_tuple=self.base[cells]
                bflag=0 
                for j in range(3):
                    for k in range(3):
                        if board[j+base_tuple[0]][k+base_tuple[1]]=='-':
                            temp = [['-' for aa in range(9)] for bb in range(9)]
                            for l in range(9):
                                for m in range(9):
                                    temp[l][m]=board[l][m]
                            # print "childvalues:::",childvalues,enemyPos," ",(j+base_tuple[0],k+base_tuple[1])
                            #Calling minimax recursively
                            rtuple=self.makeMove(temp,block,(j+base_tuple[0],k+base_tuple[1]),depth+1,flag,childvalues)[0]
                            if depth%2==1:
                                temp1=(max(rtuple[2],childvalues[2]),childvalues[1],max(rtuple[2],childvalues[2]))
                                # childvalues[0]=max(rtuple[0],childvalues[0])
                                childvalues = temp1
                            if depth%2==0:
                                temp1 = (childvalues[0],min(rtuple[2],childvalues[2]),min(rtuple[2],childvalues[2]))
                                # childvalues[1]=min(rtuple[1],childvalues[1])
                                childvalues = temp1
                            # print
                            # print "Before pruning:::",rtuple," ",childvalues," ",depth," ",enemyPos," ",(j+base_tuple[0],k+base_tuple[1])
                            utility=rtuple
                            miniMaxDict[utility]=(j+base_tuple[0],k+base_tuple[1])
                            if childvalues[0]>=childvalues[1]:
                                # print
                                # print childvalues," 45678"," ",depth," ",enemyPos," ",(j+base_tuple[0],k+base_tuple[1])
                                bflag=1
                                break
                    if bflag==1:
                        break

        # print "miniMax len %s" %len(miniMaxDict)
        # print
        # print miniMaxDict
        # print

        #Return the max or min values based on level 
        if depth%2==0 and len(miniMaxDict)!=0 and depth==0:
            return sorted(miniMaxDict.items())[0]
        else:
            return (childvalues,enemyPos)
        # if depth%2==1 and len(miniMaxDict)!=0:
        #     return sorted(miniMaxDict.items())[len(miniMaxDict)-1]

    def move(self,board,block,enemyPos,flag):
        #calling minimax funtion
        temp=[]
        for i in range(9):
            temp.append(block[i])
        final=self.makeMove(board,temp,enemyPos,0,flag,(float("-inf"),float("inf"),float("inf")))
        print 'Player sign and move',flag,final[1]
        return final[1]

# flag=sys.argv[1]
# flag='x'
# play=Player36()
# board=[[0 for i in range(9)]for i in range(9)]
# block=1
# x=play.move(board,block,(6,7),flag)
# print x
