# Autor Harriet Landa Gil 2020

import maya.cmds as mc
from functools import partial


def fractionBevel(fracSlid, *args):
   fracSlidVal = mc.floatSliderGrp(fracSlid, q=1, v=1)
   print(bevelname)
   mc.polyBevel3(bevelname[0], e=1, fraction=fracSlidVal)
def segmentBevel(segSlid, *args):
    segSlidVal = mc.intSliderGrp(segSlid, q=1, v=1)
    mc.polyBevel3(bevelname[0], e=1, sg=segSlidVal)

def makebevel(fracSlid, segSlid, *args):
    mc.floatSliderGrp(fracSlid, e=1, enable=1)
    mc.intSliderGrp(segSlid, e=1, enable=1)
    global bevelname
    bevelname = mc.polyBevel3(offsetAsFraction=1)

def hardEdges(lowAngleSld, higAngleSld, *args):
    lowAngle = mc.intSliderGrp(lowAngleSld, q=1, v=1)
    highAngle = mc.intSliderGrp(higAngleSld, q=1, v=1)
    if len(mc.ls(sl=1)) >= 1:
        mc.polySelectConstraint(m=3, t=0x8000, sm=1, ab=(int(lowAngle), int(highAngle)))
        mc.polySelectConstraint(m=0)
    else:
        mc.warning('SELECT SOMETHING')




def hardEdgesUI():
    window = mc.window( title="Hard Edges Bevel", widthHeight=(500, 220), sizeable=0)
    mc.columnLayout( adjustableColumn=True )
    mc.frameLayout(l='Select the angles', collapsable=1, collapse=0)
    lowAngleSld = mc.intSliderGrp(field=1, min=1, max=100 ,l='Low Angle', v=30)
    higAngleSld = mc.intSliderGrp(field=1, min=101, max=200 ,l='High Angle', v=150)
    mc.button(l='Select Edges', c=partial(hardEdges, lowAngleSld, higAngleSld))
    mc.setParent( '..' )
    mc.setParent( '..' )
    mc.frameLayout(l='Make the bevel', collapsable=1, collapse=1)
    bevelButon =  mc.button(l='Bevel')
    fracSlid = mc.floatSliderGrp(field=1, min=0, max=1 ,l='Fraction', pre=3 , v=0.002, enable=0)
    mc.floatSliderGrp(fracSlid, e=1, cc=partial(fractionBevel, fracSlid ))
    segSlid = mc.intSliderGrp(field=1, min=1, max=12 ,l='Segments', v=1, enable=0)
    mc.intSliderGrp(segSlid, e=1, cc=partial(segmentBevel, segSlid ))
    mc.button(bevelButon, e=1, c=partial(makebevel, fracSlid, segSlid))
    mc.showWindow( window )
    



def cableToolUI():
    if mc.window("cbl", exists=True):
            mc.deleteUI("cbl")
        
        
    mc.window("cbl", title="Cable Tool")
    mc.columnLayout(adj=True)
    mc.frameLayout( label='Create Curve', collapsable=True)
    mc.iconTextButton( style='iconOnly', image1='curveEP.png', label='EPCurveTool', c=partial(curveEPTool))
    mc.iconTextButton( style='iconOnly', image1='pencil.png', label='PencilTool', c=partial(curvePenTool))
    mc.setParent( '..' )
    createlayout = mc.frameLayout( label='Create Cable', collapsable=True, collapse=1)
    mc.separator(style='none')
    createbtn = mc.button(l='Create Cable')
    mc.separator(h=2, style='none')
    mc.setParent( '..' )
    settinglayout = mc.frameLayout( label='Cable Settings', collapsable=True, collapse=1)
    mc.button(createbtn, e=1, c=partial(cableCreate, settinglayout))
    mc.separator(style='none')
    count = mc.intFieldGrp(l='Count', v1=500)
    mc.intFieldGrp(count, e=1, cc=partial(countnum, count))
    mc.text(l='Cable Scale')
    csca = mc.floatSliderGrp(field=True,min=0.1, max=5, v=1)
    # mc.intSliderGrp(crot, e=1, cc=partial(changeCircleRot, crot))
    mc.floatSliderGrp(csca, e=1, cc=partial(changeCircleSca, csca))
    rev = mc.checkBox(l='Reverse')
    mc.checkBox(rev, e=1, cc=partial(reverseCheck, rev))
    mc.separator(h=20)
    mc.text(l='Darle a este boton al final del todo ')
    mc.button(l='Finish Cable', c=partial(fnsCable))
    mc.separator(h=2, style='none')
    mc.setParent( '..' )

    
    mc.showWindow("cbl")
    
def countnum(count, *args):
    countnum = mc.intFieldGrp(count, q=1, v1=1)
    print(countnum)
    if mc.objExists('nurbsTessellate1'):
        mc.setAttr('nurbsTessellate1.polygonCount', int(countnum))
    else:
        mc.warning('Crea El Cable')
 
def reverseCheck(rev, *args):
    check = mc.checkBox(rev, q=1, v=1)
    if check == True:
        mc.polyNormal('Cable_01', nm=0, unm=0, ch=1)
        mc.select(cl=1)
    else:
        mc.polyNormal('Cable_01', nm=0, unm=0, ch=1)
        mc.select(cl=1)
        
def changeCircleRot(crot, *args):
    goodrot = mc.intSliderGrp(crot, q=1, v=1)
    mc.xform('nurbsCircle1', ro=(0,goodrot,0))
    

def changeCircleSca(csca, *args):
    goodscale = mc.floatSliderGrp(csca, q=1, v=1)
    mc.xform('nurbsCircle1', s=(goodscale,goodscale,goodscale))
    
