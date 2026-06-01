"""A4 REBUILD — the twenty, posed by observation. Each (J,R) is read from a real
photo in the library: pose from the joints, build from the radii. Rebuilt by an
observer, not extracted by a machine."""
from sketch201_u1_a4_rig import render, radii, base, merge

def F(**kw):  # quick joint dict
    return kw

# ---------------- WALKERS ----------------
def omar():  # front walk toward camera, clearer stride + slight arm swing
    J=F(head=(0.02,0.075),neck=(0.01,0.155),sh=(0,0.20),shL=(-0.10,0.205),shR=(0.10,0.205),
        elL=(-0.10,0.34),elR=(0.13,0.345),wrL=(-0.06,0.46),wrR=(0.14,0.48),  # arms swing opposite
        hip=(0,0.50),hpL=(-0.07,0.515),hpR=(0.07,0.515),
        knL=(-0.125,0.70),knR=(0.065,0.755),anL=(-0.135,0.95),anR=(0.095,0.95),  # left leg leads
        ftL=(-0.18,0.985),ftR=(0.12,0.965))
    return J, radii(thigh=0.066,calf=0.045)
def ansspvt():  # suited profile walk, narrow body, clear fore/aft stride, front arm swung
    J=F(head=(0.05,0.08),neck=(0.025,0.16),sh=(0.0,0.205),shL=(-0.05,0.205),shR=(0.05,0.205),
        elL=(-0.075,0.34),elR=(0.085,0.33),wrL=(-0.10,0.45),wrR=(0.13,0.43),
        hip=(0,0.50),hpL=(-0.035,0.515),hpR=(0.035,0.515),
        knL=(-0.10,0.73),knR=(0.10,0.72),anL=(-0.155,0.95),anR=(0.165,0.95),
        ftL=(-0.205,0.985),ftR=(0.215,0.985))
    return J, radii(thigh=0.058,calf=0.04,uarm=0.04,farm=0.03,headx=0.066,heady=0.086)
def linkedin():  # jacket, walk toward, upright, hands near sides
    J=F(head=(0.0,0.08),neck=(0,0.16),sh=(0,0.205),shL=(-0.12,0.21),shR=(0.12,0.21),
        elL=(-0.135,0.35),elR=(0.135,0.35),wrL=(-0.12,0.485),wrR=(0.12,0.485),
        hip=(0,0.50),hpL=(-0.075,0.515),hpR=(0.075,0.515),
        knL=(-0.085,0.725),knR=(0.07,0.74),anL=(-0.09,0.95),anR=(0.085,0.95),
        ftL=(-0.12,0.985),ftR=(0.115,0.975))
    return J, radii(thigh=0.07,calf=0.048,uarm=0.05)  # slightly heavier/jacket
def wassim():  # dark clothes profile walk, slim, striding
    J=F(head=(0.04,0.08),neck=(0.02,0.16),sh=(0,0.205),shL=(-0.055,0.205),shR=(0.055,0.205),
        elL=(-0.08,0.345),elR=(0.075,0.34),wrL=(-0.10,0.47),wrR=(0.10,0.45),
        hip=(0,0.50),hpL=(-0.04,0.515),hpR=(0.04,0.515),
        knL=(-0.105,0.73),knR=(0.085,0.72),anL=(-0.145,0.95),anR=(0.135,0.95),
        ftL=(-0.185,0.985),ftR=(0.175,0.985))
    return J, radii(thigh=0.058,calf=0.04,uarm=0.04,farm=0.03)
def nima():  # casual walk toward, weight forward
    J=F(head=(0.01,0.08),neck=(0,0.16),sh=(0,0.205),shL=(-0.105,0.21),shR=(0.105,0.21),
        elL=(-0.12,0.35),elR=(0.125,0.35),wrL=(-0.10,0.48),wrR=(0.12,0.48),
        hip=(0,0.50),hpL=(-0.07,0.515),hpR=(0.07,0.515),
        knL=(-0.105,0.72),knR=(0.055,0.745),anL=(-0.115,0.95),anR=(0.07,0.95),
        ftL=(-0.15,0.985),ftR=(0.10,0.975))
    return J, radii(thigh=0.064,calf=0.044)

