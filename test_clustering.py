# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:43:46 2021

@author: lilledah
"""
import unittest
import clustering

class TestClustering(unittest.TestCase):
    
    def test_num_neighbours(self):
        result = clustering.num_neighbours(1)
        self.assertEqual(result, 4)
        result = clustering.num_neighbours(2)
        self.assertEqual(result, 8)
        
#Se video hvordan endres for å kunne kjøre i editoren (init funksjon?)