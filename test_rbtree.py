import unittest
from RBtree import Node, RBTree


class TestTST(unittest.TestCase):
    """
    def test_geeksforgeeks(self):
        t = TernarySearchTree()
        t.insert("cat")
        t.insert("cats")
        t.insert("up")
        t.insert("bug")
        # expect = "bug,cat,cats,up"
        # self.assertEqual(expect, str(t))
        self.assertEqual(True, t.search("cats"))
        self.assertEqual(False, t.search("bu"))
        self.assertEqual(True, t.search("cat"))
    """

    def test_insert_example1(self):
        rbtree = RBTree()
        rbtree.insert(Node(50))
        rbtree.insert(Node(20))
        rbtree.insert(Node(70))
        rbtree.insert(Node(10))
        rbtree.insert(Node(40))
        rbtree.insert(Node(60))
        rbtree.insert(Node(80))
        rbtree.insert(Node(30))
        self.assertEqual(rbtree.traverse(), [
            '10b', '20r', '30r', '40b', '50b', '60r', '70b', '80r'])
        rbtree.insert(Node(75))
        self.assertEqual(rbtree.traverse(), [
            '10b', '20r', '30r', '40b', '50b', '60b', '70r', '75r', '80b'])

        rbtree.insert(Node(25))
        # 30r -> 30b
        self.assertEqual(rbtree.traverse(), [
            '10b', '20r', '25r', '30b', '40r', '50b', '60b', '70r', '75r', '80b'])

    def test_insert_example2(self):
        rbtree = RBTree()
        rbtree.insert(Node(11))
        rbtree.insert(Node(2))
        rbtree.insert(Node(14))
        rbtree.insert(Node(1))
        rbtree.insert(Node(7))
        rbtree.insert(Node(15))
        rbtree.insert(Node(5))
        rbtree.insert(Node(8))
        self.assertEqual(rbtree.traverse(), [
          '1b', '2r', '5r', '7b', '8r', '11b', '14b', '15r'])

        rbtree.insert(Node(4))
        self.assertEqual(rbtree.traverse(), [
          '1b', '2r', '4r', '5b', '7b', '8b', '11r', '14b', '15r'])

    def test_delete_example1(self):
        rbtree = RBTree()
        for i in [36, 16, 41, 4, 22, 39, 48, 3, 9,
                  19, 27, 45, 52, 1, 7, 10, 24, 51, 55]:
            rbtree.insert(Node(i))

        for i in [1, 7, 10, 24, 51, 55]:
            rbtree.delete(i)
        self.assertEqual(rbtree.traverse(), [
          '3b', '4r', '9b', '16b', '19b', '22r',
          '27b', '36b', '39b', '41b', '45b', '48r', '52b'])
        rbtree.delete(48)
        self.assertEqual(rbtree.traverse(), [
          '3b', '4r', '9b', '16b', '19b', '22r',
          '27b', '36b', '39b', '41b', '45r', '52b'])

        rbtree.delete(36)
        self.assertEqual(rbtree.traverse(), [
          '3b', '4r', '9b', '16b', '19b', '22r',
          '27b', '39b', '41b', '45b', '52b'])
    

if __name__ == '__main__':
    unittest.main()