# ---------------- STANDERS ----------------
def bruno():  # denim, standing square, solid build, feet apart, arms a touch off body
    J=merge(base(), shL=(-0.12,0.205),shR=(0.12,0.205),
        elL=(-0.14,0.35),elR=(0.14,0.35),wrL=(-0.125,0.50),wrR=(0.125,0.50),
        hpL=(-0.085,0.515),hpR=(0.085,0.515),
        knL=(-0.085,0.73),knR=(0.085,0.73),anL=(-0.09,0.965),anR=(0.09,0.965),
        ftL=(-0.125,0.995),ftR=(0.125,0.995))
    return J, radii(thigh=0.076,calf=0.052,uarm=0.05)  # heavier/solid
def cemrecan():  # slim-tall stand, right forearm raised holding something near chest/shoulder
    J=merge(base(), shL=(-0.095,0.205),shR=(0.095,0.205),
        elL=(-0.115,0.345),elR=(0.10,0.32),wrL=(-0.10,0.475),wrR=(-0.02,0.255),  # right hand up near opp shoulder
        knL=(-0.05,0.74),knR=(0.06,0.73),anL=(-0.05,0.965),anR=(0.06,0.965))
    return J, radii(thigh=0.06,calf=0.042,uarm=0.04,headx=0.068,heady=0.09)
def jose():  # casual stand, strong contrapposto, hands in pockets
    J=merge(base(), shL=(-0.085,0.205),shR=(0.12,0.20),  # shoulders counter the hips
        hpL=(-0.125,0.51),hpR=(0.035,0.53),
        elL=(-0.115,0.35),elR=(0.105,0.35),wrL=(-0.07,0.49),wrR=(0.045,0.50),
        knL=(-0.115,0.73),knR=(0.03,0.74),anL=(-0.115,0.965),anR=(0.035,0.965),
        ftL=(-0.15,0.995),ftR=(0.075,0.995))
    return J, radii(thigh=0.068,calf=0.047)
def zachary():  # relaxed stand, slight contrapposto, one hand toward pocket
    J=merge(base(), hpL=(-0.085,0.515),hpR=(0.06,0.525),
        elL=(-0.135,0.35),elR=(0.10,0.355),wrL=(-0.14,0.49),wrR=(0.06,0.51),
        knL=(-0.085,0.73),knR=(0.05,0.735),anL=(-0.085,0.965),anR=(0.05,0.965),
        ftL=(-0.12,0.995),ftR=(0.09,0.995))
    return J, radii(thigh=0.062,calf=0.044)  # leaner
def britain():  # wide athletic stance, knees soft, arms held a little out
    J=F(head=(0,0.08),neck=(0,0.16),sh=(0,0.205),shL=(-0.115,0.21),shR=(0.115,0.21),
        elL=(-0.17,0.35),elR=(0.17,0.35),wrL=(-0.155,0.49),wrR=(0.155,0.49),
        hip=(0,0.50),hpL=(-0.10,0.515),hpR=(0.10,0.515),
        knL=(-0.155,0.72),knR=(0.155,0.72),anL=(-0.165,0.955),anR=(0.165,0.955),
        ftL=(-0.21,0.99),ftR=(0.21,0.99))
    return J, radii(thigh=0.07,calf=0.05)

# ---------------- SEATED ----------------
def subhaan():  # elbows on knees, lean forward, head dropped
    J=F(head=(0.0,0.20),neck=(0.0,0.29),sh=(0.0,0.33),shL=(-0.12,0.335),shR=(0.12,0.335),
        elL=(-0.165,0.55),elR=(0.165,0.55),wrL=(-0.08,0.63),wrR=(0.08,0.63),
        hip=(0,0.67),hpL=(-0.115,0.67),hpR=(0.115,0.67),
        knL=(-0.185,0.63),knR=(0.185,0.63),anL=(-0.175,0.965),anR=(0.175,0.965),
        ftL=(-0.205,0.99),ftR=(0.205,0.99))
    return J, radii(thigh=0.082,calf=0.055,uarm=0.05,headx=0.076,heady=0.096,waist=0.95)
