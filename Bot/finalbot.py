#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2016 Varshit <varshit@varshit-Lenovo>
# Copyright © 2016 Ram Kumar <ramkumar@ramkumar-HP-PC>
#
# Distributed under terms of the MIT license.

import random,datetime

class Player36:

    def __init__(self):
        """The initialisation"""

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

        self.rows=((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6))
        self.directreturn=0

    def heuristic(self,board,block,flag):
        """The main heuristic for the game"""

        blocks=((0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2))
        temp = [[0 for aa in range(3)] for bb in range(3)]
        for i in range(len(block)):
            ans=0
            base_tuple=self.base[blocks[i]]
            for j in range(8):
                os=0
                xs=0
                prerow = self.rows[j]
                for k in range(3):
                    if board[prerow[k]/3+base_tuple[0]][prerow[k]%3+base_tuple[1]]=='x':
                        xs+=1
                    if board[prerow[k]/3+base_tuple[0]][prerow[k]%3+base_tuple[1]]=='o':
                        os+=1

                if(flag=='x'):
                    if xs==3:
                        ans+=100
                    elif xs==2 and os==0:
                        ans+=10
                    elif xs==2 and os==1:
                        ans+=5
                    elif xs==1:
                        ans+=1
                    if os==3:
                        ans-=100
                    elif os==2 and xs==0:
                        ans-=10
                    elif os==2 and xs==0:
                        ans-=5

                if(flag=='o'):
                    if os==3:
                        ans+=100
                    elif os==2 and xs==0:
                        ans+=10
                    elif os==2 and xs==1:
                        ans+=5
                    elif os==1:
                        ans+=1
                    if xs==3:
                        ans-=100
                    elif xs==2 and os==0:
                        ans-=10
                    elif xs==2 and os==1:
                        ans-=5

            temp[i/3][i%3]=ans
        ans=0
        for i in range(8):
            prerow=self.rows[i]
            tempans=0
            os=0
            xs=0
            for j in range(3):
                tempans+=temp[prerow[j]/3][prerow[j]%3]/100.0
                if block[prerow[j]]=='x':
                    xs+=1
                if block[prerow[j]]=='o':
                    os+=1
            if flag=='o' and xs==3:
                ans-=1000
            if flag=='x' and os==3:
                ans-=1000
            if flag=='x' and xs==3:
                ans+=1000
            if flag=='o' and os==3:
                ans+=1000

            if flag=='o' and os==2 and xs==0:
                ans+=100
            if flag=='x' and xs==2 and os==0:
                ans+=100
            if flag=='x' and os==2 and xs==0:
                ans-=100
            if flag=='o' and xs==2 and os==0:
                ans-=100

            if flag=='o' and os==2 and xs==1:
                ans+=50
            if flag=='x' and xs==2 and os==1:
                ans+=50
            if flag=='x' and os==2 and xs==1:
                ans-=50
            if flag=='o' and xs==2 and os==1:
                ans-=50

            if flag=='o' and os==1 and xs==0:
                ans+=10
            if flag=='x' and xs==1 and os==0:
                ans+=10
            if flag=='x' and os==1 and xs==0:
                ans-=10
            if flag=='o' and xs==1 and os==0:
                ans-=10

            if flag=='o' and os==1 and xs==1:
                ans+=5
            if flag=='x' and xs==1 and os==1:
                ans+=5

            if (tempans>1 and tempans<10):
                ans+=1+((tempans-1)*9)
            elif (tempans>10 and tempans<100):
                ans+=10+(tempans-10)*90
            elif (tempans<-1 and tempans>-10):
                ans+=-1+(tempans+1)*9
            elif (tempans<-10 and tempans>-100):
                ans+=-10+(tempans+10)*90
            else:
                ans+=tempans
        return ans

    def makeMove(self,board,block,enemyPos,depth,flag,parentvalues,maxdepth):
        """The function which returns the best move among the present moves"""

        if self.flag5=='o':
            if depth%2==0:
                flag='x'
            else:
                flag='o'
        if self.flag5=='x':
            if depth%2==0:
                flag='o'
            else:
                flag='x'
        childvalues = parentvalues
        if((depth%2)==1):
            temp = (parentvalues[0],parentvalues[1],float("inf"))
            childvalues=temp
        else:
            temp = (parentvalues[0],parentvalues[1],float("-inf"))
            childvalues=temp

        #First move
        miniMaxDict={}
        if enemyPos[0]==-1:
            pos=(4,(4,4))
            return pos

        # glaf var to determine draw of a block
        glaf=0

        #Assigning signs
        if(flag=='x' and depth!=0):
          board[enemyPos[0]][enemyPos[1]]='x'
        if(flag=='o' and depth!=0):
          board[enemyPos[0]][enemyPos[1]]='o'

        base_tuple=self.base[(enemyPos[0]/3,enemyPos[1]/3)]
        glaf1=0
        for i in range(8):
            os=0
            xs=0
            prerow=self.rows[i]
            for j in range(3):
                if board[prerow[j]/3+base_tuple[0]][prerow[j]%3+base_tuple[1]]=='x':
                    xs+=1
                if board[prerow[j]/3+base_tuple[0]][prerow[j]%3+base_tuple[1]]=='o':
                    os+=1
            if os==3:
                block[(enemyPos[0]/3)*3+(enemyPos[1]/3)]='o'
                glaf1=1
                break
            if xs==3:
                block[(enemyPos[0]/3)*3+(enemyPos[1]/3)]='x'
                glaf1=1
                break

        for j in range(3):
            for k in range(3):
                if board[j+base_tuple[0]][k+base_tuple[1]]=='-':
                    glaf=1
                    break
        if (glaf==0 and glaf1==0):
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
            p=self.heuristic(board,block,self.flag5)
            return ((p,p,p),0)

        #Final return of heuristic
        if depth==maxdepth:
            p=self.heuristic(board,block,self.flag5)
            return ((p,p,p),0)
        else:
            for i in range(len(ourBlocks)):
                cells=ourBlocks[i]
                base_tuple=self.base[cells]
                bflag=0 
                for j in range(3):
                    for k in range(3):
                        if self.directreturn==1:
                            break
                        if board[j+base_tuple[0]][k+base_tuple[1]]=='-':
                            temp = [['-' for aa in range(9)] for bb in range(9)]
                            for l in range(9):
                                for m in range(9):
                                    temp[l][m]=board[l][m]
                            tempblock = [0 for aaa in range(9)]
                            for aaa in range(9):
                                tempblock[aaa]=block[aaa]

                            #Calling minimax recursively
                            rtuple=self.makeMove(temp,tempblock,(j+base_tuple[0],k+base_tuple[1]),depth+1,flag,childvalues,maxdepth)[0]
                            if depth%2==0:
                                temp1=(max(rtuple[2],childvalues[2]),childvalues[1],max(rtuple[2],childvalues[2]))
                                childvalues = temp1
                            if depth%2==1:
                                temp1 = (childvalues[0],min(rtuple[2],childvalues[2]),min(rtuple[2],childvalues[2]))
                                childvalues = temp1
                            utility=rtuple
                            miniMaxDict[utility]=(j+base_tuple[0],k+base_tuple[1])
                            if childvalues[0]>=childvalues[1]:
                                bflag=1
                                break
                    if bflag==1:
                        break

        #Return the max or min values based on level 
        if depth%2==0 and len(miniMaxDict)!=0 and depth==0:
            maxutility=float("-inf")
            pointtogo=(1,2)
            for qqq in range(len(miniMaxDict)):
                if miniMaxDict.keys()[qqq][2]>maxutility:
                    maxutility=miniMaxDict.keys()[qqq][2]
                    pointtogo = miniMaxDict.values()[qqq]
            return (0,pointtogo)
        else:
            return (childvalues,enemyPos)

    def move(self,board,block,enemyPos,flag):
        """The function which the evaluator calls"""

        #calling minimax funtion
        starttime = datetime.datetime.now()
        self.flag5=flag
        temp=[]
        for i in range(9):
            temp.append(block[i])
        final=self.makeMove(board,temp,enemyPos,0,flag,(float("-inf"),float("inf"),float("inf")),4)
        endtime = datetime.datetime.now()
        runtime = endtime-starttime
        return final[1]
