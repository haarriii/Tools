# Autor Harriet Landa Gil 2020


import maya.cmds as mc
import mtoa.ui.arnoldmenu as arnoldmenu
import webbrowser as wb
import mtoa.utils as mutils
from functools import partial


def loc(*args):
    '''
    Create a locator to then get his position and create the balls
    '''
    mc.spaceLocator(n='Balls_Position')


def lD(*args):
    '''
    This funcion create 2 balls and the mackbeth plane with a plane as floor with a shadowmate shader applied
    '''
    mc.polySphere(n='Chrome_Ball_GEO')
    mc.move(-1.5,0,0,'Chrome_Ball_GEO')
    mc.polySphere(n='Matte_Ball_GEO')
    mc.move(1.5, 0, 0, 'Matte_Ball_GEO')
    mc.polyPlane(n='McBeth_Chart_GEO')
    mc.move(0,-2.135,0, 'McBeth_Chart_GEO')
    mc.rotate(90,0,0, 'McBeth_Chart_GEO')
    mc.scale(3.468,3.468,1.855, 'McBeth_Chart_GEO')
    mc.group('Chrome_Ball_GEO','Matte_Ball_GEO','McBeth_Chart_GEO', n='Look_Dev_GRP')
    mc.parentConstraint('Balls_Position','Look_Dev_GRP', mo=False)
    mc.select('Look_Dev_GRP', hi=True)
    mc.delete('Look_Dev_GRP_parentConstraint1')
    mc.makeIdentity(apply=True, t=True, r=True, s=True )
    mc.group('Chrome_Ball_GEO','Matte_Ball_GEO', 'McBeth_Chart_GEO', n='Balls_GRP')
    mc.hide('Balls_Position')
    Chrome_shd = mc.shadingNode('aiStandardSurface', name='Chrome_SHD', asShader=True)
    mc.setAttr(Chrome_shd + '.metalness', 1)
    mc.select('Chrome_Ball_GEO')
    mc.hyperShade(a=Chrome_shd)
    Matte_shd = mc.shadingNode('aiStandardSurface', name='Matte_SHD', asShader=True)
    mc.setAttr(Chrome_shd + '.base', 1)
    mc.select('Matte_Ball_GEO')
    mc.hyperShade(a=Matte_shd)
    McBeth_SHD = mc.shadingNode('aiStandardSurface', name='McBeth_SHD', asShader=True)
    mc.setAttr(McBeth_SHD + '.base', 1)
    file_node = mc.shadingNode('file', asTexture=True, n='Mcbeth_RGB')
    shading_group = mc.sets(renderable=True, noSurfaceShader=True, empty=True)
    mc.connectAttr('%s.outColor' %McBeth_SHD, '%s.surfaceShader' %shading_group)
    mc.connectAttr('%s.outColor' %file_node, '%s.baseColor' %McBeth_SHD)
    mc.select('McBeth_Chart_GEO')
    mc.hyperShade(a=McBeth_SHD)
    sky = mutils.createLocator("aiSkyDomeLight", asLight=True)
    mc.rename('aiSkyDomeLight1', 'Sky_LIT')
    mc.setKeyframe('Sky_LIT' ,v=0, at='.rotateY',t='1101' )
    mc.setKeyframe('Sky_LIT',v=360, at='.rotateY',t='1200' )
    mc.selectKey('Sky_LIT', time=(1101,1200), attribute='rotateY' )
    mc.keyTangent( 'Sky_LIT', itt='linear', ott='linear')
    cam = mc.camera(name='RenderCam')
    cam1 = mc.select('RenderCam1')
    mc.rename(cam1, 'RenderCam')
    mc.polyPlane(n='Shadows_GEO', w=100, h=100)
    mc.parent('Shadows_GEO','Look_Dev_GRP')  
    mc.parent('Sky_LIT', 'Look_Dev_GRP')
    Shadow_shd = mc.shadingNode('aiShadowMatte', name='Shadows_SHD', asShader=True)
    mc.select('Shadows_GEO')
    mc.hyperShade(a=Shadow_shd)
    file_node = mc.shadingNode('file', asTexture=True, n='HDRI_Tx')
    mc.connectAttr('HDRI_Tx.outColor', 'Sky_LITShape.color')    
    file_node = mc.shadingNode('file', asTexture=True, n='HDRI_Tx')
    mc.connectAttr('HDRI_Tx.outColor', 'Sky_LITShape.color')
    




def tRen(*args):
    '''
    Open the Arnold RenderView
    '''
    arnoldmenu.arnoldMtoARenderView()



def locA(*args):
    '''
    Animate the lookdev
    '''
    mc.playbackOptions(edit=True, animationStartTime=1000)
    mc.playbackOptions(edit=True, animationEndTime=1200)
    mc.playbackOptions(edit=True, minTime=1000)
    mc.playbackOptions(edit=True, maxTime=1200)
    modelSel = mc.ls(sl=True)
    mc.spaceLocator(n='Model_LOC')
    mc.parent(modelSel , 'Model_LOC')
    mc.setKeyframe('Model_LOC',v=0, at='.rotateY',t='1001' )
    mc.setKeyframe('Model_LOC',v=360, at='.rotateY',t='1100' )
    mc.selectKey( 'Model_LOC', time=(1001,1100), attribute='rotateY' )
    mc.keyTangent( 'Model_LOC', itt='linear', ott='linear')




def mcbeth(*args):
    '''
    Import the macbeth file
    '''
    filename = mc.fileDialog2(fileMode=1, caption="Import Image")
    goodname = filename[0]
    mc.setAttr('Mcbeth_RGB.fileTextureName', goodname, type="string")
    


def hdri(*args):
    '''
    Import the hdri file
    '''
    filename = mc.fileDialog2(fileMode=1, caption="Import Image")
    goodname = filename[0]
    mc.setAttr('HDRI_Tx.fileTextureName', goodname, type="string")


def sball(*args):
    '''
    Select ball's group
    '''
    mc.select('Balls_GRP')


def web(*args):
    '''
    Open the web to a machbet image to download
    '''
    wb.open('https://www.dpreview.com/forums/post/58686976?image=0')
    


def spla(*args):
    '''
    Select the plane to scale 
    '''
    mc.select('Shadows_GEO')


def ldUI():
    '''
    The main function , create the UI 
    '''
    if mc.window("ldwin", exists=True, sizeable=True):
        mc.deleteUI("ldwin")


    myWindow = mc.window("ldwin", t="LookDev Setup by Harriet Landa", w=300, h=300)
    mc.columnLayout(adj=True)


    mc.text(l='Move the locator to the place where you want the balls to appear ', h=30, w=30, bgc=(1,1,1)) 
    mc.button(l='Create Locator', command=partial(loc))
    mc.button(l='Create Look Dev', command=partial(lD))
    mc.separator(h=10, w=10)
    mc.button(l='Import HDRI', command=partial(hdri))
    mc.button(l='Macbeth Image', command=partial(mcbeth))
    mc.button(l="If you don't have a macbeth image click here", command=partial(web))
    mc.separator(h=10, w=10)
    mc.button(l='Scale Balls', command=partial(sball))
    mc.button(l='Scale Plane', command=partial(spla))
    mc.separator(h=10, w=10)
    mc.text(l='Select the model that you want to do the turn around', h=30, w=30, bgc=(0,1,0)) 
    #mc.text(l='Fit the timeline to 1000-1200', h=30, w=30, bgc=(0,1,0)) 
    mc.button(l='Create Animated Locators', command=partial(locA))
    mc.button(l='Test Render', command=partial(tRen))
    mc.showWindow(myWindow)

