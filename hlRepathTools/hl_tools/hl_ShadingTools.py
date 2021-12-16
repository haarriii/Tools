# Autor Harriet Landa Gil 2020

import maya.cmds as mc
from functools import partial
import os

class AutoShaderUI(object):
    def autoShadermainUI(self):
        '''
        This function create the main
        '''
        if mc.window("autoShader", exists=True, sizeable=True):
                mc.deleteUI("autoShader")

        myWindow = mc.window("autoShader", w=300, h=300)
        mc.columnLayout( columnAttach=('both', 1), rowSpacing=10, columnWidth=350, adj=True)
        mc.text(l='The naming must be: tx name + \n UDIM (if have) + _RGB, _SPCR, _SSS, _NRM, _DSPL')
        mc.text(label='Shader Name')
        self.shadername = mc.textField()
        ### checkbox to add UDIMS to the texture ###
        self.udimcheck = mc.checkBox('udims', l='UDIMS')
        mc.button(l='Select Textures Folder', command=self.folderbrw)
        mc.button(l='Create Shaders', command=self.shaderCreation)
        mc.text(l='Base Color')
        self.basecolorpath = mc.textFieldButtonGrp( buttonLabel='...') 
        mc.textFieldButtonGrp(self.basecolorpath, e=1, bc=self.rgbpathchange)
        mc.text(l='SPCR')
        self.spcrpath = mc.textFieldButtonGrp( buttonLabel='...') 
        mc.textFieldButtonGrp(self.spcrpath, e=1, bc=self.spcrpathchange)
        mc.text(l='SSS')
        self.ssspath = mc.textFieldButtonGrp( buttonLabel='...') 
        mc.textFieldButtonGrp(self.ssspath, e=1, bc=self.ssspathchange)
        mc.text(l='NRM')
        self.nrmpath = mc.textFieldButtonGrp( buttonLabel='...')
        mc.textFieldButtonGrp(self.nrmpath, e=1, bc=self.nrmpathchange)
        mc.text(l='DSPL')
        self.dsplpath = mc.textFieldButtonGrp( buttonLabel='...') 
        mc.textFieldButtonGrp(self.dsplpath, e=1, bc=self.dsplpathchange) 
        mc.showWindow(myWindow)
    

    def folderbrw(self, *args):
        '''
        Select the folder and add the name of the textures to the textField in the UI
        '''
        proj = mc.fileDialog2(cap='Select Character Textures Folder', dialogStyle=2, fm=3)
        texfolder = str(proj[0]).split('/')
        sourceindex = texfolder.index('sourceimages')
        characterfoldername = texfolder[int(texfolder.index('sourceimages'))+1]
        mc.textFieldButtonGrp( self.basecolorpath, e=1, text='{}/{}_RGB'.format(proj[0], characterfoldername)) 
        mc.textFieldButtonGrp( self.spcrpath, e=1, text='{}/{}_SPCR'.format(proj[0], characterfoldername)) 
        mc.textFieldButtonGrp( self.ssspath , e=1, text='{}/{}_SSS'.format(proj[0], characterfoldername)) 
        mc.textFieldButtonGrp( self.nrmpath, e=1, text='{}/{}_NRM'.format(proj[0], characterfoldername)) 
        mc.textFieldButtonGrp( self.dsplpath, e=1, text='{}/{}_DSPL'.format(proj[0], characterfoldername)) 
        ### print the path to get sure of it ###
        print(proj[0])

    ### Some functions to change the path of the textFields if they are wrong ###
    def rgbpathchange(self, *args):
        newpath = mc.fileDialog2(dialogStyle=2, okCaption='Change')[0]
        print(newpath)
        mc.textFieldButtonGrp( self.basecolorpath, e=1, text=newpath)
    
    def spcrpathchange(self, *args):
        newpath = mc.fileDialog2(dialogStyle=2, okCaption='Change')[0]
        mc.textFieldButtonGrp( self.spcrpath, e=1, text=newpath)
   
    def ssspathchange(self, *args):
        newpath = mc.fileDialog2(dialogStyle=2, okCaption='Change')[0]
        mc.textFieldButtonGrp( self.ssspath, e=1, text=newpath)
  
    def nrmpathchange(self, *args):
        newpath = mc.fileDialog2(dialogStyle=2, okCaption='Change')[0]
        mc.textFieldButtonGrp( self.nrmpath, e=1, text=newpath)
  
    def dsplpathchange(self, *args):
        newpath = mc.fileDialog2(dialogStyle=2, okCaption='Change')[0]
        mc.textFieldButtonGrp( self.dsplpath, e=1, text=newpath)


    def shaderCreation(self, *args):
        '''
        Check if the Udim checkbox is on or off and depending of this , create the shader by the name gived on the top of the UI
        '''

        udimcheckVal = mc.checkBox(self.udimcheck, q=1, v=1 )
        if not udimcheckVal:
            
            projectpath = mc.workspace(q=True, rd=True)
            sel = mc.ls(sl=True)
            shadername = mc.textField(self.shadername, q=1, text=1)
            
            shader = mc.shadingNode('aiStandardSurface', name=shadername  + '_SHD', asShader=True)
            mc.select(sel)
            mc.hyperShade(assign=shader)
            mc.rename(str(shader) + 'SG', shadername + '_SG')
            
            place2d = mc.shadingNode("place2dTexture",asUtility=True)
            placeAttribList = mc.listAttr(place2d)
            placeAttribList.pop(0)
            del placeAttribList[4:8:1]
            del placeAttribList[-8:-1:1]
            ###            RGB
            
            rgbpath = mc.textFieldButtonGrp(self.basecolorpath, q=1, text=1)
            if os.path.exists('{}.exr'.format(rgbpath)):
                goodrgbpath = '{}.exr'.format(rgbpath)
                RGB = mc.shadingNode("file",asTexture=True)
                mc.setAttr(RGB + '.fileTextureName', goodrgbpath, type='string')
                mc.setAttr(RGB + '.colorSpace', 'sRGB', type='string')
                mc.connectAttr(RGB + '.outColor', shader + '.baseColor')
                mc.connectAttr(place2d + '.outUV', RGB + '.uvCoord')
                
                
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, RGB + '.' + each)
                    continue
            else:
                mc.warning('{}.exr NOT EXITS'.format(rgbpath))
                
            

            ###            SPCR
            
            spcrpath = mc.textFieldButtonGrp(self.spcrpath, q=1, text=1)
            if os.path.exists('{}.exr'.format(spcrpath)):
                goodspcrpath = '{}.exr'.format(spcrpath)
                SPCR = mc.shadingNode("file",asTexture=True)
                mc.setAttr(SPCR + '.fileTextureName', goodspcrpath, type='string')
                mc.setAttr(SPCR + '.colorSpace', 'sRGB', type='string')
                mc.setAttr(SPCR + '.alphaIsLuminance', 1)
                mc.connectAttr(SPCR + '.outAlpha', shader + '.specularRoughness')
                mc.connectAttr(place2d + '.outUV', SPCR + '.uvCoord')
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, SPCR + '.' + each)
                    continue
            
            else:
                mc.warning('{}.exr NOT EXITS'.format(spcrpath))
                
            ###            SSS
            ssspath = mc.textFieldButtonGrp(self.ssspath, q=1, text=1)
            if os.path.exists('{}.exr'.format(ssspath)):
                goodssspath = '{}.exr'.format(ssspath)
                SSS = mc.shadingNode("file",asTexture=True)
                mc.setAttr(SSS + '.fileTextureName', goodssspath, type='string')
                mc.setAttr(SSS + '.colorSpace', 'sRGB', type='string')
                mc.setAttr(SSS + '.alphaIsLuminance', 1)
                mc.connectAttr(SSS + '.outColor', shader + '.subsurfaceColor')
                mc.connectAttr(place2d + '.outUV', SSS + '.uvCoord')
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, SSS + '.' + each)
                    continue
            
            else:
                mc.warning('{}.exr NOT EXITS'.format(ssspath))
            
            ###            NRM
            nrmpath = mc.textFieldButtonGrp(self.nrmpath, q=1, text=1)
            if os.path.exists('{}.exr'.format(nrmpath)):
                goodnrmpath = '{}.exr'.format(nrmpath)
                NRM = mc.shadingNode("file",asTexture=True)
                mc.setAttr(NRM + '.fileTextureName', goodnrmpath, type='string')
                mc.setAttr(NRM + '.colorSpace', 'sRGB', type='string')
                #mc.connectAttr(NRM + '.outColor', shader + '.baseColor')
                mc.connectAttr(place2d + '.outUV', NRM + '.uvCoord')
                
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, NRM + '.' + each)
                    continue
                
                nrmnode = mc.shadingNode('aiNormalMap', asShader=True)
                mc.connectAttr(NRM + '.outColor', nrmnode + '.input')
                mc.connectAttr(nrmnode + '.outValue', shader + '.normalCamera')
            else:
                mc.warning('{}.exr NOT EXITS'.format(nrmpath))
                
            
            
            
            
            
            ###            DSPL
            dsplpath = mc.textFieldButtonGrp(self.dsplpath, q=1, text=1)
            
            if os.path.exists('{}.exr'.format(dsplpath)):
                gooddsplpath = '{}.exr'.format(dsplpath)
                DSPL = mc.shadingNode("file",asTexture=True)
                mc.setAttr(DSPL + '.fileTextureName', gooddsplpath , type='string')
                mc.setAttr(DSPL + '.colorSpace', 'Raw', type='string')
                mc.setAttr(DSPL + '.alphaIsLuminance', 1)
                #mc.connectAttr(DSPL + '.outAlpha', shader + '.specularRoughness')
                mc.connectAttr(place2d + '.outUV', DSPL + '.uvCoord')
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, DSPL + '.' + each)
                    continue
                
                
                dispshader = mc.shadingNode('displacementShader', asShader=True)
                
                mc.connectAttr(DSPL + '.outAlpha', dispshader + '.displacement')
                
                mc.connectAttr(dispshader + '.displacement', shadername + '_SG' + '.displacementShader')
            else:
                mc.warning('{}.exr NOT EXITS'.format(dsplpath))
        else:
            
            projectpath = mc.workspace(q=True, rd=True)
            sel = mc.ls(sl=True)
            shadername = mc.textField(self.shadername, q=1, text=1)
            
            shader = mc.shadingNode('aiStandardSurface', name=shadername  + '_SHD', asShader=True)
            mc.select(sel)
            mc.hyperShade(assign=shader)
            mc.rename(str(shader) + 'SG', shadername + '_SG')
            
            place2d = mc.shadingNode("place2dTexture",asUtility=True)
            placeAttribList = mc.listAttr(place2d)
            placeAttribList.pop(0)
            del placeAttribList[4:8:1]
            del placeAttribList[-8:-1:1]
            ###            RGB
            
            rgbpath = mc.textFieldButtonGrp(self.basecolorpath, q=1, text=1)
            if os.path.exists('{}.exr'.format(rgbpath)):
                goodrgbpath = '{}_<UDIM>.exr'.format(rgbpath)
                RGB = mc.shadingNode("file",asTexture=True)
                mc.setAttr(RGB + '.uvTilingMode', 3)
                mc.setAttr(RGB + '.fileTextureName', goodrgbpath, type='string')
                mc.setAttr(RGB + '.colorSpace', 'sRGB', type='string')
                mc.connectAttr(RGB + '.outColor', shader + '.baseColor')
                mc.connectAttr(place2d + '.outUV', RGB + '.uvCoord')
                
                
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, RGB + '.' + each)
                    continue
            else:
                mc.warning('{}.exr NOT EXITS'.format(rgbpath))
                
            

            ###            SPCR
            
            spcrpath = mc.textFieldButtonGrp(self.spcrpath, q=1, text=1)
            if os.path.exists('{}.exr'.format(spcrpath)):
                goodspcrpath = '{}_<UDIM>.exr'.format(spcrpath)
                SPCR = mc.shadingNode("file",asTexture=True)
                mc.setAttr(SPCR + '.uvTilingMode', 3)
                mc.setAttr(SPCR + '.fileTextureName', goodspcrpath, type='string')
                mc.setAttr(SPCR + '.colorSpace', 'sRGB', type='string')
                mc.setAttr(SPCR + '.alphaIsLuminance', 1)
                mc.connectAttr(SPCR + '.outAlpha', shader + '.specularRoughness')
                mc.connectAttr(place2d + '.outUV', SPCR + '.uvCoord')
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, SPCR + '.' + each)
                    continue
            
            else:
                mc.warning('{}.exr NOT EXITS'.format(spcrpath))
                
            ###            SSS
            ssspath = mc.textFieldButtonGrp(self.ssspath, q=1, text=1)
            if os.path.exists('{}.exr'.format(ssspath)):
                goodssspath = '{}_<UDIM>.exr'.format(ssspath)
                SSS = mc.shadingNode("file",asTexture=True)
                mc.setAttr(SSS + '.uvTilingMode', 3)
                mc.setAttr(SSS + '.fileTextureName', goodssspath, type='string')
                mc.setAttr(SSS + '.colorSpace', 'sRGB', type='string')
                mc.setAttr(SSS + '.alphaIsLuminance', 1)
                mc.connectAttr(SSS + '.outColor', shader + '.subsurfaceColor')
                mc.connectAttr(place2d + '.outUV', SSS + '.uvCoord')
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, SSS + '.' + each)
                    continue
            
            else:
                mc.warning('{}.exr NOT EXITS'.format(ssspath))
            
            ###            NRM
            nrmpath = mc.textFieldButtonGrp(self.nrmpath, q=1, text=1)
            if os.path.exists('{}.exr'.format(nrmpath)):
                goodnrmpath = '{}_<UDIM>.exr'.format(nrmpath)
                NRM = mc.shadingNode("file",asTexture=True)
                mc.setAttr(NRM + '.uvTilingMode', 3)
                mc.setAttr(NRM + '.fileTextureName', goodnrmpath, type='string')
                mc.setAttr(NRM + '.colorSpace', 'sRGB', type='string')
                #mc.connectAttr(NRM + '.outColor', shader + '.baseColor')
                mc.connectAttr(place2d + '.outUV', NRM + '.uvCoord')
                
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, NRM + '.' + each)
                    continue
                
                nrmnode = mc.shadingNode('aiNormalMap', asShader=True)
                mc.connectAttr(NRM + '.outColor', nrmnode + '.input')
                mc.connectAttr(nrmnode + '.outValue', shader + '.normalCamera')
            else:
                mc.warning('{}.exr NOT EXITS'.format(nrmpath))

            
            
            ###            DSPL
            dsplpath = mc.textFieldButtonGrp(self.dsplpath, q=1, text=1)
            
            if os.path.exists('{}.exr'.format(dsplpath)):
                gooddsplpath = '{}_<UDIM>.exr'.format(dsplpath)
                DSPL = mc.shadingNode("file",asTexture=True)
                mc.setAttr(DSPL + '.uvTilingMode', 3)
                mc.setAttr(DSPL + '.fileTextureName', gooddsplpath , type='string')
                mc.setAttr(DSPL + '.colorSpace', 'Raw', type='string')
                mc.setAttr(DSPL + '.alphaIsLuminance', 1)
                #mc.connectAttr(DSPL + '.outAlpha', shader + '.specularRoughness')
                mc.connectAttr(place2d + '.outUV', DSPL + '.uvCoord')
                for each in placeAttribList:
                    mc.connectAttr(place2d + '.' + each, DSPL + '.' + each)
                    continue
                
                
                dispshader = mc.shadingNode('displacementShader', asShader=True)
                
                mc.connectAttr(DSPL + '.outAlpha', dispshader + '.displacement')
                
                mc.connectAttr(dispshader + '.displacement', shadername + '_SG' + '.displacementShader')
            else:
                mc.warning('{}.exr NOT EXITS'.format(dsplpath))
            





    