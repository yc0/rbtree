"""
Red Black Tree
Introduction to Algorithms (Cormen, Leiserson, Rivest), Chapter 14.

ref:
http://www.hashcollision.org/hkn/python/red_black/red_black.py
http://www.geeksforgeeks.org/red-black-tree-set-1-introduction-2/
http://alrightchiu.github.io/SecondRound/red-black-tree-deleteshan-chu-zi-liao-yu-fixupxiu-zheng.html



1) Every node has a color either red or black.
2) Root of tree and NIL of tree are always black
3) There are no two adjacent red nodes
  (A red node cannot have a red parent or red child).
4) Every path from root to a NULL node has same number of black nodes.
"""

"""Each node can be colored RED or BLACK."""
RED = "RED"
BLACK = "BLACK"


class NilNode(object):
    def __init__(self):
        self.color = BLACK


"""We define NIL to be the leaf sentinel of our tree."""
NIL = NilNode()


class Node(object):
    def __init__(self, val, color=RED, left=NIL, right=NIL, parent=NIL):
        self.val = val
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent

    def dup(self, n):
        self.val = n.val
        # self.color = n.color
        # self.parent = n.parent
        # self.right = n.right
        # self.left = n.left

    def __repr__(self):
        return str(self.val) + ("b" if self.color == BLACK else "r")


