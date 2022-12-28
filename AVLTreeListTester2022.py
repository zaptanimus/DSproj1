''' In order to run the tester:
    1.  Make sure your AVLTreeList.py file and AVLTreeListTester2022.py
        file are both in the same directory.
    2.  Run your AVLTreeList.py file
    3.  Run the AVLTreeListTester2022.py file
    4.  Your grade should be written in the terminal.
        Only failed tests will be presented in the terminal,
        together with the AssertionError that made them fail.
        
        
    Note: if you want to see the time each test took, add the following commands:
    1. Add this to def setUp(cls) method - cls.start_time = time.time()
    2. Add this method:
        def tearDown(self):
            t = time.time() - self.start_time
            print("%s: %.3f " % (self.id()[31:], t))
'''
    

import time
import unittest, random
from avl_template_new import AVLTreeList, AVLNode



GRADE = 0
MAX_GRADE = 64
NUMBER_OF_TESTS = 44
PASSED_TESTS = 0


class AVLTreeListTester2022(unittest.TestCase):
 
    ''' We made the is_Tree_AVL test easier in order to ignore mistakes made by wrong
        implemention of getLeft() and getRight() methods.
        In addition, the is_node_valid_rec test does not check validity for virtual nodes,
        meaning we don't care if a virtual node's parent field is valid or not (for example). ''' 

    def is_Tree_AVL(self, tree: AVLTreeList, checkFirstAndLast = True): 
        root = tree.getRoot()
        if root is not None:

            if checkFirstAndLast:
                leftMostNode: AVLNode = root
                while (leftMostNode.getLeft() is not None and leftMostNode.getLeft().isRealNode()):
                    leftMostNode = leftMostNode.getLeft()
                self.assertEqual(leftMostNode.getValue(), tree.first(), "first() doesn't return the value of the first node")
                rightMostNode: AVLNode = root
                while (rightMostNode.getRight() is not None and rightMostNode.getRight().isRealNode()):
                    rightMostNode = rightMostNode.getRight()
                self.assertEqual(rightMostNode.getValue(), tree.last(), "last() doesn't return the value of the last node")

            self.is_node_valid_rec(root)

    def is_node_valid_rec(self, node: AVLNode):
        if node is not None and node.isRealNode():
            if node.getRight() is not None and node.getRight().isRealNode():
                self.assertEqual(node.getRight().getParent(), node, "Right son of node with value " + str(node.getValue()) +
                                                                    " doesn't point to it's parent")
            if node.getLeft() is not None and node.getLeft().isRealNode():
                self.assertEqual(node.getLeft().getParent(), node, "Left son of node with value " + str(node.getValue()) +
                                                                    " doesn't point to it's parent")
            leftHeight = -1 if node.getLeft() is None else node.getLeft().getHeight()
            rightHeight = -1 if node.getRight() is None else node.getRight().getHeight()                                                        
            BF = leftHeight - rightHeight
            self.assertIn(BF, [-1,0,1], "BF of Node with value {} is {}".format(node.getValue(), BF))
            self.assertEqual(node.getHeight(), max(leftHeight,rightHeight) + 1, "Height on node with value " +
                                                                                str(node.getValue()) + " is not correct")

            self.is_node_valid_rec(node.getLeft())
            self.is_node_valid_rec(node.getRight())
  
    
    @staticmethod
    def add_points(x: float, is_the_test_finished = True):
        global GRADE, PASSED_TESTS
        GRADE += x
        if is_the_test_finished:
            PASSED_TESTS += 1


    @staticmethod
    def in_order(tree: AVLTreeList):
        lst = []
        def in_order_rec(node: AVLNode, in_order_lst: list[str]):
            if node is not None and node.isRealNode():
                in_order_rec(node.getLeft(), in_order_lst)
                in_order_lst.append(node.getValue())
                in_order_rec(node.getRight(), in_order_lst)
        in_order_rec(tree.getRoot(), lst)
        return lst


    @classmethod
    def setUp(cls):
        cls.tree = AVLTreeList()
        cls.tree_2 = AVLTreeList()
        #cls.start_time = time.time()
        
    # def tearDown(self):
    #         t = time.time() - self.start_time
    #         print("%s: %.3f " % (self.id()[31:], t))

    @staticmethod
    def create_tree(values, random_order = False, insert_start = False, insert_end = False):
        if random_order: random.shuffle(values)
        tree = AVLTreeList()
        if insert_start:
            for val in values: tree.insert(0,str(val))
        elif insert_end:
            for (i,val) in enumerate(values): tree.insert(i,str(val))
        else:
            for (i,val) in enumerate(values): tree.insert(random.randint(0,i), str(val))
        return tree


    def test_basic_avl_node_get(self):
        self.tree.insert(0,"2")
        self.tree.insert(0,"1") #    '2'
        self.tree.insert(2,"3") # '1'   '3'
        root = self.tree.getRoot()
        #self.assertIsNone(root.getParent(), "FAIL - root's parent should be None") removed this test, could be VirtualNode (implementation decision)
        self.assertTrue(root.isRealNode(), "FAIL - root is a real node")
        self.assertEqual(root.getHeight(), 1)
        self.assertTrue(root.getLeft().isRealNode())
        self.assertTrue(root.getRight().isRealNode())
        self.assertEqual(root.getLeft().getHeight(), 0)
        self.assertEqual(root.getRight().getHeight(), 0)
        self.assertEqual(root.getLeft().getParent(), root)
        self.assertEqual(root.getRight().getParent(), root)
        self.add_points(2)


    def test_empty_tree(self):
        self.assertTrue(self.tree.empty(), "FAIL - tree.empty() on a new tree should return True")
        self.add_points(0.5)
    

    def test_non_empty_tree(self):
        self.tree.insert(0, "test")
        self.assertFalse(self.tree.empty(), "FAIL - tree.empty() on a non-empty tree should return False")
        self.add_points(0.5)


    def test_empty_after_deletion(self):
        T = self.create_tree([str(i) for i in range(20)], random_order=True)
        for i in range(19):
            T.delete(random.randint(0,19 - i))
            self.assertFalse(T.empty(),"FAIL - tree.empty() on a non-empty tree should return False, iteration " + str(i))
        T.delete(0)
        self.assertTrue(T.empty(), "FAIL - tree.empty() on an empty tree should return True")
        self.add_points(1)


    def test_retrieve_linear_insertion(self):
        for i in range(100):
            self.tree.insert(i, str(i))
        for i in range(100):
            self.assertEqual(self.tree.retrieve(i), str(i), "FAIL - iteration {}".format(i))
        self.add_points(1.5)

    
    def test_retrieve_random_insertion(self):
        T = self.create_tree([str(i) for i in range(1000)], random_order=True)
        in_order = self.in_order(T)
        for i,val in enumerate(in_order):
            self.assertEqual(val, T.retrieve(i), "FAIL - iteration {}".format(i))
        self.add_points(1.5)

    
    def test_insert_single_rotation_right(self):
        # This test is based on the AVL lecture from week 3 - page 21 on the pdf file
        self.assertEqual(self.tree.insert(0,"10"), 0, "FAIL - should be no re-balancing op on the first insertion")
        self.assertEqual(self.tree.insert(1,"12"), 1, "FAIL - should be 1 re-balancing op on the second insertion")
        self.assertEqual(self.tree.insert(0,"6"), 0, "FAIL - should be 0 re-balancing op on the third insertion")
        self.assertEqual(self.tree.insert(0,"3"), 2, "FAIL - should be 2 re-balancing op on the fourth insertion")
        self.assertEqual(self.tree.insert(0,"1"), 2, "FAIL - should be 2 re-balancing op on the fifth insertion")
        in_order = self.in_order(self.tree)
        real_order = ["1", "3", "6", "10", "12"]
        self.assertEqual(in_order, real_order, "FAIL - In order traversal: {}\n How it should look like: {}"
                                                                            .format(in_order, real_order))
        self.add_points(1)


    def test_insert_single_rotation_left(self):
        self.tree.insert(0,"0")
        self.tree.insert(1,"1")
        # The above insertions are already tested on another test
        self.assertEqual(self.tree.insert(2,"2"), 2, "FAIL - should be 2 re-balancing op on the third insertion")
        self.assertEqual(self.tree.insert(3,"3"), 2, "FAIL - should be 2 re-balancing op on the fourth insertion")
        self.assertEqual(self.tree.insert(4,"4"), 2, "FAIL - should be 2 re-balancing op on the fifth insertion")
        in_order = self.in_order(self.tree)
        real_order = ["0", "1", "2", "3", "4"]
        self.assertEqual(in_order, real_order, "FAIL - In order traversal: {}\n How it should look like: {}"
                                                                            .format(in_order, real_order))
        self.add_points(1)
             

    def test_insert_double_rotation_RL(self):
        self.tree.insert(0,"2")
        self.assertEqual(self.tree.insert(0,"1"), 1, "FAIL - should be 1 re-balancing op on the second insertion")
        self.assertEqual(self.tree.insert(2,"3"), 0, "FAIL - should be 0 re-balancing op on the third insertion")
        self.assertEqual(self.tree.insert(3,"5"), 2, "FAIL - should be 2 re-balancing op on the fourth insertion")
        self.assertEqual(self.tree.insert(3,"4"), 3, "FAIL - should be 3 re-balancing op on the fifth insertion")
        in_order = self.in_order(self.tree)
        real_order = ["1", "2", "3", "4", "5"]
        self.assertEqual(in_order, real_order, "FAIL - In order traversal: {}\n How it should look like: {}"
                                                                            .format(in_order, real_order))
        self.add_points(1)


    def test_insert_double_rotation_LR(self):
        # This test is based on the AVL lecture from week 3 - page 23 on the pdf file
        self.tree.insert(0,"10")
        self.tree.insert(1,"12")
        self.tree.insert(0,"6")
        self.tree.insert(0,"3")
        # The above insertions are already tested on another test 
        self.assertEqual(self.tree.insert(1,"4"), 3, "FAIL - should be 3 re-balancing op on the fifth insertion")
        in_order = self.in_order(self.tree)
        real_order = ["3", "4", "6", "10", "12"]
        self.assertEqual(in_order, real_order, "FAIL - In order traversal: {}\n How it should look like: {}"
                                                                            .format(in_order, real_order))
        self.add_points(1)


    def test_insert_without_op_count(self):
        python_list = []
        for i in range(5000):
            val = str(i)
            random_index = random.randint(0,i)
            self.tree.insert(random_index, val)
            python_list.insert(random_index, val)
        in_order = self.in_order(self.tree)
        self.assertEqual(in_order, python_list, "FAIL - in order traversal should be identical to the list")
        self.add_points(1.5)


    def test_tree_structure_after_insertions(self):
        T = self.create_tree([str(i) for i in range(2**12)], random_order=True)
        self.is_Tree_AVL(T)
        self.add_points(1.5)


    def test_delete_operations_simple_1(self):
        self.tree.insert(0,"2")
        self.tree.insert(0,"1")
        self.tree.insert(2,"3")
        #   2
        # 1   3
        self.assertEqual(self.tree.delete(0), 0, "FAIL - deleting '1' should cost 0 re-balancing op")
        self.assertEqual(self.tree.delete(1), 1, "FAIL - deleting '3' should cost 1 re-balancing op")
        self.assertEqual(self.tree.delete(0), 0, "FAIL - deleting '2' should cost 0 re-balancing op")
        self.add_points(1)


    def test_delete_operations_simple_2(self):
        # This test is based on the AVL lectrue from week 3 - page 85 on the pdf file
        self.tree.insert(0,"8") ; self.tree.insert(1,"10") ; self.tree.insert(0,"6") ; self.tree.insert(0,"4") ; self.tree.insert(1,"5")
        self.assertEqual(self.tree.delete(4), 1, "FAIL - deleting '10' should cost 1 re-balancing op") 
        in_order = self.in_order(self.tree)
        real_order = ["4", "5", "6", "8"]
        self.assertEqual(in_order, real_order, "FAIL - In order traversal: {}\nHow it should look like: {}"
                                                                            .format(in_order, real_order))
        self.add_points(1)


    def test_delete_operations_simple_3(self):
        T = AVLTreeList()
        T.insert(0,"4") ; T.insert(1,"6") ; T.insert(0,"2") ; T.insert(0,"1")
        T.insert(2,"3") ; T.insert(4,"5") ; T.insert(6,"7")
    #                    '4'
    #                '2'     '6'
    #              '1' '3' '5' '7'
        self.assertEqual(T.delete(2), 0, "FAIL - 1st assertion")
        self.assertEqual(T.delete(0), 1, "FAIL - 2nd assertion")
        self.assertEqual(T.delete(0), 1, "FAIL - 3rd assertion")
        self.assertEqual(T.delete(0), 1, "FAIL - 4th assertion")
        self.assertIn(T.delete(1), [0,1], "FAIL - 5th assertion") #Ease the test
        self.assertEqual(T.delete(0), 1, "FAIL - 6th assertion")
        self.assertEqual(T.delete(0), 0, "FAIL - 7th assertion")
        self.add_points(1.5,False)
        self.assertTrue(T.empty(), "FAIL - 8th assertion")
        self.add_points(0.5)

    def test_delete_root(self):
        T = self.create_tree([str(i) for i in range(100)])
        in_order = self.in_order(T)
        for i in range(10):
            root_index = in_order.index(T.getRoot().getValue())
            in_order.pop(root_index)
            T.delete(root_index)
            self.assertEqual(self.in_order(T), in_order)
            
        self.add_points(1.5)


    def test_in_order_after_deletions(self):
        python_list = []
        for i in range(100):
            val = str(random.randint(0,10000))
            random_index = random.randint(0,i)
            python_list.insert(random_index, val)
            self.tree.insert(random_index, val)
        for i in range(99): #Not checking edge case
            random_index = random.randint(0, 99 - i)
            python_list.pop(random_index)
            self.tree.delete(random_index)
            in_order = self.in_order(self.tree)
            self.assertEqual(in_order, python_list, "FAIL - In order traversal: \n{}\nHow it should look like: \n{}\
                                                    \nIteration: {}".format(in_order, python_list,i))
        self.add_points(2.5)


    def test_delete_first_and_last(self):
        for i in range(100):
            self.tree.insert(0,str(i))
            self.tree_2.insert(0,str(i))
            self.assertEqual(self.tree.first(), str(i), "FAIL - iteration {}, first for loop".format(i))
            self.assertEqual(self.tree.last(), "0", "FAIL - iteration {}, first for loop".format(i))

        real_length = 100
        for i in range(99):
            self.tree.delete(0)
            self.tree_2.delete(real_length - 1)
            self.assertEqual(self.tree.first(), str(99 - i - 1), "FAIL - iteration {}, second for loop".format(i))
            self.assertEqual(self.tree.last(), "0", "FAIL - iteration {}, second for loop".format(i))
            self.assertEqual(self.tree_2.first(), "99", "FAIL - iteration {}, second for loop".format(i))
            self.assertEqual(self.tree_2.last(), str(i + 1), "FAIL - iteration {}, second for loop".format(i))
            real_length -= 1
            self.is_Tree_AVL(self.tree)
            self.is_Tree_AVL(self.tree_2)

        self.add_points(2)
        
    
    def test_first_and_last_empty(self):
        self.assertIsNone(self.tree.first(), "FAIL - first() should return None on an empty tree")
        self.assertIsNone(self.tree.last(), "FAIL - last() should return None on an empty tree")
        self.tree.insert(0,"Not None")
        self.assertIsNotNone(self.tree.first(), "FAIL - first() should not return None on an non-empty tree")
        self.assertIsNotNone(self.tree.last(), "FAIL - first() should not return None on an non-empty tree")
        self.add_points(1)


    def test_first(self):
        for i in range(1000,2000):
            self.tree.insert(i - 1000, str(i))
            self.assertEqual(self.tree.first(), "1000", "FAIL - first() should return '1000', iteration {}".format(i))
        for i in range (500,1000):
            self.tree.insert(0,str(i))
            self.assertEqual(self.tree.first(), str(i), "FAIL - first() should return '{}', iteration {}".format(i,i))
        self.add_points(1)

    
    def test_last(self):
        for i in range(1000,2000):
            self.tree.insert(i - 1000, str(i))
            self.assertEqual(self.tree.last(), str(i), "FAIL - last() should return '{}', iteration {}".format(i,i))
        for i in range(500,1000):
            self.tree.insert(i,str(i))
            self.assertEqual(self.tree.last(), "1999", "FAIL - last() should return '1999', iteration {}".format(i))
        self.add_points(1)


    def test_first_and_last_with_length(self):
        for i in range(10):
            self.tree.insert(0, str(i))
            for j in range(i * 10 + 1, i * 10 + 10):
                self.tree.insert(self.tree.length(), str(j))
            self.assertEqual(self.tree.first(), str(i), "FAIL - tree.first() should return '{}'".format(i))
            self.assertEqual(self.tree.last(), str(i*10 + 9), "FAIL - tree.last() should return '{}'".format(i*10 + 9))
        self.add_points(2)


    def test_list_to_array_empty(self):
        self.assertEqual(self.tree.listToArray(), [], "FAIL - listToArray() should return [] for an empty tree")
        self.tree.insert(0,"1")
        self.assertNotEqual(self.tree.listToArray(), [], "FAIL - listToArray() should not return [] for a non-empty tree")
        self.add_points(1)


    def test_list_to_array_identical_vals(self):
        lst = [str(i//10) for i in range(1000)]
        random.shuffle(lst)
        T = self.create_tree(lst,insert_end=True)
        self.assertEqual(lst,T.listToArray(), "FAIL - listToArray() is not consistent with the insertion order provided")
        self.add_points(1)


    def test_list_to_array(self):
        origSentence = "My mom always said life was like a box of chocolates. You never know what you're gonna get."
        length = 0
        for ch in origSentence:
            self.tree.insert(length,ch)
            length += 1
        AVLList = self.tree.listToArray()
        treeSentence = "".join(AVLList)
        self.assertEqual(origSentence,treeSentence,"FAIL - the listToArray method creates the sentence:\n'{}'".format(treeSentence))
        self.add_points(1,False)
        for ch in reversed(origSentence):
            self.tree_2.insert(0,ch)
        AVLList = self.tree_2.listToArray()
        treeSentence = "".join(AVLList)
        self.assertEqual(origSentence,treeSentence,"FAIL - the listToArray method creates the sentence:\n{}".format(treeSentence))
        self.add_points(1)


    def test_list_to_array_random(self):
        python_list = []
        length = 0
        for i in range(10):
            for j in range(10):
                randomIndex = random.randint(0,length)
                randomValue = str(random.randint(0,1000))
                python_list.insert(randomIndex,randomValue)
                self.tree.insert(randomIndex,randomValue)
                length += 1
            AVLList = self.tree.listToArray()
            self.assertEqual(python_list, AVLList, "FAIL - \nPython list: {}\nAVLTreeList: {}".format(python_list,AVLList))
        self.add_points(2)


    def test_list_to_array_is_in_order(self):
        T = self.create_tree([str(random.randint(0,10000)) for i in range(1000)])
        in_order = self.in_order(T)
        self.assertEqual(in_order, T.listToArray(), "FAIL - in order traversal should be identical to listToArray()")
        self.add_points(1)


    def test_length_of_empty_tree(self):
        self.assertEqual(self.tree.length(), 0, "FAIL - tree.length() on an empty tree should return 0")
        self.tree.insert(0,"")
        self.assertNotEqual(self.tree.length(), 0, "FAIL - tree.length() on a non-empty tree should not return 0")
        self.add_points(1)
    

    def test_length_after_insert(self):
        length = 0
        for i in range(10):
            self.tree.insert(0,"First")
            length += 1
            self.assertEqual(length, self.tree.length(), "FAIL - Length error, first loop, iteration {}".format(str(i)))
        for i in range(10):
            self.tree.insert(10,"Last")
            length += 1
            self.assertEqual(length, self.tree.length(), "FAIL - Length error, second loop, iteration {}".format(str(i)))
        for i in range(1000):
            self.tree.insert(random.randint(0, length), "Rand")
            length += 1
            self.assertEqual(length, self.tree.length(), "FAIL - Length error, third loop, iteration {}".format(str(i)))
        self.add_points(2)


    def test_length_after_delete(self):
        for i in range(1000):
            self.tree.insert(random.randint(0,i),"test length")
        for j in range(999):
            self.tree.delete(random.randint(0,999-j))
            self.assertEqual(self.tree.length(), 999 - j, "FAIL - Length error")
        self.add_points(1, False)
        self.tree.delete(0)
        self.assertEqual(self.tree.length(), 0, "FAIL - Length error after deleting all the nodes from the list")
        self.add_points(1)



    def verify_concat(self, tree_1: AVLTreeList, tree_2: AVLTreeList):
        real_list = self.in_order(tree_1) + self.in_order(tree_2)
        tree_1_first = tree_1.first()
        tree_2_last = tree_1.last() if tree_2.empty() else tree_2.last()
        height_diff = self.calc_height_diff(self.tree, self.tree_2)
        returned_value = self.tree.concat(self.tree_2)
        self.assertEqual(returned_value, height_diff, "FAIL - concat returned {} when it should have return {}" \
                                                        .format(returned_value, height_diff))
        self.assertEqual(self.in_order(tree_1), real_list)
        self.assertEqual(tree_1.first(), tree_1_first, "FAIL - problem with first()")
        self.assertEqual(tree_1.last(), tree_2_last, "FAIL - problem with last()")
        self.assertEqual(tree_1.length(), len(real_list), "FAIL - problem with length()")
        self.is_Tree_AVL(tree_1)


    def calc_height_diff(self, tree_1: AVLTreeList, tree_2: AVLTreeList):
        if tree_1.empty() and tree_2.empty(): return 0
        elif tree_1.empty(): return tree_2.getRoot().getHeight() + 1
        elif tree_2.empty(): return tree_1.getRoot().getHeight() + 1
        return abs(tree_1.getRoot().getHeight() - tree_2.getRoot().getHeight())


    def test_concat_operations(self):
        trees = [AVLTreeList() for i in range(4)]
        for i in range(1000):
            random_index = random.randint(0,i)
            trees[0].insert(random_index, str(i))
            trees[1].insert(random_index, str(i))
        for i in range(50):
            random_index = random.randint(0,i)
            trees[2].insert(random_index, str(i))
            trees[3].insert(random_index, str(i))
        
        height_diff = self.calc_height_diff(trees[0],trees[2])
        self.assertEqual(height_diff, trees[0].concat(trees[2]))
        self.assertEqual(height_diff, trees[3].concat(trees[1]))
        self.add_points(1)


    def test_concat_simple(self):
        sentence = "The quick brown fox jumps over a lazy dog."
        first_part = sentence[0:16] ; second_part = sentence[16:]
        for i,letter in enumerate(first_part):
            self.tree.insert(i, letter)
        for i,letter in enumerate(second_part):
            self.tree_2.insert(i, letter)
        self.verify_concat(self.tree, self.tree_2)
        self.add_points(2)


    def test_concat_empty_tree(self):
        T = self.create_tree([str(i) for i in range(100)], random_order=True)
        empty_tree = AVLTreeList()
        before_concat_in_order = self.in_order(T) ; before_concat_length = T.length()
        before_concat_first = T.first() ; before_concat_last = T.last()
        height_diff = self.calc_height_diff(T, empty_tree)
        concat_ret_value = T.concat(empty_tree)
        after_concat_in_order = self.in_order(T) ; after_concat_length = T.length()
        after_concat_first = T.first() ; after_concat_last = T.last()
        self.assertEqual(before_concat_in_order, after_concat_in_order, "FAIL - in order traversal should be equal "\
                                                                        "before and after concatenating an empty tree")
        self.assertEqual(before_concat_length, after_concat_length, "FAIL - length should be equal before and after "\
                                                                        "concatenating an empty tree")
        self.assertEqual(before_concat_first, after_concat_first, "FAIL - first should be equal before and after "\
                                                                        "concatenating an empty tree")
        self.assertEqual(before_concat_last, after_concat_last, "FAIL - last should be equal before and after "\
                                                                        "concatenating an empty tree")
        self.assertEqual(height_diff, concat_ret_value)                                                                 
        self.add_points(1)


    def test_concat_to_empty_tree(self):
        T = self.create_tree([str(i) for i in range(100)], random_order=True)
        empty_tree = AVLTreeList()
        before_concat_in_order = self.in_order(T) ; before_concat_length = T.length()
        before_concat_first = T.first() ; before_concat_last = T.last()
        height_diff = self.calc_height_diff(T, empty_tree)
        concat_ret_value = empty_tree.concat(T)
        after_concat_in_order = self.in_order(empty_tree) ; after_concat_length = empty_tree.length()
        after_concat_first = empty_tree.first() ; after_concat_last = empty_tree.last()
        self.assertEqual(before_concat_in_order, after_concat_in_order, "FAIL - in order traversal should be equal " \
                                                                        "before and after concatenating to an empty tree")
        self.assertEqual(before_concat_length, after_concat_length, "FAIL - length should be equal before and after "\
                                                                        "concatenating to an empty tree")
        self.assertEqual(before_concat_first, after_concat_first, "FAIL - first should be equal before and after "\
                                                                        "concatenating to an empty tree")
        self.assertEqual(before_concat_last, after_concat_last, "FAIL - last should be equal before and after "\
                                                                        "concatenating to an empty tree")
        self.assertEqual(height_diff, concat_ret_value)                                                                 
        self.add_points(1)

    
    def test_concat_many_lists(self):
        list_of_trees = [self.create_tree([str(i) for i in range(100*j, 100*(j+1))],random_order=True) for j in range(10)]
        in_order_all = self.in_order(list_of_trees[0])
        final_tree = list_of_trees[0]
        for tree in list_of_trees[1:]:
            in_order_all.extend(self.in_order(tree))
            height_diff = self.calc_height_diff(final_tree,tree)
            self.assertEqual(x:=final_tree.concat(tree), height_diff, "FAIL - concat returned {} when it should have return {}" \
                                                                    .format(x, height_diff))
            self.is_Tree_AVL(final_tree)
        in_order_after_concat = self.in_order(final_tree)
        self.assertEqual(in_order_all, in_order_after_concat)
        self.add_points(3)



    def test_non_succesful_search(self):
        self.assertEqual(self.tree.search("test"), -1, "FAIL - tree.search() on an empty tree should return -1")
        for i in range(10):
            self.tree.insert(0, str(i))
        self.assertEqual(self.tree.search("10"), -1, "FAIL - tree.search() should return -1 " \
                                                        "whenever val is not in the tree")
        self.add_points(1)
    
    
    def test_search_first_index(self):
        for i in range(100):
            self.tree.insert(i,str(i))
        self.assertEqual(self.tree.search("47"),47)
        self.tree.insert(13,"47")
        self.assertEqual(self.tree.search("47"),13)
        self.add_points(1)
    

    def test_search_complex(self):
        N = 100
        T = self.create_tree([str(i) for i in range(N)],random_order=True)
        in_order = self.in_order(T)
        lst = ['0' for i in range(N)]
        for i in range(N):
            lst[T.search(str(i))] = str(i)
        self.assertEqual(in_order,lst)
        self.add_points(2)

    
    def test_search_after_delete(self):
        N = 100
        T = self.create_tree([str(i) for i in range(N)], random_order=True)
        for i in range(N):
            self.assertNotEqual(T.search(str(i)), -1, "FAIL - search should return -1 iff str({}) is not in the tree".format(i))
            T.delete(T.search(str(i)))
            self.assertEqual(T.search(str(i)), -1, "FAIL - search should return -1 iff str({}) is not in the tree".format(i))
        self.add_points(2)


    @classmethod
    def tearDownClass(self):
        super()
        print("\n\n")
        print("======================================================================")
        print("===========                 Tester Results:                ===========")
        print("======================================================================")
        print("                         # Of Tests: {}             ".format(NUMBER_OF_TESTS))
        print("                         # of Successful Tests: {}            ".format(PASSED_TESTS))
        print("                         # of Failed Tests: {}            ".format(NUMBER_OF_TESTS - PASSED_TESTS))
        print("                         The Final Grade is:              ")
        print("\n                          {} out of {}               ".format(round(GRADE,1), MAX_GRADE))
        print("======================================================================")
        print("\n\n")


if __name__ == '__main__':
    unittest.main(verbosity = 1)
    #Change verbosity = 0 or verbosity = 2 for less/more details from tests

    