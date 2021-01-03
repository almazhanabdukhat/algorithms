class Node(object):
    def __init__(self):
        self.guide = None
        # guide points to max key in subtree rooted at node


class InternalNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.child0 = None
        self.child1 = None
        self.child2 = None
        # child0 and child1 are always non-none
        # child2 is none iff node has only 2 children

    def tlist(self):
        children = self.child0.tlist()
        children.extend(self.child1.tlist())
        if not self.child2 is None:
            children.extend(self.child2.tlist())
        offset = ["               " + i for i in children]
        offset.insert(1, self.guide)
        return offset

    def __str__(self):
        return "\n".join(self.tlist())


class LeafNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.value = None
        # guide points to the key

    def tlist(self):
        return [str(self.guide) + " " + str(self.value)]

    def __str__(self):
        return "\n".join(self.tlist())


class TwoThreeTree:
    def __init__(self):
        self.root = None
        self.height = -1


class WorkSpace:
    def __init__(self):
        self.newNode = None
        self.offset = None
        self.guideChanged = None
        self.scratch = [None] * 4


def insert(key, value, tree):
    # insert a key value pair into tree (overwrite existsing value
    # if key is already present)

    h = tree.height

    if h == -1:
        newLeaf = LeafNode()
        newLeaf.guide = key
        newLeaf.value = value
        tree.root = newLeaf
        tree.height = 0

    else:
        ws = doInsert(key, value, tree.root, h)

        if ws != None and ws.newNode != None:
            # create a new root

            newRoot = InternalNode()
            if ws.offset == 0:
                newRoot.child0 = ws.newNode
                newRoot.child1 = tree.root

            else:
                newRoot.child0 = tree.root
                newRoot.child1 = ws.newNode

            resetGuide(newRoot)
            tree.root = newRoot
            tree.height = h + 1


def doInsert(key, value, p, h):
    # auxiliary recursive routine for insert

    if h == 0:
        # we're at the leaf level, so compare and
        # either update value or insert new leaf

        leaf = p  #downcast (unnecessary in python)
        cmp = 0
        if key < leaf.guide:
            cmp = -1
        elif key > leaf.guide:
            cmp = 1

        if cmp == 0:
            leaf.value = value
            return None

        # create new leaf node and insert into tree
        newLeaf = LeafNode()
        newLeaf.guide = key
        newLeaf.value = value

        offset = 1
        if cmp < 0:
            offset = 0
        # offset == 0 => newLeaf inserted as left sibling
        # offset == 1 => newLeaf inserted as right sibling

        ws = WorkSpace()
        ws.newNode = newLeaf
        ws.offset = offset
        ws.scratch = [None] * 4

        return ws

    else:
        q = p  # downcast (unnecessary in python)
        pos = 2
        ws = None

        if key <= q.child0.guide:
            pos = 0
            ws = doInsert(key, value, q.child0, h - 1)

        elif key <= q.child1.guide or q.child2 is None:
            pos = 1
            ws = doInsert(key, value, q.child1, h - 1)

        else:
            pos = 2
            ws = doInsert(key, value, q.child2, h - 1)
        if ws != None:
            if ws.newNode != None:
                # make ws.newNode child # pos + ws.offset of q
                sz = copyOutChildren(q, ws.scratch)

                ws.scratch.insert(pos + ws.offset, ws.newNode)

                if sz == 2:
                    ws.newNode = None
                    ws.guideChanged = resetChildren(q, ws.scratch, 0, 3)
                else:
                    ws.newNode = InternalNode()
                    ws.offset = 1
                    resetChildren(q, ws.scratch, 0, 2)
                    resetChildren(ws.newNode, ws.scratch, 2, 2)

            elif ws.guideChanged:
                ws.guideChanged = resetGuide(q)

        return ws


def copyOutChildren(q, x):
    # copy children of q into x, and return # of children

    sz = 2
    x[0] = q.child0
    x[1] = q.child1
    if q.child2 != None:
        x[2] = q.child2
        sz = 3

    return sz


def resetGuide(q):
    # reset q.guide, and return true if it changes.

    oldGuide = q.guide
    if q.child2 != None:
        q.guide = q.child2.guide
    else:
        q.guide = q.child1.guide

    return q.guide != oldGuide


def resetChildren(q, x, pos, sz):
    # reset q's children to x[pos..pos+sz), where sz is 2 or 3.
    # also resets guide, and returns the result of that

    q.child0 = x[pos]
    q.child1 = x[pos + 1]

    if sz == 3:
        q.child2 = x[pos + 2]
    else:
        q.child2 = None

    return resetGuide(q)

