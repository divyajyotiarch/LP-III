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
print(shift3)
key2 = P8(shift3)
print("KEY 2: ")
print(key2)
	


	
	




