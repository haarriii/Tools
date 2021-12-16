import sys

p = r'P:\VFX_Project_17\Repath\tools\hlRepathTools\hl_tools\rp_import'

if not p in sys.path:
    sys.path.append(p)
    
import HL_import as im
reload(im)

rp_im_win = im.DesignerUI()
rp_im_win.show()