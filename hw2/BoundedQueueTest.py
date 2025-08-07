import unittest
from BoundedQueue import BoundedQueue

class BoundedQueueTest(unittest.TestCase):

    def setUp(self):
        self.BQ = BoundedQueue(3)
        self.firstObject = object()
        self.BQ.enqueue(self.firstObject)

    # Test BoundedQueue
    # Test BoundedQueue C1, C2
    # BoundedQueue Base : F(arg >= 0)
    def test_BoundedQueue_base(self):
        # Code does not raise any exception
        try:
            BoundedQueue(2)
        except Exception as e:
            print(e)

    # BoundedQueue2 : T(arg < 0)
    def test_BoundedQueue_2(self):
        # Should raise exception
        with self.assertRaises(ValueError):
            BoundedQueue(-2)

    # Test Enqueue C1, C2, C3, C4, C7
    # enqueue base: FTFF(when queue is not full, enqueue an object)
    # no exception
    def test_Enqueue_base(self):
        try:
            self.BQ.enqueue(object()) # add second object
        except Exception as e:
            print(e)

    # enqueue 2. FTFT (queue is full, enqueue an object)
    # raise RuntimeError
    def test_Enqueue_2(self):
        self.BQ.enqueue(object())
        self.BQ.enqueue(object())
        # add new element when Queue is full
        with self.assertRaises(RuntimeError):
            self.BQ.enqueue(object())

    # enqueue 3. FTTF (queue is not full, enqueue null object)
    def test_Enqueue_3(self):
        with self.assertRaises(TypeError):
            self.BQ.enqueue(None)

    # enqueue 4. FTTT (queue is full, enqueue null object)
    def test_Enqueue_4(self):
        self.BQ.enqueue(object())
        self.BQ.enqueue(object())
        with self.assertRaises(TypeError):
            self.BQ.enqueue(None) # add new element when Queue is full

    # Dequeue
    # Test Dequeue C1, C2, C5, C6
    # base: FTF (not empty, dequeue) no exception
    def test_Dequeue_base(self):
        try:
            self.BQ.enqueue(object())
            self.BQ.dequeue()
        except Exception as e:
            print(e)

    # dequeue 2: FTT (queue is empty, dequeue)
    def test_Dequeue_2(self):
        #self.BQ.dequeue() # BQ empty
        self.BQ = BoundedQueue(3)
        with self.assertRaises(RuntimeError):
            self.BQ.dequeue()

    # Test isEmpty
    # Test isEmpty C1, C6, C7
    # base FF(new a not empty queue)
    def test_isEmpty_base(self):
        self.assertFalse(self.BQ.is_empty())

    # 2. FT (new an empty queue)
    def test_isEmpty_2(self):
        #self.BQ.dequeue()
        self.BQ = BoundedQueue(3)
        self.assertTrue(self.BQ.is_empty())

    # Test isFull
    # Test isFull C1, C2, C7
    # base FF  (new a not full queue)
    def test_isFull_base(self):
        self.assertFalse(self.BQ.is_full())

    # 2. FT (new a full queue)
    def test_isFull_2(self):
        # self.BQ.enqueue(object())
        # self.BQ.enqueue(object())
        self.BQ = BoundedQueue(1)
        self.BQ.enqueue(object())
        self.assertTrue(self.BQ.is_full())

if __name__ == '__main__':
    unittest.main()