# -*- coding: utf-8 -*-
"""
Created on Sat Nov 15 11:48:37 2014

@author: halley
"""
from noteconstants import *
import functionalhelpers as fh
import copy
import scale as sc

"""
Motif class
Fields:
self.l0d = one-dimensional array of duration/rhythm values
self.l1d = two-dimensional array of duration/rhythm values, separated into one-beat groupings
self.l0p = one-dimensional array of pitch values
self.l1p = two-dimensional array of pitch values, separated into one-beat groupings
"""
class Motif:
    def mapStructure(self, origstruct, newlist): #used only for creating self.l1p out of self.l0p
        newstruct = []
        n = 0
        for i in range(0, len(origstruct)):
            newstruct.append([])
            for j in range(0, len(origstruct[i])):
                if len(newlist) > n:
                    newstruct[-1].append(newlist[n])
                n += 1
        return newstruct
    def __init__(self, pitches, durs, mtype = 0):
        self.mtype = mtype
        self.l0d = durs
        self.l1d = []
        new_note = True
        for note in self.l0d:
            if new_note:
                self.l1d.append([note])
                if (note % 1) != 0:
                    new_note = False
            else:
                self.l1d[-1].append(note)
                if sum(self.l1d[-1]) % 1 == 0:
                    new_note = True
        self.l0p = pitches
        self.l1p = self.mapStructure(self.l1d, pitches)
    def shift(self, shift_amount): #shift motif by n degrees
        self.l0p = map(lambda i: i + shift_amount, self.l0p)
        self.l1p = [map(lambda i: i + shift_amount, beat) for beat in self.l1p]
    def totalBeats(self): #returns total beats in motif
        return sum(map(lambda i: abs(i), self.l0d))   
    def shifted(self, shift_amount): #returns a shifted version of the motif (different than .shift, which changes self fields)
        new_shifted = Motif(self.l0p, self.l0d)
        new_shifted.shift(shift_amount)
        return new_shifted
    def strongPitches(self): #returns the strong pitches of the motif
        if sum(self.l1d[0]) == 1.0:
            return ([self.l1p[0][0], self.l1p[2][0]])
        else:
            return ([self.l1p[0][0], self.l1p[1][0]])
    def last_note(self):
        return self.l0p[-1]
    def isEnd(self):
        return self.l0d[-1] == 2 or self.l0d[:-4] == [1, -0.5, 0.5] or self.l0d[-1] == -1