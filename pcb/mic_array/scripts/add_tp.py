__author__ = 'afc'

import pcbnew
from pcbnew import *

import math

def moveModule(m, center, offset, x, y, a):
    ox = offset[0]*math.cos(a) - offset[1]*math.sin(a)
    oy = offset[0]*math.sin(a) + offset[1]*math.cos(a) 

    m.SetPosition(wxPointMM(center[0] + x + ox, center[1] + y + oy))

    return m

base = '../'
file = 'array.kicad_pcb'
board = pcbnew.LoadBoard(base + '/' + file)


center = [100, 100]

mic = 0
tp = 0
tp_offset   = [ -2.0, -3.0]

radius = 20; #mm

for ndx in range(1, 61):
    layer = int( round( math.sqrt( ndx/3.0 ) ))
    firstIdxInLayer = 3*layer*(layer-1) + 1
    side = (ndx - firstIdxInLayer) // layer
    idx  = (ndx - firstIdxInLayer) % layer
    x = radius *  (layer * math.cos( (side - 1) * math.pi/3 ) + (idx + 1) * math.cos( (side + 1) * math.pi/3 ) )
    y = radius * (-layer * math.sin( (side - 1) * math.pi/3 ) - (idx + 1) * math.sin( (side + 1) * math.pi/3 ) )
    a = math.atan2(y,x)

    mic_mod = board.FindModuleByReference('M' + str(mic))
    mic = mic + 1

    tp_mod = moveModule(board.FindModuleByReference('TP' + str(tp)), center, tp_offset, x, y, a)
    tp = tp + 1


    mic_P1 = [p for p in mic_mod.Pads() if p.GetPadName()=="1"][0]
    tp_P1  = [p for p in tp_mod.Pads() if p.GetPadName()=="1"][0]

    nt = pcbnew.TRACK(board)
    board.Add(nt)

    nt.SetStart(mic_P1.GetPosition())
    nt.SetEnd(tp_P1.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)



board.Save(base + '/' + 'test.kicad_pcb')


