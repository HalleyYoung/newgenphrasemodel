# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 19:34:09 2015

@author: halley
"""
import transform as tf
import melodyhelpers as mlh

def oneTwoOneTwo(motifs):
    phrases = []
    phrases.append(motifs[0])
    phrases.append(motifs[1])
    phrases.append(tf.getSmallTransformFunction()(motifs[0]))
    phrases.append(mlh.transformToEnding(motifs[1]))
    return phrases    
    
def oneOneOneOne(motifs):
    phrases = []
    phrases.append(motifs[0])
    phrases.append(tf.getTransformFunction()(motifs[0]))
    phrases.append(tf.getSmallTransformFunction()(motifs[0]))
    phrases.append(mlh.transformToEnding(tf.getTransformFunction()(motifs[0])))
    return phrases
    
def oneOneTwoTwo(motifs):
    phrases = []
    phrases.append(motifs[0])
    phrases.append(tf.getTransformFunction()(motifs[0]))
    phrases.append(motifs[1])
    phrases.append(mlh.transformToEnding(tf.getSmallTransformFunction()(motifs[1])))
    return phrases
    
def oneTwoOneThree(motifs):
    phrases = []
    phrases.append(motifs[0])
    phrases.append(motifs[1])
    phrases.append(tf.getSmallTransformFunction()(motifs[0]))
    phrases.append(mlh.transformToEnding(motifs[2]))
    return phrases
        