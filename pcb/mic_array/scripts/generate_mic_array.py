import pcbnew
from pcbnew import *
import math

board = pcbnew.GetBoard()

center = [110, 100]
led_center = [110, 100]

mic = 0
led = 0
cap = 0
mic_offset   = [ 0.0,  0.0]
led_offset   = [-3.0,  0.0]
c100n_offset = [-3.2,  0.2]
c10u_offset  = [-4.2,  0.0]
vdd_offset   = [-4.7,  0.65]
gnd_offset   = [-4.7, -0.65]
clk_offset   = [-1.1,  1.5]
sel_offset   = [-1.3, -1.5]
v5_offset    = [-1.8,  2.5]

radius = 20; #mm

def moveModule(m, center, offset, x, y, a):
    ox = offset[0]*math.cos(a) - offset[1]*math.sin(a)
    oy = offset[0]*math.sin(a) + offset[1]*math.cos(a) 

    m.SetPosition(VECTOR2I(int((center[0] + x + ox)*1000000), int((center[1] + y + oy)*1000000)))

    return m


for ndx in range(1, 61):
    layer = int( round( math.sqrt( ndx/3.0 ) ))
    firstIdxInLayer = 3*layer*(layer-1) + 1
    side = (ndx - firstIdxInLayer) // layer
    idx  = (ndx - firstIdxInLayer) % layer
    x = radius *  (layer * math.cos( (side - 1) * math.pi/3 ) + (idx + 1) * math.cos( (side + 1) * math.pi/3 ) )
    y = radius * (-layer * math.sin( (side - 1) * math.pi/3 ) - (idx + 1) * math.sin( (side + 1) * math.pi/3 ) )
    a = math.atan2(y,x)

    d = moveModule(board.FindFootprintByReference('D' + str(led)), led_center, led_offset, x, y, a)
    d.SetLayer(pcbnew.F_Cu)
    d.SetOrientationDegrees((-math.degrees(a+math.pi/2)))
    
    led = led + 1

    V5 = [p for p in d.Pads() if p.GetPadName()=="6"][0]

    v = moveModule(pcbnew.PCB_VIA(board), center, v5_offset, x, y, a)
    board.Add(v)
    v.SetNet(board.GetNetsByName()['+5V'])
    v.SetWidth(700000)

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetNet(board.GetNetsByName()['+5V'])
    nt.SetStart(V5.GetPosition())
    nt.SetEnd(v.GetPosition())
    nt.SetLayer(pcbnew.F_Cu)    

    continue 
    m = moveModule(board.FindFootprintByReference('M' + str(mic)), center, mic_offset, x, y, a)
    m.SetOrientationDegrees((-math.degrees(a+math.pi/2)))
    mic = mic + 1

    v = moveModule(pcbnew.PCB_VIA(board), center, sel_offset, x, y, a)
    board.Add(v)
    v.SetWidth(700000)

    mp = [p for p in m.Pads() if p.GetPadName()=="2"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)

    nt.SetStart(v.GetPosition())
    nt.SetEnd(mp.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)

    v = moveModule(pcbnew.PCB_VIA(board), center, clk_offset, x, y, a)
    board.Add(v)
    v.SetWidth(700000)

    mp = [p for p in m.Pads() if p.GetPadName()=="4"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)

    nt.SetStart(v.GetPosition())
    nt.SetEnd(mp.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)

    c100n = moveModule(board.FindFootprintByReference('C' + str(cap)), center, c100n_offset, x, y, a)
    c100n.SetOrientationDegrees((-math.degrees(a-math.pi/2)))
    cap = cap + 1

    c10u = moveModule(board.FindFootprintByReference('C' + str(cap)), center, c10u_offset, x, y, a)
    c10u.SetOrientationDegrees((-math.degrees(a-math.pi/2)))
    cap = cap + 1

    v = moveModule(pcbnew.PCB_VIA(board), center, vdd_offset, x, y, a)
    board.Add(v)
    v.SetNet(board.GetNetsByName()['VDD'])
    v.SetWidth(700000)

    cp = [p for p in c100n.Pads() if p.GetPadName()=="1"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetNet(board.GetNetsByName()['VDD'])
    nt.SetStart(v.GetPosition())
    nt.SetEnd(cp.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)

    mp = [p for p in m.Pads() if p.GetPadName()=="5"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetNet(board.GetNetsByName()['VDD'])
    nt.SetStart(cp.GetPosition())
    nt.SetEnd(mp.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)

    v = moveModule(pcbnew.PCB_VIA(board), center, gnd_offset, x, y, a)
    board.Add(v)
    v.SetNet(board.GetNetsByName()['GND'])
    v.SetWidth(700000)
    cp = [p for p in c100n.Pads() if p.GetPadName()=="2"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetNet(board.GetNetsByName()['GND'])
    nt.SetStart(cp.GetPosition())
    nt.SetEnd(v.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)


    cp = [p for p in c100n.Pads() if p.GetPadName()=="2"][0]
    mp = [p for p in m.Pads() if p.GetPadName()=="3"][0]
    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetNet(board.GetNetsByName()['GND'])
    nt.SetStart(cp.GetPosition())
    nt.SetEnd(mp.GetPosition())
    nt.SetLayer(pcbnew.B_Cu)


led = 0

for ndx in range(1, 60):
    layer = int( round( math.sqrt( ndx/3.0 ) ))
    firstIdxInLayer = 3*layer*(layer-1) + 1
    side = (ndx - firstIdxInLayer) // layer
    idx  = (ndx - firstIdxInLayer) % layer
    x = radius *  (layer * math.cos( (side - 1) * math.pi/3 ) + (idx + 1) * math.cos( (side + 1) * math.pi/3 ) )
    y = radius * (-layer * math.sin( (side - 1) * math.pi/3 ) - (idx + 1) * math.sin( (side + 1) * math.pi/3 ) )
    a = math.atan2(y,x)

    d0 = board.FindFootprintByReference('D' + str(led))
    d1 = board.FindFootprintByReference('D' + str(led+1))
    
    led = led + 1

    DO = [p for p in d0.Pads() if p.GetPadName()=="1"][0]
    DI = [p for p in d1.Pads() if p.GetPadName()=="5"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetStart(DO.GetPosition())
    nt.SetEnd(DI.GetPosition())
    nt.SetLayer(pcbnew.F_Cu)

    DI = [p for p in d0.Pads() if p.GetPadName()=="2"][0]
    BI = [p for p in d1.Pads() if p.GetPadName()=="4"][0]

    nt = pcbnew.PCB_TRACK(board)
    board.Add(nt)
    nt.SetStart(DI.GetPosition())
    nt.SetEnd(BI.GetPosition())
    nt.SetLayer(pcbnew.F_Cu)

