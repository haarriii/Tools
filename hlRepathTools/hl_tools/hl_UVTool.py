# Autor Harriet Landa Gil 2020


from functools import partial
import maya.cmds as mc

def trnX(numbermove, collection1, *args):
    '''
    This funcion move the uv shell depending the parameters gived in the UI
    '''
    movenum = mc.intField(numbermove, q=1, v=1)
    radiosel = mc.radioCollection(collection1, q=1, sl=1)
    radiolabel = mc.radioButton(radiosel, q=1, label=True)
    if radiolabel == '-':
        mc.polyEditUV(u=-movenum, v=0)
    else:
        mc.polyEditUV(u=movenum, v=0)


def trnY(numbermove, collection1, *args):
    '''
    This funcion move the uv shell depending the parameters gived in the UI
    '''
    movenum = mc.intField(numbermove, q=1, v=1)
    radiosel = mc.radioCollection(collection1, q=1, sl=1)
    radiolabel = mc.radioButton(radiosel, q=1, label=True)
    if radiolabel == '-':
        mc.polyEditUV(u=0, v=-movenum)
    else:
        mc.polyEditUV(u=0, v=movenum)


def unf(unresmenu, *args):
    '''
    This funcion unfold the uv shells depending the parameters gived in the UI
    '''
    res = mc.optionMenu(unresmenu, q=1, v=1)
    mc.u3dUnfold(bi=1, ite=1, ms=int(res), tf=1)


def lay(layresmenu, unum, vnum, *args):
    '''
    This funcion layout all the uv shells depending the parameters gived in the UI
    '''
    reso = mc.optionMenu(layresmenu, q=1, v=1)
    unumb = mc.intFieldGrp(unum, q=1, v=1)
    vnumb = mc.intFieldGrp(vnum, q=1, v=1)
    mc.u3dLayout(res=int(reso), spc=0.0078125, mar=0.0078125, u=int(unumb[0]), v=int(vnumb[0]))

### uv cut and sew funcions ###
def cut(*args):
    mc.polyMapCut()
def sew(*args):
    mc.polyMapSew()

def UVTool():
    '''
    The main funcion that creates the UI 
    '''
    ### Open the UV editor ###
    mc.TextureViewWindow()
    
    
    if mc.window("UVToolkit", exists=True):
        mc.deleteUI("UVToolkit")
    
    mc.window("UVToolkit", title="UV Toolkit", sizeable=True)
    
    mc.columnLayout(adj=True)
    mc.button(l='Cut', bgc=(0,1,0), c=partial(cut))
    mc.button(l='Sew', bgc=(0,1,0), c=partial(sew))
    
    mc.frameLayout(label='Transform', nch=3)
    mc.rowColumnLayout(nc=3)
    numbermove = mc.intField()
    btn = mc.button(l='Transform X')
    collection1 = mc.radioCollection()
    mc.radioButton(label='+', select=True)
    mc.button(btn, e=1, c=partial(trnX, numbermove, collection1))
    mc.separator(style='none')
    mc.button(l='Transform Y', c=partial(trnY, numbermove, collection1))
    mc.radioButton(label='-')
    mc.setParent('..')

    mc.frameLayout(label='Unfold')
    mc.rowColumnLayout()
    unresmenu = mc.optionMenu(label='Resolution')
    mc.menuItem(label='0')
    mc.menuItem(label='1024')
    mc.menuItem(label='2048')
    mc.menuItem(label='4096')
    mc.button(l='Unfold', c=partial(unf, unresmenu))
    mc.setParent('..')

    mc.frameLayout(label='Layout')
    mc.rowColumnLayout()
    layresmenu = mc.optionMenu(label='Resolution')
    mc.menuItem(label='0')
    mc.menuItem(label='1024')
    mc.menuItem(label='2048')
    mc.menuItem(label='4096')
    unum = mc.intFieldGrp(l='U', v1=1)
    vnum = mc.intFieldGrp(l='V', v1=1)
    mc.button(l='Layout', c=partial(lay, layresmenu, unum, vnum))
    mc.setParent('..')

    mc.showWindow("UVToolkit")
    mc.window("UVToolkit", e=True, width=220, height=320, sizeable=False)






