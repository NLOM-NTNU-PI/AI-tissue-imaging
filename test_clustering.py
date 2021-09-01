# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:43:46 2021

@author: lilledah
"""
import unittest
import img_utils as util

class TestClustering(unittest.TestCase):
    
    def test_num_neighbours(self):
        result = util.num_neighbours(1)
        self.assertEqual(result, 4)
        result = util.num_neighbours(2)
        self.assertEqual(result, 8)
    
    def test_neighbours_in_circle(self):
        result = util.neighbours_in_circle(0,0,1)
        l = len(result)
        self.assertEqual(l,4)
        self.assertTrue([0,1] in result)
        self.assertTrue([-1,0] in result)
        result = util.neighbours_in_circle(0,0,2)
        self.assertTrue([2,0] in result)
        result = util.neighbours_in_circle(3,3,2)
        self.assertTrue([3,2] in result)

if __name__ == '__main__':
    unittest.main()
#Se video hvordan endres for å kunne kjøre i editoren (init funksjon?)