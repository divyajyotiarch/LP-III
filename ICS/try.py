'''
Refer Sbox1 and Sbox2 
http://mercury.webster.edu/aleshunas/COSC%205130/G-SDES.pdf
'''

def string2bits(s=''):
    return [bin(ord(x))[2:].zfill(8) for x in s]

def bits2string(b=None):
    return ''.join([chr(int(x, 2)) for x in b])

text = input("Enter plaintext: ")
b = string2bits(text)
print(b)

#plainTxt = list(map(int,input("Enter 8bit plain text: ").split(" ")))
inputKey = list(map(int,input("Enter 10bit input key: ")))

P8 = [5,2,6,3,7,4,9,8]
IP = [1,5,2,0,3,7,4,6]
E_P = [3,0,1,2,1,2,3,0]
IP_1 = [3,0,2,4,6,1,7,5] #IP inverse
P4 = [1,3,2,0]
P10 = [2,4,1,6,3,9,0,8,7,5]

#parameters are permutation choice and txt or key
def pcBox(pc,p_k):
	arr=[]
	for i in range(0,len(pc)):
		arr.append(p_k[pc[i]])
	return arr

pc10_k = pcBox(P10,inputKey)
L0 = pc10_k[0:5]
R0 = pc10_k[5:10]
print("P10(K): ",pc10_k)

def Shift_1(K):
	ele = K[0]
	K.pop(0)
	K.append(ele)
	return K

shift1_l0 = Shift_1(L0)
shift1_r0 = Shift_1(R0)
shift1 = shift1_l0 + shift1_r0
print("Shift(P10(K)): ",shift1)

key1 = pcBox(P8,shift1)
#key1 generated
print("P8(Shift(P10(K))) --> KEY 1: ")
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
key2 = pcBox(P8,shift3)
print("P8(Shift3(P10(K))) --> KEY 2: ")
print(key2)

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
['1 0','0 0','0 1','1 1'],
['1 1','0 0','0 1','0 0'],
['1 0','0 1','0 0','1 1']]


#4bit string R(=right half) and 8bit key
def F(R,k):
	expt = pcBox(E_P,R)
	print("E/P(R): ",expt)
	xorv = xoring(k,expt)
	print("E/P(R) xor K: ",xorv)
	S1 = xorv[0:4]	#left half
	S2 = xorv[4:8]	#right half
	row1 = S1[0]*2+S1[3]
	col1 = S1[1]*2+S1[2]
	row2 = S2[0]*2+S2[3]
	col2 = S2[1]*2+S2[2]
	return sbox1[row1][col1]+' '+sbox2[row2][col2]
	

		
#xoring L and F(R,k1)
def funcFk(L,S,R):
	xorVal=[]
	for i in range(0,4):
		xorVal.append(L[i]^S[i])
	return R,xorVal


def execute(plainTxt):
	initP = pcBox(IP,plainTxt)
	print("IP(P): ")
	print(initP)

	L = initP[0:4]
	R = initP[4:8]

	#output of F(p,k) goes into P4 permutation

	#4 bit output of Sboxes
	finalS1 = list(map(int,F(R,key1).split(" ")))
	print("SBoxes(E/P(R) xor key1): ",finalS1)
	permS1 = pcBox(P4,finalS1)

	print("P4(SBoxes(E/P(R) xor key1): ")
	print(permS1)

	#round 1
	#after switching
	L1,R1 = funcFk(L,permS1,R)
	print("L and R after round 1")
	print(L1)
	print(R1)
	
	#round 2 using key2 and L1,R1
	finalS2 = list(map(int,F(R1,key2).split(" ")))
	print("SBoxes(E/P(R) xor key2): ",finalS2)

	permS2 = pcBox(P4,finalS2)
	print("P4(SBoxes(E/P(R) xor key2): ")
	print(permS2)

	L2,R2 = funcFk(L1,permS2,R1)

	#keep the xored value as it is
	print("After Round2: ")
	print(L2)
	print(R2)
	#p2 = L2+R2
	p2 = R2+L2
	cTxt = pcBox(IP_1,p2)
	return cTxt

cipherTxt=[]
for x in b:
	plainTxt = list(map(int,x))
	cTxt = execute(plainTxt)
	cipherTxt.append(cTxt)
print("Cipher: ")
print(cipherTxt)

#decryption ---------------------------------------------------------
print("Decryption")
initC = pcBox(IP,cipherTxt)
print("IP(C): ")
print(initC)
L = initC[0:4]
R = initC[4:8]

finalS1 = list(map(int,F(R,key2).split(" ")))
#print("SBoxes(E/P(R) xor key2): ",finalS1)
permS1 = pcBox(P4,finalS1)
#print("P4(SBoxes(E/P(R) xor key2): ")
print(permS1)
L1,R1 = funcFk(L,permS1,R)
print("L and R after round 1")
print(L1)
print(R1)

#round 2 using key2 and L1,R1
finalS2 = list(map(int,F(R1,key1).split(" ")))
#print("SBoxes(E/P(R) xor key1): ",finalS2)

permS2 = pcBox(P4,finalS2)
#print("P4(SBoxes(E/P(R) xor key1): ")
print(permS2)

L2,R2 = funcFk(L1,permS2,R1)

#keep the xored value as it is
print("After Round2: ")
print(L2)
print(R2)
#p2 = L2+R2
p2 = R2+L2

pTxt = pcBox(IP_1,p2)
print("Plaintext: ")
print(pTxt)	





		
	
	


	
	