#auxiliary function to search for the key 
def search(tree,x):
    h=tree.height 
    r=tree.root 
    search_path=[]  #record search path
    for i in range(h): 
        if x<=r.child0.guide: #key is in the child0 subtree
            search_path.append(r) 
            r=r.child0 
        elif r.child2 is None or x<=r.child1.guide: 
            search_path.append(r) #key is in the child1 subtree
            r=r.child1
        else: #key is in the child2 subtree
            search_path.append(r)
            r=r.child2
    search_path.append(r) 
    return search_path

def printRange(tree,x,y):
    
    # x and y do not diverge
    if x == y:
        path = search(tree,x)
        #if key is in the search path
        if path[-1].guide==x:
            print(str(path[-1].guide) + " " + str(path[-1].value))
    else:
        #get search paths for keys x and y
        x_path=search(tree,x) 
        y_path=search(tree,y)

        #find where the paths diverge
        x_index = 0
        y_index = 0
        while x_index < len(x_path) and y_index < len(y_path):
            if x_path[x_index] == y_path[y_index]:
                x_index+=1
                y_index+=1
            else:
                break
        #if paths are identical return (x,y are not in the tree)
        if x_path == y_path:
            return
       
        #node at which paths diverge
        div_node=x_path[x_index - 1]
        #index at which paths diverge
        div_i=x_index
        
        #based on the search algorithm, x_path[-1] will always be printed
        #since x_path[-1].guide >= x and we print keys that are >=x
        curr_x=x_path[-1]
        print(str(x_path[-1].guide)+" "+str(x_path[-1].value))

        last_x = x_path[-1] #last processed node in the x_path
        curr_x = len(x_path) - 2 #start from the second last node in the path

        #Walk the search path from x to the divergence point
        while curr_x > -1 and x_path[curr_x]!=div_node: 
            #if last processed node is in the child0 (left-most) subtree 
            # print all leaf nodes of its siblings (always >x and thus in [x,y])
            if last_x == x_path[curr_x].child0:
                if x_path[curr_x].child2 is None:
                    printAll(x_path[curr_x].child1,tree.height - (1 + curr_x))
                else: 
                    printAll(x_path[curr_x].child1,tree.height - (1 + curr_x))
                    printAll(x_path[curr_x].child2,tree.height - (1 + curr_x))
            #if last processed node is in the child1 subtree 
            elif last_x == x_path[curr_x].child1:
                #print all leaf nodes of the second child 
                if x_path[curr_x].child2 is not None:
                    printAll(x_path[curr_x].child2,tree.height - (1 + curr_x)) 
            last_x = x_path[curr_x] 
            curr_x -= 1 #go to the next node in the x_path

        #If divergence node has 3 children and search x_path proceeds down the left-most child
        # and search path for y proceeds down the right-most child,print all nodes of the middle child
        if div_node.child2 is not None:
            if div_node.child0 == last_x and div_node.child2 == y_path[div_i]:
                printAll(div_node.child1, tree.height - 1 - curr_x)  
  
        #Walk the search path from divergence point to y           
        for k in range(div_i, len(y_path) - 1):
            curr_y = y_path[k]
            #if the next node in the y_path has siblings to the left
            #print leaf nodes of all its siblings
            if y_path[k+1]==curr_y.child2: 
                printAll(curr_y.child0,tree.height-1-k)
                printAll(curr_y.child1,tree.height-1-k)
            elif y_path[k+1] == curr_y.child1: 
                printAll(curr_y.child0,tree.height-1-k)

        #Conditionally print the last node in the y_path (y might be < y_path[-1])
        if y_path[-1].guide<=y:
            print(y_path[-1].guide+" "+y_path[-1].value)
            


#recursive function that prints all leaf nodes of a given node
def printAll(p, h):
    # base case if p is a leaf node:
    if h == 0: 
        print(str(p.guide) + " " + str(p.value)) 
    else: #otherwise, call function on all children
        printAll(p.child0,h-1)
        printAll(p.child1,h-1)
        if p.child2 is not None:
            printAll(p.child2,h-1)

    


def main():
    tree=TwoThreeTree() #create a new tree
    key_count = int(input().strip())
    
    #if key_count == 0:
        #return
    #insert the nodes to the tree
    for x in range(key_count): 
        data=input().strip().split()
        key=data[0]
        value=data[1]
        insert(key,value,tree)  
    
    if tree.root is None:
        return
   
    #for each query call the printRange
    query_count=int(input())
    for y in range(query_count):
        data=input().strip().split()
        key_first=data[0]
        key_second=data[1]
        #swap keys if second key is larger
        if key_second<key_first:
            key_first,key_second=key_second,key_first
        #print("-path: "+str(key_first)+"->"+str(key_second))
        printRange(tree, key_first, key_second)
        
    
    

if __name__ == "__main__":
    main()
