from queue import Queue
graph = {(-1, -1): 0}
visit = {(-1, -1): 0}
h = input()
for i in range(int(h)):
	s = input()
	k = 0
	for j in range(len(s)):
		if (s[j] == ' '):
			pass
		else:
			graph[(i, k)] = int(s[j])
			visit[(i, k)] = 0
			k += 1
