__author__ = 'afc'

import pcbnew
from pcbnew import *

base = '../'
file = 'array.kicad_pcb'
board = pcbnew.LoadBoard(base + '/' + file)


center = [100, 100]

mic = 0
cap = 0


for ndx in range(1, 61):
    m = board.FindModuleByReference('M' + str(mic))
    mic = mic + 1

    c100n = board.FindModuleByReference('C' + str(cap))
    cap = cap + 1

    c10u = board.FindModuleByReference('C' + str(cap))
    cap = cap + 1

    mP3 = [p for p in m.Pads() if p.GetPadName()=="3"][0]

    c100nP1 = [p for p in c100n.Pads() if p.GetPadName()=="1"][0]
    c100nP2 = [p for p in c100n.Pads() if p.GetPadName()=="2"][0]

    c10uP1 = [p for p in c10u.Pads() if p.GetPadName()=="1"][0]
    c10uP2 = [p for p in c10u.Pads() if p.GetPadName()=="2"][0]

    nt = pcbnew.TRACK(board)
    board.Add(nt)

    nt.SetStart(c100nP1.GetPosition())
    nt.SetEnd(c10uP1.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)

    nt = pcbnew.TRACK(board)
    board.Add(nt)

    nt.SetStart(c100nP2.GetPosition())
    nt.SetEnd(c10uP2.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)

    nt = pcbnew.TRACK(board)
    board.Add(nt)

    nt.SetStart(mP3.GetPosition())
    nt.SetEnd(c100nP2.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)




board.Save(base + '/' + 'test.kicad_pcb')