def christian():  # broad, seated bench, hands on knees, knees apart
    J=F(head=(0,0.11),neck=(0,0.19),sh=(0,0.23),shL=(-0.14,0.235),shR=(0.14,0.235),
        elL=(-0.17,0.41),elR=(0.17,0.41),wrL=(-0.15,0.56),wrR=(0.15,0.56),
        hip=(0,0.59),hpL=(-0.13,0.59),hpR=(0.13,0.59),
        knL=(-0.17,0.61),knR=(0.17,0.61),anL=(-0.155,0.94),anR=(0.155,0.94),
        ftL=(-0.18,0.965),ftR=(0.18,0.965))
    return J, radii(thigh=0.088,calf=0.057,uarm=0.054,headx=0.08,heady=0.10,waist=0.96)
def brock():  # seated, legs extended forward (relaxed back), a bag bulk at side
    J=F(head=(0.02,0.13),neck=(0,0.21),sh=(0,0.25),shL=(-0.125,0.255),shR=(0.125,0.255),
        elL=(-0.14,0.41),elR=(0.14,0.41),wrL=(-0.06,0.52),wrR=(0.07,0.52),
        hip=(0,0.585),hpL=(-0.115,0.585),hpR=(0.115,0.585),
        knL=(-0.105,0.75),knR=(0.125,0.74),anL=(-0.165,0.93),anR=(0.185,0.93),
        ftL=(-0.205,0.96),ftR=(0.225,0.955))
    return J, radii(thigh=0.078,calf=0.052,uarm=0.05)
def podmatch():  # seated upright bench, hands to knees
    J=F(head=(0,0.12),neck=(0,0.20),sh=(0,0.24),shL=(-0.115,0.245),shR=(0.115,0.245),
        elL=(-0.13,0.41),elR=(0.13,0.41),wrL=(-0.085,0.56),wrR=(0.085,0.56),
        hip=(0,0.585),hpL=(-0.105,0.585),hpR=(0.105,0.585),
        knL=(-0.11,0.62),knR=(0.11,0.62),anL=(-0.10,0.93),anR=(0.10,0.93),
        ftL=(-0.135,0.96),ftR=(0.135,0.96))
    return J, radii(thigh=0.075,calf=0.05)
def diego_floor():  # sit on floor, one knee up, one arm propped back
    J=F(head=(-0.06,0.19),neck=(-0.04,0.27),sh=(-0.01,0.31),shL=(-0.13,0.315),shR=(0.10,0.32),
        elL=(-0.19,0.47),elR=(0.14,0.50),wrL=(-0.24,0.63),wrR=(0.19,0.62),
        hip=(0,0.665),hpL=(-0.08,0.665),hpR=(0.10,0.665),
        knL=(-0.15,0.71),knR=(0.20,0.55),anL=(-0.22,0.83),anR=(0.10,0.745),
        ftL=(-0.27,0.84),ftR=(0.055,0.755))
    return J, radii(thigh=0.07,calf=0.048,uarm=0.046)

# ---------------- DYNAMIC / SPECIAL ----------------
def dominic():  # dancer: planted left leg, right leg lifted/extended, arms spread
    J=F(head=(0.02,0.085),neck=(0.0,0.165),sh=(0.0,0.21),shL=(-0.11,0.205),shR=(0.11,0.215),
        elL=(-0.235,0.165),elR=(0.215,0.27),wrL=(-0.33,0.11),wrR=(0.30,0.345),
        hip=(0,0.52),hpL=(-0.07,0.52),hpR=(0.075,0.52),
        knL=(-0.10,0.74),knR=(0.215,0.62),anL=(-0.105,0.97),anR=(0.36,0.69),
        ftL=(-0.145,0.995),ftR=(0.405,0.70))
    return J, radii(thigh=0.058,calf=0.041,uarm=0.04,farm=0.03)
