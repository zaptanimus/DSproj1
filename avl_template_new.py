#username - yaronreunbeni
#id1      - 208935312
#name1    - Yaron Reuben Ittah
#id2      - complete info
#name2    - complete info

import random

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

	"""returns the size of node

	@rtype: int
	@returns: the size of self, 0 if the node is virtual
	"""
	def getSizeNode(self):
		return self.sizeNode

	"""calculate the BF of the current node 

	@rtype: int
	@returns: the balance factor of the node.
	"""
	def getBF(self):
		return self.left.getHeight() - self.right.getHeight()

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

	"""sets the height of the node

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

	""" updates node height by computing it from childrens' height
	"""
	def updateHeight(self):
		self.setHeight(max(self.getRight().getHeight(), self.getLeft().getHeight()) + 1)

	"""updates node size by computing it from childrens' size
	"""
	def updateSize(self):
		self.setSize(self.getRight().getSizeNode() + self.getLeft().getSizeNode() + 1)

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
					self.insertLeaf(self.findMin(), node, "left")
				else:
					self.insertLeaf(self.firstItem, node, "left")
					self.firstItem = node

		elif i == self.length():
			if self.lastItem == None:
				self.insertLeaf(self.findMax(), node, "right")
			else:
				self.insertLeaf(self.lastItem, node, "right")
				self.lastItem = node

		else:
			curr = self.treeSelect(i+1)
			if not curr.getLeft().isRealNode():
				self.insertLeaf(curr, node, "left")
			else:
				self.insertLeaf(self.myPredecessor(curr), node, "right")

		curr, balance = self.fixInsert(node)
		if curr != None:
			self.fixSizeUp(curr.getParent())

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
		def recListToArray(node, arr):
			if node.isRealNode():
				recListToArray(node.getLeft(), arr)
				arr.append(node.getValue())
				recListToArray(node.getRight(), arr)
		
		arr = []
		recListToArray(self.getRoot(),arr)
		return arr

	"""returns the size of the list 

	@rtype: int
	@returns: the size of the list
	"""
	def length(self):
		if self.empty():
			return 0
		return self.getRoot().getSizeNode()

	"""sort the info values of the list

	@rtype: list
	@returns: an AVLTreeList where the values are sorted by the info of the original list.
	"""
	def sort(self):
		sortT = AVLTreeList()
		arr = self.listToArray
		myHeapSort(arr)
		for i in range(len(arr)):
			sortT.insert(i,arr[i])
		return sortT

	"""permute the info values of the list 

	@rtype: list
	@returns: an AVLTreeList where the values are permuted randomly by the info of the original list. ##Use Randomness
	"""
	def permutation(self):
		permT = AVLTreeList()
		arr = self.listToArray
		random.shuffle(arr)
		for i in range(len(arr)):
			permT.insert(i,arr[i])
		return permT

	"""concatenates lst to self

	@type lst: AVLTreeList
	@param lst: a list to be concatenated after self
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""
	def concat(self, lst):
		deltaHeight = abs(self.getTreeHeight() - lst.getTreeHeight())
		if self.empty():
			self.root = lst.getRoot()
			self.firstItem = lst.firstItem
			self.lastItem = lst.lastItem
		else:
			selfMaxi = self.lastItem
			self.delete(self.length()-1)
			self.join(selfMaxi, lst)
		return deltaHeight

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
		while (curr.getSizeNode() < k):
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
		currSize = curr.getLeft().getSizeNode() + 1
		while (i != currSize):
			if i < currSize:
				curr = curr.getLeft()

			else:
				curr = curr.getRight()
				i = i - currSize
			currSize = curr.getLeft().getSizeNode() + 1
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

	"""returns the node which contains the last item in the AVLtreelist.
	if empty returns None.
	@rtype: AVLNode
	"""
	def findMax(self):
		traveler = self.getRoot()
		if traveler == None:
			return None
		while(traveler.getRight().isRealNode()):
			traveler = traveler.getRight()
		return traveler

	"""	returns the node which contains the first item in the AVLtreelist.
	if empty returns None.
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
				parent.setLeftParent(A)
			else:
				parent.setRightParent(A)
		B.setRightParent(A.getLeft())
		A.setLeftParent(B)

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

	"""performs rotation on AVL criminal subtree so that self will be legal AVL tree
		@type node: AVLNode
		@param node: the root of the AVL criminal subtree
		@rtype : int
		@returns: number of rebalancing operation that has been done
	"""
	def insertCases(self, node):
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
	def fixInsert(self, node):
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
					balancer += self.insertCases(curr)
					return (curr, balancer)

			return (curr, balancer)

	"""inserts node as a leaf without making any height or size adjustments.
	the adjustments will be done in insert function
	@type currLeaf: AVLNode
	@param currLeaf: the leaf that we want to insert a new son to
	@type newLeaf: AVLNode
	@param newLeaf: the node that we want to insert as a new leaf
	@type direction: string
	@param direction: indicates if newLeaf will be the left or right son of currLeaf
	@pre: direction = "left" or direction = "right"
	"""
	def insertLeaf(self,currLeaf, newLeaf, direction):
		if direction == "right":  # insert newLeaf as right son of currLeaf
			virtualSon = currLeaf.getRight()
			currLeaf.setRightParent(newLeaf)
		else:  # insert newLeaf as left son of currLeaf
			virtualSon = currLeaf.getLeft()
			currLeaf.setLeftParent(newLeaf)

		newLeaf.setRightParent(virtualSon)
		newLeaf.setLeftParent(AVLNode())

	"""	updating the size of all the nodes which are in the path from node to the root
	@type node: AVLNode
	"""
	def fixSizeUp(self, node):
		while (node != None):
			node.updateSize()
			node = node.getParent()

	"""	returns the height of the tree, -1 if empty
	@rtype: int
	"""
	def getTreeHeight(self):
		if self.empty():
			return -1
		else:
			return self.getRoot().getHeight()

	"""	inserts val at the end of the list
	@param val: the value we insert to the end of the list
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	@complexity: O(logn)
	"""
	def append(self, val):
		return self.insert(self.length(), val)

	"""
	travels from the parent of the deleted node or the parent of the connector to tree's root, 
	while looking for criminal AVL subtrees and handling the criminals by preforming the rotations needed.
	for every node in the path to the root, it updates its size and height, if needed.
	returns the number of rebalancing operation due to AVL rebalancing.
	
	@type node: AVLNode
	@param node: the parent of the deleted node or the parent of the connector
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing.
	@complexity: O(h1 - h2 + 1) = O(logn) when h1 is the tree height and h2 is the height of node.
	"""
	def fixTreeUp(self, node):
		fixFlag = False
		balancingCntr = 0
		while node != None:
			originalParent = node.getParent()
			node.updateSize()
			if not fixFlag:
				BF = node.getBf()
				heightBefore = node.getHeight()
				node.updateHeight()
				heightAfter = node.getHeight()
				if abs(BF) < 2 and heightAfter == heightBefore:
					fixFlag = True

				elif abs(BF) < 2 and heightAfter != heightBefore:
					balancingCntr += 1
				else:  # abs(BF) = 2
					if BF == 2:
						BFL = node.getLeft().getBf()
						if BFL == 1 or BFL == 0:
							self.rightRotation(node)
							balancingCntr += 1
						elif BFL == - 1:
							self.leftRotation(node.getLeft())
							self.rightRotation(node)
							balancingCntr += 2
					else:  # BF = -2
						BFR = node.getRight().getBf()
						if BFR == -1 or BFR == 0:
							self.leftRotation(node)
							balancingCntr += 1
						elif BFR == 1:
							self.rightRotation(node.getRight())
							self.leftRotation(node)
							balancingCntr += 2

			node = originalParent

		return balancingCntr

	"""merges two AVL trees as shown in class
	@type connector: AVL node
	@type T2: AVL tree
	@pre connector.isRealNode()
	@complexity: O(abs(self.getTreeHeight() - L2.getTreeHeight()) + 1)
	"""
	def join(self, connector, T2):
		if T2.empty():
			self.append(connector.getValue())
			return
		elif self.empty():
			T2.insert(0, connector.getValue())
			self.firstItem = T2.firstItem
			self.lastItem = T2.lastItem
			self.root = T2.getRoot()
			return

		elif self.getRoot().getHeight() == T2.getRoot().getHeight():
			connector.setLeftParent(self.getRoot())
			connector.setRightParent(T2.getRoot())
			connector.setParent(None)
			self.root = connector

		elif self.getRoot().getHeight() < T2.getRoot().getHeight():
			curr = T2.getRoot()
			while curr.getHeight() > self.getRoot().getHeight():
				curr = curr.getLeft()
			currParent = curr.getParent()
			connector.setLeftParent(self.getRoot())
			connector.setRightParent(curr)
			currParent.setLeftParent(connector)
			self.root = T2.getRoot()

		else:
			curr = self.getRoot()
			while curr.getHeight() > T2.getRoot().getHeight():
				curr = curr.getRight()
			currParent = curr.getParent()
			connector.setLeftParent(curr)
			connector.setRightParent(T2.getRoot())
			currParent.setRightParent(connector)
		self.lastItem = T2.lastItem
		connector.updateSize()
		connector.updateHeight()
		if self.getRoot() != connector:
			self.fixTreeUp(connector.getParent())

### PRINT TREE FUNCTIONS ###

	def printt(self):
		out = ""
		for row in self.printree(self.root):  # need printree.py file
			out = out + row + "\n"
		print(out)

	def printree(self, t, bykey=True):
		"""Print a textual representation of t
		bykey=True: show keys instead of values"""
		# for row in trepr(t, bykey):
		#        print(row)
		return self.trepr(t, False)

	def trepr(self, t, bykey=False):
		"""Return a list of textual representations of the levels in t
		bykey=True: show keys instead of values"""
		if t == None:
			return ["#"]

		thistr = str(t.key) if bykey else str(t.getValue())

		return self.conc(self.trepr(t.left, bykey), thistr, self.trepr(t.right, bykey))

	def conc(self, left, root, right):
		"""Return a concatenation of textual represantations of
		a root node, its left node, and its right node
		root is a string, and left and right are lists of strings"""

		lwid = len(left[-1])
		rwid = len(right[-1])
		rootwid = len(root)

		result = [(lwid+1)*" " + root + (rwid+1)*" "]

		ls = self.leftspace(left[0])
		rs = self.rightspace(right[0])
		result.append(ls*" " + (lwid-ls)*"_" + "/" + rootwid *
					" " + "\\" + rs*"_" + (rwid-rs)*" ")

		for i in range(max(len(left), len(right))):
			row = ""
			if i < len(left):
				row += left[i]
			else:
				row += lwid*" "

			row += (rootwid+2)*" "

			if i < len(right):
				row += right[i]
			else:
				row += rwid*" "

			result.append(row)

		return result

	def leftspace(self, row):
		"""helper for conc"""
		# row is the first row of a left node
		# returns the index of where the second whitespace starts
		i = len(row)-1
		while row[i] == " ":
			i -= 1
		return i+1

	def rightspace(self, row):
		"""helper for conc"""
		# row is the first row of a right node
		# returns the index of where the first whitespace ends
		i = 0
		while row[i] == " ":
			i += 1
		return i


"""Heapsort algorithm using heapify as shown in class
@type arr: array
@complexity: O(n log n)
"""
def myHeapSort(arr):
	def myHeapify(arr, N, i):
		largest = i
		l = 2 * i + 1
		r = 2 * i + 2
	
		if l < N and arr[largest] < arr[l]:
			largest = l
		
		if r < N and arr[largest] < arr[r]:
			largest = r
	
		if largest != i:
			arr[i], arr[largest] = arr[largest], arr[i]  # swap
			myHeapify(arr, N, largest)

	N = len(arr)

	for i in range(N//2 - 1, -1, -1):
		myHeapify(arr, N, i)

	for i in range(N-1, 0, -1):
		arr[i], arr[0] = arr[0], arr[i]  # swap
		myHeapify(arr, i, 0)

			