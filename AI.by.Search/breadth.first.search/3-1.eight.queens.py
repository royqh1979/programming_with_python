"""
8皇后问题


使用队列实现BFS（广度优先搜索）
"""
from collections import deque

def print_board(n,count):
	print(f"------解.{count}------")
	print("  ",end="")
	for j in range(n):
		print(f"{j:<2}" ,end="")
	print()

	for i in range(1,n+1):
		print(f"{i:<2}",end="")
		for j in range(1,n+1):
			if queens[i] == j:
				print("Q ",end="")
			else:
				print("  ",end="")
		print()

def set_flags(i,j,n):
	col_flags[j]=1
	diag_flags[i+j-1]=1
	diag2_flags[n+i-j]=1

def clear_flags(i,j,n):
	col_flags[j]=0
	diag_flags[i+j-1]=0
	diag2_flags[n+i-j]=0

def can_stay(i,j,n):
	if col_flags[j]==1:
		return False
	if diag_flags[i+j-1]==1:
		return False
	if diag2_flags[n+i-j]==1:
		return False
	return True

def try_queen(i,n):
	global count

	queue = deque()

	node = object()
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
					print_board(n,count,)
				else:
					new_node = object()
					new_node.queens = node.queens.copy()
					new_node.col_flags = node.col_flags
					new_node.diag_flags = node.diag_flags
					new_node.diag2_flags = node.diag2_flags
					new_node.queens.append(q)
					set_flags(new_node,i,q,n)
					queue.append(new_node)

def queen(n):
	try_queen(1,n)


n=int(input("请输入n:"))

count = 0
queen(n)
print(f"共有{count}种解法\n")


