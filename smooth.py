# -*- coding: utf-8 -*-
"""
Created on Tue Dec  2 16:09:47 2014

@author: halley
"""
import random
import scale as sc
import pitchhelpers as pth
import probabilityhelpers as ph

#smooth out pitch array
def doubleSmooth(pitches, durs, leading = True):
    new = [pitches[0]]
    new_durs = [durs[0]]
    for i in range(1, len(pitches)):
        dur = durs[i] if i < len(durs) else 1.0
        new_durs.append(dur)
        if pitches[i] == new[-1]: #remove doubles
            new.append(new[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]))
        elif pitches[i] < -3: #choose a new note if going lower than -3
            if new[-1] > 0: 
                new.append(new[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]) )
            else:
                new.append(new[-1] + 2)
        elif pitches[i] > 14: #choose a new note if going higher than 14
            if new[-1] < 12:
                new.append(new[-1] + ph.probDictToChoice(sc.horizontalmarkov)*random.choice([-1,1]) )
            else:
                new.append(new[-1] - 2)                    
        elif (new[-1] - pitches[i]) >= 4 or (new[-1] - pitches[i]) <= -4: #choose a new note if the gap between notes is too large
            closest = sc.closestNoteDegreeInTriad(new[-1], 0)
            if closest < -2:
                new.append(closest + random.choice([1,2,2,3]))
            elif new[-1] == closest:
                new.append(closest + random.choice([-2,-1,-1,1,1,2]))
            else:
                new.append(closest)
        else:
            new.append(pitches[i])        
        if dur > 1 and new[-1] % 7 not in [0,2,4]: #choose a new note if it is not in the chord triad
            closest = sc.closestNoteDegreeInTriad(new[-1], 0)
            new[-1] = (closest)
        if new[-1] < -3:
            new[-1] = random.choice(range(-3, 0))
        elif new[-1] > 14:
             new[-1] = random.choice(range(12,14))
    #make leading notes resolve to tonic
    if leading:
        for i in range(0, len(new) - 1):
            if new[i] % 12 == 11:
                if random.uniform(0,1) < 0.7:
                    new[i + 1] = new[i] + 1
    return (new, new_durs)

def smoothOut(pitches, durs, leading = True):
    new = [pitches[0]]
    for i in range(1, len(pitches)):
        new.append(pth.getClosestPCDegree(new[i-1], pitches[i]))
    return doubleSmooth(new, durs, leading)