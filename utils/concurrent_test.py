import unittest
import concurrent

class TestPThread(unittest.TestCase):
    def setUp(self):
        pass
    
    def testPthread(self):
        class ThreadA(concurrent.PThread):
            def run(self):
                print("ThreadA")
        
        class ThreadB(concurrent.PThread):
            def run(self):
                print("ThreadB")
        
        oThreadA = ThreadA()
        oThreadB = ThreadB()
        print("before start")
        oThreadA.start()
        oThreadB.start()
        print(f"ThreadA.ident={oThreadA.ident}")
        print(f"ThreadB.ident={oThreadB.ident}")
        oThreadA.join()
        oThreadB.join()
         
    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()