# -*- coding: utf-8 -*-
"""
Created on Sat Oct 10 00:38:35 2020

@author: rasheed el-bouri
"""


from bingImageScrape import scrape
import argparse


topics = ["قطة", "كلب"]
numImgs = 30

for item in topics:
    scrape(item, numImgs)
