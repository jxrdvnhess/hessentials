import importlib.util, numpy as np
spec=importlib.util.spec_from_file_location("ht","head_ten.py")
# we can't run head_ten (it renders a sheet); instead reproduce minimal check:
# looking-UP should make the UNDER-CHIN (BASE) come toward viewer (+z) and APEX go back.
import math
def Rx(a):c,s=math.cos(a),math.sin(a);return np.array([[1,0,0],[0,c,-s],[0,s,c]])
APEX=np.array([0,-130,-30.]); BASE=np.array([0,128,20.])
for p in (-50,50):
    R=Rx(math.radians(p))
    az=(R@APEX)[2]; bz=(R@BASE)[2]
    view="LOOKING UP (underside toward us)" if bz>az else "LOOKING DOWN (cranium toward us)"
    print(f"pitch {p:+d}: apex z={az:6.1f}  underchin z={bz:6.1f}  -> {view}")
