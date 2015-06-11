from matplotlib import pyplot as plt
import numpy as np
import math
import time
from IPython.display import display
from IPython.display import clear_output
from IPython.display import Image
from ipythonblocks import BlockGrid




def random_grid(N,x,y):          #This generates a random size x size  matrix with 1's and 2's randomly distributed
    A= np.zeros(N**2)                        # x is the desired number of 1's
    coords=np.random.permutation(N**2)       # y is the desired number of 2's
    A[coords[:x]]=1
    A[coords[x:(x+y)]]=2
    A=A.reshape((N,N))
    print(A)
    return A

def locate_empty(A):         # Retrieves empty spaces
    N=A.shape[0]
    empty=[]
    for i in range(0,N):
        for j in range(0,N):
            if A[i,j]==0:
                empty.append((i,j))
            
    return empty

def get_neighbors(row,col,N):                              #neighbors are listed in a clockwise fashion,starting from above.
    if row==0 and col ==0:              #-------tl
        return [(0,1),(1,1),(1,0)]
    elif row ==0 and col ==N-1:          #---tr
        return [(1,N-1),(1,N-2),(0,N-2)]
    elif row==N-1 and col ==N-1:         #------br
        return [(N-2,N-1),(N-1,N-2),(N-2,N-2)]
    elif row==N-1 and col==0:            #-------bl
        return[(N-2,0),(N-2,1),(N-1,1)]
    elif row==0:                          # first row
        return[(0,col+1),(1,col+1),(1,col),(1,col-1),(0,col-1)]
    elif row==N-1:                       #last row
        return[(N-2,col),(N-2,col+1),(N-1,col+1),(N-1,col-1),(N-2,col-1)]
    elif col==0:                         #first column
        return[(row-1,col),(row-1,col+1),(row,col+1),(row+1,col+1),(row+1,col)]
    elif col==N-1:                       #last column
        return[(row-1,col),(row+1,col),(row+1,col-1),(row,col-1),(row-1,col-1)]
    else:                                # all other indices
        return[(row-1,col),(row-1,col+1),(row,col+1),(row+1,col+1),(row+1,col),(row+1,col-1),(row,col-1),(row-1,col-1)]
        
        

        
        
        
        
def how_satisfied(A):                       #Returns a matrix C that indicates satisfaction of elements in 
    C=np.empty((len(A),len(A)))             # argument matrix A.
    for i in range(len(A)):
        for j in range(len((A))):
            if A[i,j]==1 or A[i,j]==2:           
                B=get_neighbors(i,j,len(A))
                count=0
                for k in range(len(B)):
                    if A[i,j]==A[B[k]] or A[B[k]]==0:
                        count+=1
                C[i,j]=(count/len(B))
    return C
                
    
    
def unsatisfied(A,B,P):                # Retrieves coordinates of those that are unsatisfied.
    C=[]
    for i in range(len(B)):
        for j in range(len(B)):
            if A[i,j]==1 or A[i,j]==2:
                if B[i,j] < P:
                    C.append((i,j))        
    return C




def relocate(A,P):      # input: A=random_grid(N,x,y)
    N=A.shape[0]
    B=how_satisfied(A)  # returns matrix w/ satisfaction values
    C=unsatisfied(A,B,P)  # returns a list of all unsatisfied coordinates
    D=locate_empty(A)   # returns list of all empty spaces
    
    E= np.random.permutation(len(D))
    F= np.random.permutation(len(C))
    for i in range(min(len(C),len(D))):
        source=C[F[i]]
        target=D[E[i]]
        A[source],A[target]=A[target],A[source]
            
    return A            # returns a matrix with swapped elements
    
    
    
def colored_grid_process(A,P):            # This function implements iPythonBlocks into my code and displays
    A= relocate(A,P)                      # the random grid generated w/ colored blocks. Red represents 1s. Blues represents 2s.
    N=A.shape[0]
    grid= BlockGrid(N,N,block_size=10)    #  black represents empty spaces.
    for i in range(0,N):
        for j in range(0,N):
            if A[i,j]==1:
                grid[i,j].red=200
            if A[i,j]==2:
                grid[i,j].blue=200
            if A[i,j]==0:
                grid[i,j].green=10
                
    return grid 

def process(A,P,t):                      # runs colored_grid_process t number of times.
    for i in range(t):
        clear_output(True)
        r=colored_grid_process(A,P)
        display(r)
        time.sleep(.00000001)
        
        
def mean_sat(A):                        # finds the mean satisfaction of my grid.
    f=[]
    for i in range(len(A)):
        for j in range(len(A)):
            if A[i,j]==0:
                f.append((i,j))        # these are the indicies where it is 0 in our original grid.
    B=how_satisfied(A)                 # find the satisfaction of each element
    for i in range(len(f)):
        B[f[i]]=np.nan                 #makes sure that 0's do not affect our mean
    B=B[~np.isnan(B)]                  #http://stackoverflow.com/questions/11620914/removing-nan-values-from-an-array
    return np.mean(B)




def plot(A,P,t):                         # Pretty much combination of all of my above functions
    ls=[]
    iterations=np.linspace(1,t,t)
    for i in range(len(iterations)):
        process(A,P,1)
        mean=mean_sat(A)
        ls.append(mean)
    plt.figure(figsize=(7,7))            # with the addition of an output of the satisfaction values over time
    plt.plot(iterations,ls)
    plt.xlabel('Number of Iterations')
    plt.ylabel(' Satisfaction')
    plt.title('Satisfaction Over Time')
    plt.box(False)
    print('Initial satisfaction: ',ls[0],           
         'Final satisfaction: ',ls[-1])