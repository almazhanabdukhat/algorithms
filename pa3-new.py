
class Soldier():
    def __init__(self, name, score):
        self.score = score
        self.name = name
        self.index=None

class soldierHeap(): #minheap
    def __init__(self):
        self.heap = []
        self.hashMap = dict()

    #add score to a particular candidate
    def add_score(self, score:int, name):
        soldier=self.hashMap[name]
        if score>0:
            soldier.score+=score
            self.floatDown(soldier.index)
        #if score is negative, we substract the score
        elif score<0:
            soldier.score-=score
            self.floatUp(soldier.index)
            
    #return minimum value    
    def peakMin(self):
        return self.heap[0]
    
    def hasLeft(self,i:int) -> bool:
        return 0 <= (2*i) + 1 < len(self.heap)

    def hasRight(self,i:int) -> bool:
        return 0 <= (2*i)+2 < len(self.heap)

    def hasParent(self,i:int) -> bool:
        return 0 <= (i-1)//2 < len(self.heap)

    def left(self, i:int):
        return self.heap[(2*i) + 1]

    def right(self, i:int):
        return self.heap[(2 * i) + 2]

    def parent(self, i:int):
        return self.heap[(i-1)//2]
    

    #float element up to preserve min heap condition (analogy based on binary tree heap)
    def floatUp(self, i):
        while self.hasParent(i) and self.heap[i].score < self.parent(i).score:
            soldier = self.heap[i]
            self.swap(soldier, self.parent(i))
            i = (i-1)//2
           
        
    #sink element down to preserve min heap condition (analogy based on binary tree heap)
    def floatDown(self,i):
        while self.hasLeft(i):
            soldier = self.heap[i]
            min_child_i = 2*i+1 #smallest child is the left child
            if self.hasRight(i) and self.left(i).score > self.right(i).score:
                min_child_i = 2*i+2 #smallest child is the right child
            if soldier.score > self.heap[min_child_i].score:
                self.swap(self.heap[i], self.heap[min_child_i])
                i = min_child_i
            else:
                break


    #swap elements in the heap and adjust their respective indices            
    def swap(self,s1,s2):        
        self.heap[s1.index], self.heap[s2.index] = self.heap[s2.index], self.heap[s1.index]
        s1.index, s2.index = s2.index, s1.index


    #delete the minimum element at heap[0] 
    def deleteMin(self):
        minimum=self.peakMin()
        #swap the minimum element with the last element in the heap
        self.swap(self.heap[0],self.heap[-1])
        #delete the minimum element
        del self.hashMap[self.heap[-1].name]
        del self.heap[-1]
        #sink the newly swapped element to preserve minheap condition
        self.floatDown(0)

        
    #insert a new element   
    def insert(self, soldier):
        #insert element to the end of the heap
        self.heap.append(soldier) 
        soldier.index = len(self.heap)-1
        #float the element up to preserve minheap condition
        self.floatUp(soldier.index)


    #delete elements below a certain threshold
    def clearThreshold(self, threshold):
        minimum = self.peakMin().score 
        while threshold > minimum: 
            self.deleteMin()
            minimum=self.peakMin().score
        return len(self.heap)
            
            


def main():   
    n = int(input().strip())
    heap = soldierHeap()
    hashMap = heap.hashMap

    for x in range(n): 
        data_n=input().strip().split()  
        soldier_name=(data_n[0])
        score = int(data_n[1])
        soldier = Soldier(soldier_name, score)
        heap.insert(soldier)
        hashMap[soldier_name] = soldier 

    
    m = int(input().strip())
    solution = []
    for x in range(m): 
        data_m=input().strip().split() 
        query_type=int(data_m[0])
        if query_type == 1:
            candidate=data_m[1]
            score_to_add=int(data_m[2])
            heap.add_score(score_to_add,candidate)
        elif query_type == 2:
            threshold=int(data_m[1])
            val = heap.clearThreshold(threshold)
            solution.append(val)
      


    for k in solution:
        print(k)


if __name__ == "__main__":
    main()