def curveEPTool(*args):
    mc.EPCurveTool()
    
def curvePenTool(*args):
    mc.PencilCurveTool()

def fnsCable(*args):
    mc.duplicate('Cable_01', n='Cable_01_GEO')
    mc.select('curve1', 'nurbsCircle1', 'Spheres', 'Clusters', 'Cable_01')
    mc.delete()
    mc.setAttr('Cable_01_GEO.overrideEnabled', 0)
    
    
    

    
def cableCreate(settinglayout, *args):
    sel = mc.ls(sl=True)
    if len(sel) > 0:   
        pos = mc.pointPosition( '{}.cv[0]'.format(sel[0]) )
        mc.hide(sel[0])
        
        curv, curv_hits= mc.circle()
        mc.hide(curv)
        mc.xform(curv, t=pos)
        
        ext, ext_hist = mc.extrude(curv, [sel[0]], ch=1, rn=0, po=1, et=2, ucp=0, fpt=0, upn=1, rotation=0, scale=1, rsp =1, n='Cable_01')
        mc.setAttr('{}.fixedPath'.format(ext_hist), 1)
        mc.setAttr('nurbsTessellate1.polygonType', 1)
        mc.setAttr('Cable_01.overrideEnabled', 1)
        mc.setAttr('Cable_01.overrideDisplayType', 2)
        cvs = mc.getAttr('{}.cp'.format(sel[0]),s=1)

        spherees = []
        clusters = []
        spherees[:] = []
        clusters[:] = []
        for x in range(int(cvs)):
            mc.select('{}.cv[{}]'.format(sel[0], x) )
            cls, cl_hand = mc.cluster()
            psi = mc.pointPosition( '{}.cv[{}]'.format(sel[0], x) )
            sp, sp_hist = mc.polySphere()
            mc.xform(sp, t=psi, s=(0.3,0.3,0.3))
            mc.parentConstraint(sp, cl_hand)
            spherees.append(sp)
            clusters.append(cl_hand)
        
        mc.aimConstraint(clusters[1], curv, mo=1)
        
        mc.group(spherees, n='Spheres')
        clis_grp = mc.group(clusters, n='Clusters')        
        mc.hide(clis_grp)
        mc.frameLayout(settinglayout, e=1, collapse=0)
    else:
        mc.warning('Select the Curve to create the cable')

def modeltoolsUI():
    '''
    Function to create the UI 
    '''

    if mc.window("modeltools", exists=True, sizeable=True):
        mc.deleteUI("modeltools")


    myWindow = mc.window("modeltools", t="Modeling Tools", w=300, h=300)
   
    mc.shelfLayout()

    mc.iconTextButton( style='iconAndTextVertical', image1='polyMirrorGeometry.png', label='Mirror', h=50, w=50, c="mel.eval('MirrorPolygonGeometry')")
    mc.iconTextButton( style='iconAndTextVertical', image1='multiCut_NEX32.png', label='Mul_Cut', h=50, w=50,c="mel.eval('dR_multiCutTool')")
    mc.iconTextButton( style='iconAndTextVertical', image1='connect_NEX32.png', label='Connect', h=50, w=50,c="mel.eval('dR_connectTool; toolPropertyWindow;')")
    mc.iconTextButton( style='iconAndTextVertical', image1='CenterPivot.png', label='Center Pivot', h=50, w=50,c="mel.eval('CenterPivot')")
    mc.iconTextButton( style='iconAndTextVertical', image1='DeleteHistory.png', label='Dele_H',h=50, w=50,c="mel.eval('DeleteHistory')")
    mc.iconTextButton( style='iconAndTextVertical', image1='FreezeTransform.png', label='Freeze',h=50, w=50,c="mc.makeIdentity(apply=True, t=1, r=1, s=1, n=0)")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyCircularize.png', label='Circ',h=50, w=50,c="mc.polyCircularize()")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyBridge.png', label='Bridge',h=50, w=50,c="mc.polyBridgeEdge()")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyBevel.png', label='Bridge',h=50, w=50,c="mc.polyBevel3()")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyMergeVertex.png', label='Del_Edge',h=50, w=50,c="mc.polyDelEdge(cv=1)")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyNormal.png', label='Reve',h=50, w=50,c="mel.eval('ReversePolygonNormals')")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyHardEdge.png', label='H_Edge',h=50, w=50,c="mel.eval('SoftPolyEdgeElements 0')")
    mc.iconTextButton( style='iconAndTextVertical', image1='polySoftEdge.png', label='S_Edge',h=50, w=50,c="mel.eval('SoftPolyEdgeElements 1')")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyBooleansUnion.png', label='Union',h=50, w=50,c="mc.polyBoolOp(op=1)")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyBooleansDifference.png', label='Diff',h=50, w=50,c="mc.polyBoolOp(op=2)")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyBooleansIntersection.png', label='Inter',h=50, w=50,c="mc.polyBoolOp(op=3)")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyExtrudeFacet.png', label='Extrude',h=50, w=50,c="mc.polyExtrudeFacet()")
    mc.iconTextButton( style='iconAndTextVertical', image1='polySeparate.png', label='Separate',h=50, w=50,c="mc.polySeparate(ch=0, n=mc.ls(sl=1)[0])")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyUnite.png', label='Combine',h=50, w=50,c="mc.polyUnite(ch=0, n=mc.ls(sl=1)[0])")
    mc.iconTextButton( style='iconAndTextVertical', image1='polyCleanup.png', label='CleanUp',h=50, w=50,c="mel.eval('performPolyCleanup 1')")
    mc.setParent( '..' )
    mc.showWindow(myWindow)