class RBTree(object):
    def __init__(self, root=NIL):
        self.root = root

    def left_rotate(self, x):
        """Left-rotates node x on tree T.

                   x
                  / \
                 a   y
                    / \
                   b   g

        mutates into:

                   y
                  / \
                 x   g
                / \
               a   b

        Used for maintaining tree balance.
        """
        assert(x.right != NIL)
        y = x.right
        x.right = y.left

        if y.left != NIL:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == NIL:
            self.root = y
        elif x.parent.left == x:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        """Right-rotates node x on tree T.

                   x
                  / \
                 y   g
                / \
               a   b

        mutates into:

                   y
                  / \
                 a   x
                    / \
                   b   g

        Used for maintaining tree balance.
        """
        assert(x.left != NIL)
        y = x.left

        x.left = y.right

        if y.right != NIL:
            y.right.parent = x

        y.parent = x.parent

        if x.parent == NIL:
            self.root = y

        elif x.parent.left == x:
            x.parent.left = y

        else:
            x.parent.right = y

        y.right = x
        x.parent = y

    def insert(self, z):
        """Inserts node 'z' into binary tree 'tree'."""
        x, p = self.root, NIL
        while x != NIL:
            p = x
            if z.val < x.val:
                x = x.left
            else:
                x = x.right

        z.parent = p
        if p == NIL:
            self.root = z
        elif z.val < p.val:
            p.left = z
        else:
            p.right = z
        self._insertFixedUpRBT(z)

    def _insertFixedUpRBT(self, current):
        while current.parent.color == RED:
            # current.parent would not be black one,
            # as the result of the Theorem that Root black node
            if current.parent == current.parent.parent.left:
                # precedessor is grandfather left-child. so uncle would be
                # right-child of grandfather
                uncle = current.parent.parent.right
                if uncle.color == RED:
                    # case 1:) uncle is also red node
                    current.parent.color = BLACK
                    uncle.color = BLACK

                    current.parent.parent.color = RED
                    current = current.parent.parent
                else:
                    # case 2) or 3) uncle is black node
                    if current.parent.right == current:
                        # case 2), than we transform into case 3)
                        current = current.parent
                        self.left_rotate(current)

                    # case 3)
                    current.parent.color = BLACK
                    current.parent.parent.color = RED
                    self.right_rotate(current.parent.parent)

            else:
                uncle = current.parent.parent.left

                if uncle.color == RED:
                    # case 1:) uncle is also red node
                    current.parent.color = BLACK
                    uncle.color = BLACK

                    current.parent.parent.color = RED
                    current = current.parent.parent
                else:
                    # case 2) or 3) uncle is black node
                    if current.parent.left == current:
                        # case 2), than we transform into case 3)
                        current = current.parent
                        self.right_rotate(current)

                    # case 3)
                    current.parent.color = BLACK
                    current.parent.parent.color = RED
                    self.left_rotate(current.parent.parent)
        self.root.color = BLACK  # make sure the root would be Black node

    def search(self, val):
        cur = self.root
        while cur != NIL and cur.val != val:
            if val < cur.val:
                cur = cur.left
            else:
                cur = cur.right
        return cur

    def t_min(self, x):
        """ Return the minimal element of the subtree rooted at 'x'. """
        cur = x
        while cur.left != NIL:
            cur = cur.left
        return cur

    def t_max(self, x):
        """Return the maximum element of the subtree rooted at 'x' """
        cur = x
        while cur.right != NIL:
            cur = cur.right
        return cur

    def predecessor(self, x):
        """Returns the inorder predecessor of node 'x'."""
        if x.left != NIL:
            return self.t_max(x.left)
        p, cur = x.parent, x
        while p != NIL and p.left == cur:
            cur, p = p, p.parent
        return p

    def successor(self, x):
        """Returns the inorder successor of node 'x'."""
        if x.right != NIL:
            return self.t_min(x.right)
        p, cur = x.parent, x
        while p != NIL and p.right == cur:
            cur, p = p, p.parent
        return p

    def _deleteFixedUpRBT(self, current):
        print("fixedup=> current:", current, "sibling:", current.parent.left
              if current.parent.left == current
              else current.parent.right)
        while current != self.root and current.color != RED:
            """case 0) root or current is RED, change its color to BLACK"""
            if current == current.parent.left:
                # left child
                sibling = current.parent.right
                if sibling.color == RED:
                    # case 1) modify it, and become case 2, case 3 or case 4
                    sibling.color = BLACK
                    sibling.parent.color = RED
                    self.left_rotate(sibling.parent)
                    sibling = current.parent.right

                if sibling.right.color == sibling.left.color == BLACK:
                    # case 2) all children of sibling are black
                    sibling.color = RED
                    current = current.parent
                else:
                    if sibling.right.color == BLACK:
                        # case 3) sibling right child is black, and left child
                        # is red
                        sibling.color = RED
                        sibling.left.color = BLACK
                        self.right_rotate(sibling)
                        sibling = current.parent.right

                    # after case 3), the subtree becomes case 4)
                    # which means, right color is RED, and left color is BLACK
                    sibling.color = current.parent.color
                    sibling.right.color = BLACK
                    current.parent.color = BLACK
                    self.left_rotate(current.parent)
                    current = self.root

            else:
                # right child
                sibling = current.parent.left
                if sibling.color == RED:
                    # case 1) modify it, and become case 2, case 3 or case 4
                    sibling.color = BLACK
                    sibling.parent.color = RED
                    self.right_rotate(sibling.parent)
                    sibling = current.parent.left

                if sibling.right.color == sibling.left.color == BLACK:
                    # case 2) and continue loop
                    sibling.color = RED
                    current = current.parent
                else:
                    if sibling.left.color == BLACK:
                        # case 3) right is red, and try to becomes case 4)
                        sibling.right.color = BLACK
                        sibling.color = RED
                        self.left_rotate(sibling)

                    # case4 ) left must be red
                    sibling.color = sibling.parent.color
                    sibling.left.color = BLACK
                    sibling.parent.color = BLACK

                    self.right_rotate(sibling.parent)
                    current = self.root

        current.color = BLACK

    def delete(self, val):
        delete = self.search(val)
        if delete == NIL:
            raise Exception("data not found.")

        # keep only one child for deleted delegator
        if delete.left == NIL or delete.right == NIL:
            delegator = delete
        else:
            delegator = self.successor(delete)
            print("successor=>", delegator)
        child = delegator.left if delegator.left else delegator.right
        child.parent = delegator

        # though x is NIL,  x's parent still needs to be assigned
        # because we need to determine child located on left side or right side
        # of a deleted node while fixing up
        child.parent = delegator.parent

        if delegator.parent == NIL:
            # root
            self.root = child
        elif delegator.parent.left == delegator:
            delegator.parent.left = child

        else:
            delegator.parent.right = child

        if delegator != delete:
            # if the deleted node is delegator, we need to dupliate all
            # attributes of the deleted node into a delegator
            delete.dup(delegator)

        if delegator.color == BLACK:
            # if the deleted node is black, we must fix its child to meet the
            # Theorems of RB tree.
            self._deleteFixedUpRBT(child)

    def t_height(self, node):
        return 0 if node == NIL else 1 + \
            max(self.t_height(node.left), self.t_height(node.right))

    def traverse(self):
        cur = self.root
        rst = []
        while cur != NIL:
            if cur.left == NIL:
                rst += [str(cur)]
                cur = cur.right
            else:
                pred = cur.left
                while pred.right != NIL and pred.right != cur:
                    pred = pred.right
                if pred.right == NIL:
                    pred.right = cur
                    cur = cur.left
                else:
                    pred.right = NIL
                    rst += [str(cur)]
                    cur = cur.right
        return rst

    def preorder(self):
        cur = self.root
        rst = []
        visited = set([NIL])
        while cur != NIL:
            if cur.left == NIL:
                visited.add(cur)
                rst += [(str(cur),
                         str(cur.left) if cur.left not in visited else '',
                         str(cur.right) if cur.right not in visited else '')]
                cur = cur.right
            else:
                pred = cur.left
                while pred.right != NIL and pred.right != cur:
                    pred = pred.right
                if pred.right == NIL:
                    pred.right = cur
                    visited.add(cur)
                    rst += [(str(cur),
                             str(cur.left) if cur.left not in visited else '',
                             str(cur.right) if cur.right not in visited else ''
                             )]
                    cur = cur.left
                else:
                    pred.right = NIL
                    cur = cur.right
        return rst


if __name__ == "__main__":
    print(Node(2))
