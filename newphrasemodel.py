# -*- coding: utf-8 -*-
"""
Created on Sun Jan 11 19:04:23 2015

@author: halley
"""

from inspect import getmembers, isfunction
import random
import melodyhelpers as mlh
import music21helpers as mh
import newgenphrases as ngp
import probabilityhelpers as ph
import functionalhelpers as fh
import smooth
from constants import *
    
#shift motifs to allow for different chord types    
def shiftMotifs(phrase, prev_note = 0):
    shift_chords = [[i, i+2, i+4] for i in [0,4,3,6,1,5,2]]
    new_motifs = []
    #shift so that the two on-beat notes are on the desired chord
    for k in range(0, len(phrase)):
        motif = phrase[k]
        strong_pitches = motif.strongPitches()
        #all of the shifted motif values
        motif_shifts = [(i, [j + i for j in strong_pitches]) for i in [0,1,-1,2,-2,3,-3]]
        motif_shifts = filter(lambda i: abs(i[1][0]) - prev_note < 3, motif_shifts)
        done = False 
        n = 0
        #get an appropriate shift to product a desired chord
        while (not done and n < len(shift_chords)):
            correct_shift = filter(lambda i: all(i[1]) in shift_chords[n], motif_shifts)
            if len(correct_shift) > 0:
                print(correct_shift[0])
                new_motifs.append(motif.shifted(correct_shift[0][0]))
                done = True
            else:
                n += 1
        if (not done):
            new_motifs.append(motif) #if no appropriate value is found, just return motif
        prev_note = new_motifs[-1].l0p[-1]
    return phrase


#probability of applying a given phrase transform
def probPhraseType(tf):
    if tf == 'oneTwoOneTwo':
        return 4.0
    elif tf == 'oneOneOneOne':
        return 1.0
    elif tf == 'oneOneTwoTwo':
        return 2.0
    elif tf == 'oneTwoOneThree':
        return 3.0
    else:
        return 0.5

for k in range(0,1):
    phrases = []
    motif_patterns = []
    motifs = []
    for i in range(0,8):
        #first, decide what motifs are being used
        phr_motifs = []
        #with probability d, start with previous pattern
        p_prev_start = 0.6*len(motifs)**0.5
        ran1 = random.uniform(0,1) #for probability of starting with a new motif
        if ran1 < p_prev_start: #start with a previous one
            which_to_start = random.choice(range(0, len(motifs)))
            phrs_motifs = [motifs[which_to_start]]
            ran2 = random.uniform(0,1) #for probability of using previous batch
            prev_types = filter(lambda i: i[0] == which_to_start, motif_patterns)
            if ran2 < 0.8 * len(prev_types):
                reused_pattern = random.choice(prev_types)
                motif_patterns.append(reused_pattern)
                phrs_motifs = ([motifs[i] for i in random.choice(prev_types)])
            else:
                phrs_motifs = [motifs[which_to_start]]
                which_second = random.choice(range(0, len(motifs)))
                phrs_motifs.append(mlh.alterMotif(motifs[which_second], random.uniform(0,0.3), random.uniform(0,0.3)))
                #now, append third motif
                phrs_motifs.append(mlh.genMotif(4))
                #append to list of motifs and motif patterns
                motifs.append(phrs_motifs[-1])
                motif_patterns.append([which_to_start, which_second, len(motifs) - 1])
        else:
            phrs_motifs = [mlh.genMotif(4), mlh.genMotif(4), mlh.genMotif(4)]
            motifs.extend(phrs_motifs)
            motif_patterns.append([len(motifs) - 3, len(motifs) - 2, len(motifs) - 1])
        #then, divide into phrases
        phrase_functions_list = dict([(o[0], o[1]) for o in getmembers(ngp) if isfunction(o[1])])
        #the probability dict containing names of functions
        phrase_functions_probs = dict( [ (o[0], probPhraseType(o[0])) for o in getmembers(ngp) if isfunction(o[1]) ])
        phrase_type = phrase_functions_list[ph.probDictToChoice(phrase_functions_probs)]
        phrases.append(phrase_type(phrs_motifs))
    
    phrases = [shiftMotifs(phrase) for phrase in phrases]
        
    p = fh.concat(phrases)
    degrees = fh.concat([i.l0p for i in p])
    rhythms = fh.concat([i.l0d for i in p])
    degrees, rhythms = smooth.smoothOut(degrees, rhythms)
    score = mh.listsDegreesToStream(degrees, rhythms, scale = scales["dorian"])
    score.show()
