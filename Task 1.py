
#1
def orders(lizt,task):
    if task=='asc':
        for i in range (1,len(lizt)):
            for i in range (1,len(lizt)):
                if lizt[i]<lizt[i-1]:
                    lizt[i],lizt[i-1]=lizt[i-1],lizt[i]
        return lizt
    elif task=='desc':
        for i in range (1,len(lizt)):
            for i in range (1,len(lizt)):
                if lizt[i]>lizt[i-1]:
                    lizt[i],lizt[i-1]=lizt[i-1],lizt[i]
        return lizt
    else:
        return lizt
c='go'
i=0
a=[]
while c!='n':
    a.append(int(input("Enter a number: ")))
    c=str(input("Do you want to continue adding numbers? (y/n)"))
task=str(input("Enter 'asc', 'desc' or 'none': "))
xx=orders(a,task)
print(xx)

#2
def obscure(credit_no):
    new=''
    new+='*'*(len(credit_no)-4)+credit_no[-4:]
    return new
credit_no=input("Enter your credit card number: ")
xx=obscure(credit_no)
print(xx)

#3
def opp(p,q,r):
    return eval(f'{p} {q} {r}')
num1=int(input("Enter the first integer: "))
opr=input("Enter the desired operator: ")
num2=int(input("Enter the second integer: "))
op = ['+', '-', '/','*']
for i in op:
    if i==opr:
        c=opp(num1,i,num2)
        print(c)

#4
def doub(string):
    new=''
    for x in string:
        new+=x*2
    return new
string=str(input("Enter string: "))
xx=doub(string)
print(xx)

#5
import array
import random
from random import randint
arr=array.array('i',[])
arr=random.sample(range(0,100),100)
for j in range(0,len(arr)):
    if arr[j]==0:
        arr[j]=randint(1,99)
print(arr)
for k in arr:
    d=0
    for m in arr:
        if k==m:
            d+=1
    if d==2:
        print(k,' has a duplicate')
        break

#6
def prime(x):
    c=0
    for j in range (1,x):
        if x%j==0:
            c+=1
    return True if c==1 else False
print("To find prime numbers in given range\n")
start=int(input("Enter start of range: "))
end=int(input("Enter end of range: "))
for i in range(start,end+1):
    if prime(i):
        print(i)

#7
import array
ar=array.array('i',[1,2,3,6,8,5,2,3,5,3,1,3,5,7,8,9,3])
d={}
print("Elements of the array are: ")
for i in ar:
    print(i,end=', ')
for i in ar:
    if i not in d:
        mm=i
        d[mm]=0
        for k in ar:
            if i==k:
                d[mm]+=1
maxx=0
maxx_key=0
for n in d:
    if d[n]>maxx:
        maxx=d[n]
        maxx_key=n
print('\n',maxx_key,'is the highest frequency element in the array, with frequency =',maxx)

#8
q8=str(input("Enter string: "))
c=0
for i in q8:
    if i.isdigit():
        c+=int(i)
print(c)

#9
q9=str(input("Enter string: "))
q9=''.join(sorted(q9.lower()))
print(q9)

#10
n1=int(input('Enter number 1: '))
n2=int(input('Enter number 2: '))
n1=n1^n2
n2=n1^n2
n1=n1^n2
print("Number 1: ",n1,"\nNumber 2: ",n2)

#11
q11=str(input("Enter string to check palindrome: "))
if q11[0::]==q11[::-1]:
    print(q11," is a palindrome")
else:
    print(q11," is not a palindrome")

#15
q15=str(input("Enter string: "))
al=0
di=0
sp=0
for i in q15:
    if i.isdigit():
        di+=1
    elif i.isalpha():
        al+=1
    elif i!=' ':
        sp+=1
    else:
        x=1
print("Number of alphates in the string: ",al,'\nNumber of digits in the string: ',di,'\nNumber of special characters in the string: ',sp)
'''
#17
def is_pandigital(num):
    s=str(num)
    a=[]
    for i in s:
        a.append(int(i))
    x=[1,2,3,4,5,6,7,8,9,0]
    y={}
    for i in a:
        if i in x:
            x.remove(i)
    if x==[]:
        return True
    return False
def is_step(num):
    s=str(num)
    a=[];c=0
    for i in s:
        a.append(int(i))
    for i in range(1,len(a)):
        if (a[i]-a[i-1])==1 or (a[i]-a[i-1])==-1:
            c+=1
        else:
            return False
    return True
t=10**20
df=0
for q in range(1023456789,t):
    if is_pandigital(q):
        if is_step(q):
            df+=1
print(df) #NOTE: Due to large amount of data needing to be processed, the algorithm is quite slow
'''
#18
def eliminate(a):
    dic={'NORTH':1,'SOUTH':-1,'EAST':2,'WEST':-2}
    xx=[0]
    for l in a:
        xx.append(l)
    for i in a:
        for j in xx:
            if j!=0:
                c=dic[i]
                d=dic[j]
                if c+d==0:
                    a.remove(i)
                    a.remove(j)
                continue
    print(a)
a=['NORTH','SOUTH','SOUTH','EAST','WEST','NORTH','WEST']
print("Input: ",a)
print("Output: ",end='')
eliminate(a)

#19
tries=10
guess=0000
num=str(8465)
v=[]
for j in num:
    v.append(int(j))
while tries>0 and guess!=num:
    print("B: Digit entered is wrong \nY: Digit entered is right but in incorrect position \nR: Digit entered is right and in the correct position\n")
    guess=str(input("Guess the number: "))
    t=[]
    c=''
    for i in guess:
        t.append(int(i))
    for k in range(0,4):
        if t[k]==v[k]:
            c+='R'
        elif t[k] in v:
            c+='Y'
        else:
            c+='B'
    print('\n',c,'\n')
    tries-=1
    if c!="RRRR" and t!=0:
        print(tries," tries left\n")
    if t==0:
        print(tries," tries left\n")
        print("You lost the game! Better luck next time!")
'''
#20
c=0
p=[]
def is_prime(num):
    c=0
    for i in range(1,num):
        if num%i==0:
            c+=1
    if c==1:
        return True
    return False
def circular(n):
    s=str(n)
    w=[]
    z=0
    for i in s:
        w.append(int(i))
    t=w[0]
    for k in range(1,len(w)):
        w[k-1]=w[k]
    w[len(w)-1]=t
    b=10**(len(w)-1)
    for i in w:
        z+=i*b
        b/=10
    if is_prime(int(z)):
        global c
        c+=1
        if c==len(w):
            global p
            p.append(n)
            return True
        else:
            circular(int(z))
    else:
        return False
for i in range(2,1000000):#NOTE: STACK OVERFLOW. RECURSION LIMIT EXCEEDED
    c=0
    circular(i)
print(len(p))
'''