def benigno():  # perched/leaning, reaching one arm out, the dynamic seated
    J=F(head=(0.10,0.15),neck=(0.06,0.24),sh=(0.0,0.28),shL=(-0.11,0.285),shR=(0.11,0.29),
        elL=(-0.10,0.44),elR=(0.21,0.40),wrL=(-0.03,0.54),wrR=(0.31,0.50),
        hip=(0,0.575),hpL=(-0.10,0.575),hpR=(0.10,0.575),
        knL=(-0.12,0.73),knR=(0.105,0.72),anL=(-0.10,0.93),anR=(0.165,0.93),
        ftL=(-0.135,0.96),ftR=(0.205,0.955))
    return J, radii(thigh=0.066,calf=0.045,uarm=0.044)
def sarah():  # reclining on grass, propped on left elbow, legs extended right
    J=F(head=(-0.30,0.46),neck=(-0.24,0.51),sh=(-0.18,0.54),shL=(-0.245,0.51),shR=(-0.12,0.57),
        elL=(-0.30,0.66),elR=(-0.02,0.66),wrL=(-0.345,0.80),wrR=(0.07,0.62),
        hip=(0.04,0.66),hpL=(-0.01,0.625),hpR=(0.08,0.69),
        knL=(0.24,0.69),knR=(0.22,0.78),anL=(0.44,0.73),anR=(0.43,0.82),
        ftL=(0.50,0.735),ftR=(0.49,0.825))
    return J, radii(thigh=0.062,calf=0.044,uarm=0.044,headx=0.066,heady=0.086)
def sueda():  # low crouch / squat, compact, elbows toward knees
    J=F(head=(0.0,0.42),neck=(0.0,0.50),sh=(0.0,0.54),shL=(-0.11,0.545),shR=(0.11,0.545),
        elL=(-0.15,0.70),elR=(0.15,0.70),wrL=(-0.07,0.80),wrR=(0.07,0.80),
        hip=(0,0.86),hpL=(-0.10,0.86),hpR=(0.10,0.86),
        knL=(-0.17,0.72),knR=(0.17,0.72),anL=(-0.105,0.97),anR=(0.105,0.97),
        ftL=(-0.145,0.99),ftR=(0.145,0.99))
    return J, radii(thigh=0.072,calf=0.05,uarm=0.046,headx=0.072,heady=0.092,waist=0.95)
def safia():  # standing, back to camera, both arms raised overhead
    J=F(head=(0.0,0.10),neck=(0,0.17),sh=(0,0.215),shL=(-0.11,0.215),shR=(0.11,0.215),
        elL=(-0.165,0.105),elR=(0.165,0.105),wrL=(-0.135,0.0),wrR=(0.135,0.0),
        hip=(0,0.51),hpL=(-0.075,0.52),hpR=(0.075,0.52),
        knL=(-0.07,0.73),knR=(0.07,0.73),anL=(-0.07,0.965),anR=(0.07,0.965),
        ftL=(-0.10,0.995),ftR=(0.10,0.995))
    return J, radii(thigh=0.07,calf=0.047)

# registry: idx -> (label, fn)
FIGS={
 29:('omar',omar),1:('ansspvt',ansspvt),23:('linkedin',linkedin),38:('wassim',wassim),28:('nima',nima),
 5:('bruno',bruno),7:('cemrecan',cemrecan),21:('jose',jose),39:('zachary',zachary),3:('britain',britain),
 4:('brock',brock),8:('christian',christian),34:('subhaan',subhaan),14:('diego',diego_floor),30:('podmatch',podmatch),
 16:('dominic',dominic),2:('benigno',benigno),33:('sarah',sarah),35:('sueda',sueda),32:('safia',safia),
}
