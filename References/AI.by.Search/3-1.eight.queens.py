"""
8皇后问题


"""
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
	for j in range(1,n+1):
		if can_stay(i,j,n):
			queens[i] = j
			if i==n:
				count+=1
				print_board(n,count)
			else:
				set_flags(i,j,n)
				try_queen(i+1,n)
				clear_flags(i,j,n)
			queens[i] = 0

def queen(n):
	try_queen(1,n)


n=int(input("请输入n:"))
queens = [0]*(n+1)
# 列标志
col_flags=[0]*(n+1)
# 主对角线标志
diag_flags = [0]*(2*n)
# 副对角线标志
diag2_flags = [0] * (2*n)

count = 0
queen(n)
print(f"共有{count}种解法\n")


