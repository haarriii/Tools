# Autor Harriet Landa Gil 2020


import maya.cmds as mc
from functools import partial
import maya.mel as mel
import json
import os

class ModelMainWindowUI(object):
    '''
    This is a class with an UI (modelUI) that creates a tabs with some riggins tools
    '''
    def modelUI(self):
        '''
        Funcion para crear la ventana con sus tabs y los botones llamando a las funciones
        '''

        if mc.window("ldwin", exists=True, sizeable=True):
            mc.deleteUI("ldwin")


        myWindow = mc.window("ldwin", t="Rigging Tools", w=300, h=300)
        tabs = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
        child1 = mc.shelfLayout( 'Rig Tools' )
        
        mc.iconTextButton( style='iconAndTextVertical', image1='menuIconModify.png', label='M_Tra', h=50, w=50, c=self.matchTranslation)
        mc.iconTextButton( style='iconAndTextVertical', image1='menuIconModify.png', label='M_Rot', h=50, w=50,c=self.matchRotation)
        mc.iconTextButton( style='iconAndTextVertical', image1='menuIconModify.png', label='M_TraRot', h=50, w=50,c=self.matchBoth)
        mc.iconTextButton( style='iconAndTextVertical', image1='menuIconModify.png', label='M_Scl',h=50, w=50,c=self.matchScale)
        mc.iconTextButton( style='iconAndTextVertical', image1='menuIconDisplay.png', label='JS',h=50, w=50,c=self.jointScale)
        mc.iconTextButton( style='iconAndTextVertical', image1='cluster.png', label='Cluster',h=50, w=50,c=self.cluster)
        mc.iconTextButton( style='iconAndTextVertical', image1='menuIconSelect.png', label='Sel Hi',h=50, w=50,c=self.selecHi)
        mc.iconTextButton( style='iconAndTextVertical', image1='kinHandle.png', label='Ik Handle',h=50, w=50,c=self.ikHandle)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='C_OFF',h=50, w=50,c=self.cOffGRP)
        mc.iconTextButton( 'parentCon', style='iconAndTextVertical', image1='parentConstraint.png', label='ParentC',h=50, w=50,c="mel.eval('ParentConstraintOptions')")
        mc.iconTextButton( style='iconAndTextVertical', image1='posConstraint.png', label='PointC',h=50, w=50,c="mel.eval('PointConstraintOptions')")
        mc.iconTextButton( style='iconAndTextVertical', image1='orientConstraint.png', label='OrientC',h=50, w=50,c="mel.eval('OrientConstraintOptions')")
        mc.iconTextButton( style='iconAndTextVertical', image1='scaleConstraint.png', label='ScaleC',h=50, w=50,c="mel.eval('ScaleConstraintOptions')")
        mc.iconTextButton( style='iconAndTextVertical', image1='poleVectorConstraint.png', label='PVC',h=50, w=50,c="mc.poleVectorConstraint(w=1)")
        mc.setParent( '..' )
        mc.setParent( '..' )
        
        child2 = mc.shelfLayout( 'Renamer' )
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='Renamer',h=50, w=50,c=self.renameUI)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='_CTRL',h=50, w=50,c=self.ctrl)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='_GEO',h=50, w=50,c=self.geo)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='_skn_JNT',h=50, w=50,c=self.sknjnt)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='_ik_JNT',h=50, w=50,c=self.ik)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='_fk_JNT',h=50, w=50,c=self.fk)
        mc.setParent( '..' )
        
        child3 = mc.paneLayout( configuration='vertical3' )
        mc.columnLayout()
        self.remvinf = mc.checkBox(l='Remove unused influences',v=1)
        self.bindoption = mc.optionMenu(l='Bind to:')
        mc.menuItem(l='Joints Hierarchy')
        mc.menuItem(l='Selected Joints')
        mc.text(l='Max influences:')
        self.maxinflu = mc.intSliderGrp(f=1, min=1, max=20, v=3)
        mc.setParent('..')
        mc.columnLayout(adj=1)
        mc.separator(h=50, style='none')
        mc.button(l='Bind Skin', h=100, c=self.bindskinG)
        mc.separator(h=50, style='none')
        mc.setParent('..')
        mc.rowColumnLayout(nc=2)
        mc.separator(h=50, style='none')
        mc.separator(h=50, style='none')
     
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='Export Skin Weights',h=50, w=50,c=self.exportWeight)
        mc.iconTextButton( style='iconAndTextVertical', image1='pythonFamily.png', label='Import Skin Weights',h=50, w=50,c=self.setSkin)
        
        mc.setParent( '..' )
        mc.tabLayout(tabs, edit=True,
                 tabLabel=(
                     (child1, 'Rig Tools'), (child2, 'Renamer'), (child3, 'Skinning')))
        mc.showWindow(myWindow)

    ### Creacion de funciones para juntar las transiciones , rotaciones y escalas ###
    def matchTranslation(self):
        sel = mc.ls(sl=True)
        mc.matchTransform(sel[0], sel[1], pos=1)
    
    
    def matchRotation(self):
        sel = mc.ls(sl=True)
        mc.matchTransform(sel[0], sel[1], rot=1)
    
    def matchBoth(self):
        sel = mc.ls(sl=True)
        mc.matchTransform(sel[0], sel[1], pos=1, rot=1)
    
    def matchScale(self):
        sel = mc.ls(sl=True)
        mc.matchTransform(sel[0], sel[1], scl=1)

    ### Ventana donde se puede cambiar el tamano de los joints , llamamos un comando de mel gracias al maya.mel y el mel.eval ###    
    def jointScale(self):
        mel.eval('jdsWin')
    
    ### Varias funciones con simples herramientas o botones utiles ###
    def cluster(self):
        mc.cluster()

    def selecHi(self):
        mc.select(hi=1)

    def ikHandle(self):
        mel.eval('IKHandleToolOptions')
    

    def cOffGRP(self):
        '''
        Funcion para crear un grupo de offset y otro grupo intermedio que se basa en el nombre para crearlos
        '''
        sel = mc.ls(sl=True)

        for each in sel:
            if '_CTRL' in each:
                name = each.replace('_CTRL', '')
                con = mc.group(n='{}_ctrl_CON'.format(name),em = True)
                off = mc.group(n='{}_ctrl_OFF'.format(name),em = True)
                mc.parent(con, off)
                conP = mc.parentConstraint(each, off, mo=False)
                mc.delete(conP)
                mc.parent(each, con)
            else:
                con = mc.group(n='{}_ctrl_CON'.format(each),em = True)
                off = mc.group(n='{}_ctrl_OFF'.format(each),em = True)
                nrename = mc.rename(each, '{}_CTRL'.format(each))
                mc.parent(con, off)
                conP = mc.parentConstraint(nrename, off, mo=False)
                mc.delete(conP)
                mc.parent(nrename, con)

    
    def renameUI(self):
        '''
        Funcion que crea una ventana donde se puede buscar una serie de caracteres para luego renombrarlos
        '''
        if mc.window('renam erUI', exists=True):
            mc.deleteUI('renamerUI')

        mc.window('renamerUI',title='Renamer by Harriet', widthHeight=(400,250))
        main = mc.columnLayout(adj=False)

        mc.rowColumnLayout(numberOfColumns=1)

        self.searchname = mc.textFieldGrp(l='Search Word', editable=True)
        self.replacename = mc.textFieldGrp(l='Replac Word', editable=True)

        mc.button(l='Search and Replace', command=self.rename) 

        mc.showWindow('renamerUI')


    def rename(self, *args):
        
        
        buscaNombre = mc.textFieldGrp( self.searchname, q=True, text=True)
        cambioNombre = mc.textFieldGrp(self.replacename, q=True, text=True)
        print (buscaNombre)

        selection = mc.ls(sl=True)
        
        for each in selection:
            if buscaNombre in each:
                newname = each.replace(buscaNombre, cambioNombre)
                mc.rename(each, newname)
            else:
                print('No existe ese caracter en la seleccion')

    ### Creacion de funciones para anadir los sufijos mas comunes y que se borran al clickar otro sufijo ###   
    
    def ctrl(self):
        selection = mc.ls(sl=True, tr=True)
        for each in selection:
            skn = each.replace('_skn_JNT' , '')
            geo = skn.replace('_GEO' , '')
            ik = geo.replace('_ik_JNT' , '')
            ctrl = ik.replace('_CTRL' , '')
            fk = ctrl.replace('_fk_JNT' , '')
            mc.rename(each, fk + '_CTRL')
    def geo(self):
        selection = mc.ls(sl=True, tr=True)

        for each in selection:
            skn = each.replace('_skn_JNT' , '')
            geo = skn.replace('_GEO' , '')
            ik = geo.replace('_ik_JNT' , '')
            ctrl = ik.replace('_CTRL' , '')
            fk = ctrl.replace('_fk_JNT' , '')
            mc.rename(each, fk + '_GEO')




    def sknjnt(self):
        selection = mc.ls(sl=True, tr=True)
        for each in selection:
            skn = each.replace('_skn_JNT' , '')
            geo = skn.replace('_GEO' , '')
            ik = geo.replace('_ik_JNT' , '')
            ctrl = ik.replace('_CTRL' , '')
            fk = ctrl.replace('_fk_JNT' , '')
            mc.rename(each, fk + '_skn_JNT')
        


    def ik(self):
        selection = mc.ls(sl=True, tr=True)
        for each in selection:
            skn = each.replace('_skn_JNT' , '')
            geo = skn.replace('_GEO' , '')
            ik = geo.replace('_ik_JNT' , '')
            ctrl = ik.replace('_CTRL' , '')
            fk = ctrl.replace('_fk_JNT' , '')
            mc.rename(each, fk + '_ik_JNT')
           

  
    def fk(self):
        selection = mc.ls(sl=True, tr=True)
        for each in selection:
            skn = each.replace('_skn_JNT' , '')
            geo = skn.replace('_GEO' , '')
            ik = geo.replace('_ik_JNT' , '')
            ctrl = ik.replace('_CTRL' , '')
            fk = ctrl.replace('_fk_JNT' , '')
            mc.rename(each, fk + '_fk_JNT')

    ### Creacion de funciones para exportar los pesos de una geo en formato json y en el path elegido por el usuario ###

    def save_file(self):
        ''' 
        Guardar la info dada por otra funcion en el Json
        
        '''
        if not os.path.exists(self.pathWeights):
            mc.error('ERRROR')
        elif self.json_format is None:
            mc.error('VACIO')
            
        file_path = os.path.join(self.pathWeights, self.file_name)
        
        with open(file_path, 'w') as f_out:
            f_out.write(self.json_format)



    
    def exportWeight(self):
        ''' 
        Conseguir los valores de los pesos de cada vertice, 
        meterlos en un diccionario para podemos meterlos en el arhcivo de Json
        
        '''
        projectpath = mc.workspace(q=True, act=True)
        self.pathWeights = mc.fileDialog2(okCaption='Export', fileMode=2)[0]
        
        sel = mc.ls(sl=1)[0]
        self.file_name = '{}_weights.json'.format(sel)
        vertex = mc.polyEvaluate(sel, v=1)
        joints_list = mc.skinCluster(sel, q=1, inf=1)
        vertex_influ = {}
        for x in range(vertex):
            percen = mc.skinPercent( 'skinCluster1', '{}.vtx[{}]'.format(sel, x), query=True, value=True )
            vertex_influ['{}.vtx[{}]'.format(sel, x)] = joints_list , percen

        self.json_format = json.dumps(vertex_influ, separators=(',', ':'), indent=4)
        
        self.save_file()
    
    
    def read_json(self):
        ''' 
        Funcion para poder leer todo lo que hay en el archivo json seleccionado por el usuario
        
        '''
        with open(self.pathWeightsImport, 'r') as f:
            data2 = json.load(f)
        return data2

    
    def setSkin(self):
        ''' 
        Aplicar los valores de los pesos de cada vertice, que estan en el arhcivo json
        
        '''
        self.pathWeightsImport = mc.fileDialog2(okCaption='Import', fileMode=1)[0]
        info = self.read_json()
        
        sel = mc.ls(sl=1)[0]
        vertex = mc.polyEvaluate(sel, v=1)
        joints_list = mc.skinCluster(sel, q=1, inf=1)
        for obj, info  in info.items():
            for x in range(len(joints_list)):
                mc.skinPercent( 'skinCluster1', obj, transformValue=[(info[0][x], info[1][x])])
    
    def bindskinG(self, *args):
        ''' 
        Funcion que al clickar el boton de Bind Skin dependiendo de un checkbox, 
        de un optionmenu y un int slider para poder skinear una geo con joints
        
        '''
        remvinfValue = mc.checkBox(self.remvinf, q=1, v=1)
        bindoptionValue = mc.optionMenu(self.bindoption, q=1, v=1)
        maxinfluValue = mc.intSliderGrp(self.maxinflu, q=1, v=1) 
        
        if bindoptionValue == 'Selected Joints':
            mc.skinCluster(mi=maxinfluValue, sm=1, wd=2, rui=remvinfValue, tsb=True)
        else:
            mc.skinCluster(mi=maxinfluValue, sm=1, wd=2, rui=remvinfValue, tst=False)

    def starUI(self):
        if __name__ == "__main__":
            ui = ModelMainWindowUI()
            ui.modelUI()
        

