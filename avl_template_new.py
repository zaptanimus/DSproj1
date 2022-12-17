#username - yaronreunbeni
#id1      - 208935312
#name1    - Yaron Reuben Ittah
#id2      - 11111111
#name2    - username



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type value: str
	@param value: data of your node
	"""
	def __init__(self, value = None):
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1 # Balance factor
		self.sizeNode = 0
		

	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child
	"""
	def getLeft(self):
		return self.left

	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child
	"""
	def getRight(self):
		return self.right

	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def getParent(self):
		return self.parent

	"""return the value

	@rtype: str
	@returns: the value of self, None if the node is virtual
	"""
	def getValue(self):
		return self.value

	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def getHeight(self):
		return self.height

	"""returns the size

	@rtype: int
	@returns: the size of self, 0 if the node is virtual
	"""
	def getSizeNode(self):
		return self.sizeNode

	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def setLeft(self, node):
		self.left=node

	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def setRight(self, node):
		self.right=node

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def setParent(self, node):
		self.parent = node

    """ sets right child and also sets right child's parent
        @type child: AVLnode
        @param child: a node
     """

    def setRightParent(self, child):
        self.setRight(child)
        child.setParent(self)

    """ sets left child and also sets left child's parent
        @type child: AVLnode
        @param child: a node
     """

    def setLeftParent(self, child):
        self.setLeft(child)
        child.setParent(self)


	"""sets value

	@type value: str
	@param value: data
	"""
	def setValue(self, value):
		self.value = value

	"""sets the balance factor of the node

	@type h: int
	@param h: the height
	"""
	def setHeight(self, h):
		self.height = h

	"""sets the size of the node

	@type n: int
	@param n: the height
	"""
	def setSizeNode(self, n):
		self.sizeNode = n

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def isRealNode(self):
		if self.setHeight == -1:
			return False
		return True

	"""calculate the BF of the current node 

	@rtype: int
	@returns: the balance factor of the node.
	"""
	def getBF(self):
		return self.left.getHeight() - self.right.getHeight()

	""" updates node height by computing it from childrens' height
	"""
	def updateHeight(self):
		self.setHeight(max(self.getRight().getHeight(),
                           self.getLeft().getHeight()) + 1)

	"""updates node size by computing it from childrens' size
    """
	def updateSize(self):
		self.setSize(self.getRight().getSize() + self.getLeft().getSize() + 1)

"""
A class implementing the ADT list, using an AVL tree.
"""

class AVLTreeList(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.size = 0
		self.root = None
		self.firstItem = None #minimum
		self.lastItem = None #maximum


	"""returns whether the list is empty

	@rtype: bool
	@returns: True if the list is empty, False otherwise
	"""
	def empty(self):
		if self.root == None:
			return True
		return False


	"""retrieves the value of the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: index in the list
	@rtype: str
	@returns: the the value of the i'th item in the list
	"""
	def retrieve(self, i):
		if i < 0 or i>= self.length():
			return None
		return self.treeSelect(i+1).getValue()

	"""inserts val at position i in the list

	@type i: int
	@pre: 0 <= i <= self.length()
	@param i: The intended index in the list to which we insert val
	@type val: str
	@param val: the value we inserts
	@rtype: list
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, i, val):
		node = AVLNode(val)
		
		if i == 0:
			if self.empty():
				self.root = node
				node.setLeftParent(AVLNode())
				node.setRightParent(AVLNode())
				self.lastItem = node
				self.firstItem = node

			else:
				if self.firstItem == None:
					insertLeaf(self.findMin(), node, "left")
				else:
					insertLeaf(self.firstItem, node, "left")
					self.firstItem = node

		elif i == self.length():  # inserting the maximum
			if self.lastItem == None:
				insertLeaf(self.findMax(), node, "right")
			else:
				insertLeaf(self.lastItem, node, "right")
				self.lastItem = node

		else:
			curr = self.treeSelect(i+1)
			if not curr.getLeft().isRealNode():
				insertLeaf(curr, node, "left")
			else:
				insertLeaf(self.getPredecessorOf(curr), node, "right")

		curr, balance = fixInsert(node)
		if curr != None:
			self.updateSizeAllTheWayUpFrom(curr.getParent())

		return balance


	"""deletes the i'th item in the list

	@type i: int
	@pre: 0 <= i < self.length()
	@param i: The intended index in the list to be deleted
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, i):
		return -1


	"""returns the value of the first item in the list

	@rtype: str
	@returns: the value of the first item, None if the list is empty
	"""
	def first(self):
		if self.empty():
			return None
		return self.firstItem.getValue()

	"""returns the value of the last item in the list

	@rtype: str
	@returns: the value of the last item, None if the list is empty
	"""
	def last(self):
		if self.empty():
			return None
		return self.lastItem.getValue()

	"""returns an array representing list 

	@rtype: list
	@returns: a list of strings representing the data structure
	"""
	def listToArray(self):
		return None

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		return self.size

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		return None

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		return None

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		return None

	"""searches for a *value* in the list

	@type val: str
	@param val: a value to be searched
	@rtype: int
	@returns: the first index that contains val, -1 if not found.
	"""
	def search(self, val):
		traveler = self.firstItem
		index = 0
		while traveler != None:
			if traveler.getValue() == val:
				return index
			index += 1
			traveler = self.mySuccessor(traveler)
		return -1

	"""returns the root of the tree representing the list

	@rtype: AVLNode
	@returns: the root, None if the list is empty
	"""
	def getRoot(self):
		if self.empty():
			return None
		return self.root

### service functions###

	"""returns the smallest node in the tree whose subtree of size >= k
    @type k: int
    @pre: 1 <= k <= self.length()
    @rtype: AVLNode
    @returns: the smallest node off size >= k
    """

	def subTreeOfSizeK(self, k):
		curr = self.firstItem
		while (curr.getSize() < k):
			curr = curr.getParent()
		return curr

	"""returns the i'th smallest node in the tree
    @type i: int
    @pre: 1 <= i <= self.length()
    @param i: a position in the tree
    @rtype: AVLNode
    @returns: the i'th smallest node in the tree
    """
	def treeSelect(self, i):
		if i == 1:
			return self.firstItem
		if i == self.length():
			return self.lastItem

		curr = self.subTreeOfSizeK(i)
		currSize = curr.getLeft().getSize() + 1
		while (i != currSize):
			if i < currSize:
				curr = curr.getLeft()

			else:
				curr = curr.getRight()
				i = i - currSize
			currSize = curr.getLeft().getSize() + 1
		return curr

	"""returns the successor of a given node
	@type node: AVLNode
	@rtype: AVLNode
	@returns: the successor of a given node. if the node is the Maximum returns None
	"""

	def mySuccessor(self, node):
		if self.lastItem == node:
			return None

        if node.getRight().isRealNode():
            subTree = AVLTreeList()
            subTree.root = node.getRight()
            return subTree.findMin()

        curr = node.getParent()
        while (curr != None) and (curr.getRight() == node):
            node = curr
            curr = curr.getParent()
        return curr

    """returns the predecessor of a given node
    @type node: AVLNode
	@rtype: AVLNode
	@returns: the predecessor of a given node. if the node is the minimum returns None
	"""

	def myPredecessor(self, node):
        if node == self.firstItem:
            return None
        if node.getLeft().isRealNode():
            subTree = AVLTreeList()
            subTree.root = node.getLeft()
            return subTree.findMax()

        curr = node.getParent()
        while (curr != None) and (curr.getLeft() == node):
            curr = curr.getParent
        return curr


	"""
	returns the node which contains the last item in the AVLtreelist. if empty returns None.
	@rtype: AVLNode
	"""

	def findMax(self):
		traveler = self.getRoot()
		if traveler == None:
			return None
		while(traveler.getRight().isRealNode()):
			traveler = traveler.getRight()
		return traveler

	"""
	returns the node which contains the first item in the AVLtreelist. if empty returns None.
	@rtype: AVLNode
	"""

	def findMin(self):
		traveler = self.getRoot()
		if traveler == None:
			return None
		while (traveler.getLeft().isRealNode()):
			traveler = traveler.getLeft()
		return traveler

    """rotates a node with BF = +2 and its left son has BF = +1,
    fixes the Bf of node, updating the height and size fields of the nodes involved
		@type node: AVLNode
        @param node: starting point of rotation
        @rtype : None
        @returns: None
	"""

	def rightRotation(self, node):
        B = node
        parent = B.getParent()
        A = B.getLeft()
        if parent != None:
            if parent.getLeft() == B:
                parent.setLeft(A)
            else:
                parent.setRight(A)
        else:
            self.root = A
        A.setParent(parent)
        B.setParent(A)
        B.setLeft(A.getRight())
        A.setRight(B)
        B.getLeft().setParent(B)

        B.updateHeight()
        A.updateHeight()

        B.updateSize()
        A.updateSize()

    """rotates a node with BF = -2 and its left son has BF = -1,
    fixes the Bf of node, updating the height and size fields of the nodes involved
	    @type node: AVLNode
        @param node: starting point of rotation
        @rtype : None
        @returns: None
	"""

	def leftRotation(self, node):
        B = node
        parent = B.getParent()
        A = B.getRight()
        if parent == None:
            self.root = A
            A.setParent(None)
        else:
            if parent.getLeft() == B:
                parent.completeSetLeft(A)
            else:
                parent.completeSetRight(A)
        B.completeSetRight(A.getLeft())
        A.completeSetLeft(B)

        B.updateHeight()
        A.updateHeight()

        B.updateSize()
        A.updateSize()

		"""performs rotation on AVL subtree with all cases as shown in class
		@type node: AVLNode
		@param node: the root of the AVL subtree
		@rtype : int
		@returns: number of rebalancing operation that has been done
		"""

	def insertCases(node):
		if node.getBf() == -2:
			if node.getRight().getBf() == -1:
				self.leftRotation(node)
				return 1
			else:
				self.rightRotation(node.getRight())
				self.leftRotation(node)
				return 2

		else:
			if node.getLeft().getBf() == 1:
				self.rightRotation(node)
				return 1
			else:
				self.leftRotation(node.getLeft())
				self.rightRotation(node)
				return 2

        """travels from the inserted node to root, updating size and height while traveling.
        @type node: AVLNode
        @param node: inserted node
        @rtype: tuple
        @returns: tuple which its first object is the last node it checked
                 and second object is number of rebalancing operations that has been done
        """

        def fixInsert(node):
            node.updateHeight()
            node.updateSize()
            curr = node.getParent()
            balancer = 0

            while curr != None:
                curr.updateSize()
                prevHeight = curr.getHeight()
                curr.updateHeight()

                if abs(curr.getBf()) < 2:
                    if prevHeight == curr.getHeight():
                        return (curr, balancer)
                    else:
                        curr = curr.getParent()
                        balancer += 1

                else:
                    balancer += insertCases(curr)
                    return (curr, balancer)

            return (curr, balancer)
