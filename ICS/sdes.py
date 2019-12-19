'''
Refer Sbox1 and Sbox2 
https://www.c-sharpcorner.com/article/s-des-or-simplified-data-encryption-standard/
'''
plainTxt = list(map(int,input("Enter 8bit plain text: ").split(" ")))
inputKey = list(map(int,input("Enter 10bit input key: ").split(" ")))

#generation of key k1 by P10,Shift,P8
def P10(K):
	pc10 = [2,4,1,6,3,9,0,8,7,5] 
	arr=[]
	for i in range(0,10):
		arr.append(K[pc10[i]])
	return arr

pc10_k = P10(inputKey)
L0 = pc10_k[0:5]
R0 = pc10_k[5:10]
print(L0)
print(R0)

def Shift_1(K):
	ele = K[0]
	K.pop(0)
	K.append(ele)
	return K

shift1_l0 = Shift_1(L0)
shift1_r0 = Shift_1(R0)
shift1 = shift1_l0 + shift1_r0
print(shift1)

def P8(K):
	pc8 = [5,2,6,3,7,4,9,8]
	arr=[]
	for i in range(0,8):
		arr.append(K[pc8[i]])
	return arr

key1 = P8(shift1)
#key1 generated
print("KEY 1: ")
print(key1)




def Shift_3(K):
	for i in range(0,2):
		ele = K[0]
		K.pop(0)
		K.append(ele)
	return K

shift3_l0 = Shift_3(L0)
shift3_r0 = Shift_3(R0)
shift3 = shift3_l0 + shift3_r0
#print(shift3)
key2 = P8(shift3)
print("KEY 2: ")
print(key2)

def InitPerm(txt):
	ip1 = [1,5,2,0,3,7,4,6]
	arr=[]
	for i in range(0,8):
		arr.append(txt[ip1[i]])
	return arr

initP = InitPerm(plainTxt)
print("IP(P): ")
print(initP)

L = initP[0:4]
R = initP[4:8]

def ExpandPerm(txt):
	exp = [3,0,1,2,1,2,3,0]
	arr=[]
	for i in range(0,8):
		arr.append(txt[exp[i]])
	return arr

def xoring(key,exp):
	xorVal = []
	for i in range(0,8):
		xorVal.append(key[i]^exp[i])
	return xorVal

sbox1 = [
['0 1','0 0','1 1','1 0'],
['1 1','1 0','0 1','0 0'],
['0 0','1 0','0 1','1 1'],
['1 1','0 1','1 1','1 0']]

sbox2 = [
['0 0','0 1','1 0','1 1'],
['1 1','0 0','0 1','1 1'],
['1 1','0 0','0 1','0 0'],
['1 0','0 1','0 0','1 1']]


#4bit string p(=R) and 8bit key
def F(p,k):
	expt = ExpandPerm(p)
	print(expt)
	xorv = xoring(expt,k)
	print(xorv)
	S1 = xorv[0:4]	#left half
	S2 = xorv[4:8]	#right half
	row1 = S1[0]*2+S1[3]*1
	col1 = S1[1]*2+S1[2]*1
	row2 = S2[0]*2+S2[3]*1
	col2 = S2[1]*2+S2[2]*1
	return sbox1[row1][col1]+' '+sbox2[row2][col2]
	
#output of F(p,k) goes into P4 permutation
def P4(s):
	p4 = [1,3,2,0]
	arr =[]
	for i in range(0,4):
		arr.append(s[p4[i]])
	return arr

#4 bit output of Sboxes
finalS1 = list(map(int,F(R,key1).split(" ")))
permS1 = P4(finalS1)

print("4 bit output of P4(Sboxes): ")
print(permS1)
		
#xoring L and F(R,k1)
def funcFk(L,S,R):
	xorVal=[]
	for i in range(0,4):
		xorVal.append(L[i]^S[i])
	return R,xorVal

#after switching
L1,R1 = funcFk(L,permS1,R)
print("L and R after round 1")
print(L1)
print(R1)
	
#round 2 using key2 and L1,R1
finalS2 = list(map(int,F(R1,key2).split(" ")))
#print(permS2)
permS2 = P4(finalS2)
print(permS2)
L2,R2 = funcFk(L1,permS2,R1)

print("After Round2: ")
print(L2)
print(R2)
	
	





		
	
	


	
	




