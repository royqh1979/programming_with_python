"""
8皇后问题


使用队列实现BFS（广度优先搜索）
"""
from collections import deque
from dataclasses import dataclass
from typing import List


@dataclass()
class Node:
	queens: List[int] = None
	col_flags:  List[int] = None
	diag_flags:  List[int] = None
	diag2_flags:  List[int] = None

def print_board(queens,n,count):
	print(f"------解.{count}------")
	print("  ",end="")
	for j in range(n):
		print(f"{j:<2}" ,end="")
	print()

	for i in range(1,n+1):
		print(f"{i:<2}",end="")
		for j in range(1,n+1):
			if queens[i-1] == j:
				print("Q ",end="")
			else:
				print("  ",end="")
		print()

def set_flags(node:Node,i,j,n):
	node.col_flags[j]=1
	node.diag_flags[i+j-1]=1
	node.diag2_flags[n+i-j]=1

def clear_flags(node:Node, i,j,n):
	node.col_flags[j]=0
	node.diag_flags[i+j-1]=0
	node.diag2_flags[n+i-j]=0

def can_stay(node:Node,i,j,n):
	if node.col_flags[j]==1:
		return False
	if node.diag_flags[i+j-1]==1:
		return False
	if node.diag2_flags[n+i-j]==1:
		return False
	return True



def try_queen(i,n):
	global count

	queue = deque()

	node = Node()
	# 已产生的皇后位置
	node.queens = []
	# 列标志
	node.col_flags = [0] * (n + 1)
	# 主对角线标志
	node.diag_flags = [0] * (2 * n)
	# 副对角线标志
	node.diag2_flags = [0] * (2 * n)

	queue.append(node)

	while len(queue)>0:
		node = queue.popleft()
		i = len(node.queens)+1 # 要产生第几个皇后的位置
		for q in range(1,n+1):
			if can_stay(node,i,q,n):
				if i==n:
					count+=1
					queens = node.queens.copy()
					queens.append(q)
					print_board(queens,n,count)
				else:
					new_node = Node()
					new_node.queens = node.queens.copy()
					new_node.col_flags = node.col_flags.copy()
					new_node.diag_flags = node.diag_flags.copy()
					new_node.diag2_flags = node.diag2_flags.copy()
					new_node.queens.append(q)
					set_flags(new_node,i,q,n)
					queue.append(new_node)

def queen(n):
	try_queen(1,n)


n=int(input("请输入n:"))

count = 0
queen(n)
print(f"共有{count}种解法\n")


