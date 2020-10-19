#coding:utf-8
import unittest
from AI大比拼 import *
class MyTestCase(unittest.TestCase):
    def test1(self):
        uuid = "7aa3a255-a8a9-4314-91d8-57772d068087"
        global  answer
        answer = False
        step, swap, uuid, zuhao, listproblem, dis = jiekou.challenge(uuid)
        set(step, swap, uuid, zuhao, listproblem, dis)
        NumberHuaRong()
        jiekou.submit(uuid, operations, myswap)
        self.assertEqual(answer, str(True))
    def test2(self):
        uuid = "ec0dd026-3a78-4b18-971f-2b651aaa7b5f"
        global  answer
        answer = False
        step, swap, uuid, zuhao, listproblem, dis = jiekou.challenge(uuid)
        set(step, swap, uuid, zuhao, listproblem, dis)
        NumberHuaRong()
        jiekou.submit(uuid, operations, myswap)
        self.assertEqual(answer, str(True))
    def test3(self):
        uuid = "cac66a4d-956b-4abe-9baf-f45087a4290a"
        global  answer
        answer = False
        step, swap, uuid, zuhao, listproblem, dis = jiekou.challenge(uuid)
        set(step, swap, uuid, zuhao, listproblem, dis)
        NumberHuaRong()
        jiekou.submit(uuid, operations, myswap)
        self.assertEqual(answer, str(True))
if __name__ == '__main__':
    unittest.main()

