# Autor Harriet Landa Gil 2020

import maya.cmds as mc
import mtoa.ui.arnoldmenu as arnoldmenu
import pymel.core as pm
from functools import partial



### Some funtions thats change the render settigns with an optionMeny or a textField ###
def name_Out(file_OUT, *args):
    filename = mc.textField(file_OUT, q=1, text=1)
    print(filename)
    mc.setAttr('defaultRenderGlobals.imageFilePrefix', filename, type="string")


def render_Form(item, *args):
    # print item
    form = mc.optionMenu(item, q=1, v=1)
    mc.setAttr('defaultArnoldDriver.ai_translator', form, type='string')


def render_Ext(item,  sf, ef, *args):
    '''
    Change the render format
    '''
    padding = mc.optionMenu(item, q=1, v=1)
    ### change the render format depending the optionMenu ###
    if padding == 'name_#.ext':
        mc.textFieldGrp(sf, e=1, enable=1)
        mc.textFieldGrp(ef, e=1, enable=1)
        mc.setAttr('defaultRenderGlobals.outFormatControl', 0)
        mc.setAttr('defaultRenderGlobals.animation', 1)
    elif padding == 'name.ext (Single Frame)':
        mc.textFieldGrp(sf, e=1, enable=0)
        mc.textFieldGrp(ef, e=1, enable=0)
        mc.setAttr('defaultRenderGlobals.outFormatControl', 0)
        mc.setAttr('defaultRenderGlobals.animation', 0)


def rendRes(item, *args):
    '''
    Change the render resolution to some presets
    '''
    resolution = mc.optionMenu(item, q=1, v=1)
    if resolution == 'HD_1080':
        mc.setAttr('defaultResolution.width', 1920)
        mc.setAttr('defaultResolution.height', 1080)
    elif resolution == 'HD_720':
        mc.setAttr('defaultResolution.width', 1280)
        mc.setAttr('defaultResolution.height', 720)
    elif resolution == 'Proxy_540':
        mc.setAttr('defaultResolution.width', 960)
        mc.setAttr('defaultResolution.height', 540)

def nameRenderLayer(file_OUT, *args):
    ### add <renderlayer> to the name with right click###
    text = mc.textField(file_OUT, q=1, text=1)
    mc.textField(file_OUT, e=1, text='{}_<RenderLayer>_'.format(text))

def nameCamera(file_OUT, *args):
     ### add <camera> to the name with right click###
    text = mc.textField(file_OUT, q=1, text=1)
    mc.textField(file_OUT, e=1, text='{}_<Camera>_'.format(text))



### Checkbox to merge the AOV in the render file ###
def mergeaovs(mrg, *args):
    valormergeaovs = mc.checkBox(mrg, q=True, value=True)
    ### if valormerge aovs is true, the merge aovs checkbox change to active ###
    if (valormergeaovs == True):
        mc.setAttr('defaultArnoldDriver.mergeAOVs', 1)
    else:
        mc.setAttr('defaultArnoldDriver.mergeAOVs', 0)

### start and enf frame fields ###
def startFrame(sf, *args):
    s = mc.textFieldGrp(sf, q=True, text=True)
    mc.setAttr('defaultRenderGlobals.startFrame', s)


def endFrame(ef, *args):
    e = mc.textFieldGrp(ef, q=True, text=True)
    mc.setAttr('defaultRenderGlobals.endFrame', e)

### open the arnold renderview to view the render ###
def render_Out(*args):
    arnoldmenu.arnoldMtoARenderView()

### Checkbox to get the arnold denoise aov in the output ###
def arnoldDenoise(arnoldDenoiser, *args):
    valorDenoiser = mc.checkBox(arnoldDenoiser, q=True, value=True)
    if valorDenoiser == True:
        mc.setAttr('defaultArnoldRenderOptions.outputVarianceAOVs', 1)
    else:
        mc.setAttr('defaultArnoldRenderOptions.outputVarianceAOVs', 0)

### Checkbox to skip frames if they exists ###
def skipFrames(skp, *args):
    valorskip = mc.checkBox(skp, q=True, value=True)
    if (valorskip == True):
        mc.setAttr('defaultRenderGlobals.skipExistingFrames', 1)
    else:
        mc.setAttr('defaultRenderGlobals.skipExistingFrames', 0)

### Sliders to change the Sampling ###
def apply_RS(aACamera, diffuse, specular, transmission, sss, volume, *args):
    v_aaCam = mc.intSliderGrp(aACamera, q=True, value=True)
    v_Diff = mc.intSliderGrp(diffuse, q=True, value=True)
    v_Spcr = mc.intSliderGrp(specular, q=True, value=True)
    v_Transs = mc.intSliderGrp(transmission, q=True, value=True)
    v_SSS = mc.intSliderGrp(sss, q=True, value=True)
    v_vol = mc.intSliderGrp(volume, q=True, value=True)
    mc.setAttr('defaultArnoldRenderOptions.AASamples', v_aaCam)
    mc.setAttr('defaultArnoldRenderOptions.GIDiffuseSamples', v_Diff)
    mc.setAttr('defaultArnoldRenderOptions.GISpecularSamples', v_Spcr)
    mc.setAttr('defaultArnoldRenderOptions.GITransmissionSamples', v_Transs)
    mc.setAttr('defaultArnoldRenderOptions.GISssSamples', v_SSS)
    mc.setAttr('defaultArnoldRenderOptions.GIVolumeSamples', v_vol)

def adapSam(adaptaive , *args):
    adapV = mc.checkBox(adaptaive, q=1, v=1)
    if adapV:
        mc.setAttr("defaultArnoldRenderOptions.enableAdaptiveSampling", 1)
    else:
        mc.setAttr("defaultArnoldRenderOptions.enableAdaptiveSampling", 0)


### Some functions to create and apply the most used AOVs by the node editor ###
def rGBA_AOV(rgback, *args):
    valorRGBA = mc.checkBox(rgback, q=True, value=True)
    if (valorRGBA == True):
        mc.createNode("aiAOV", name='aiAOV_RGBA')
        mc.connectAttr('aiAOV_RGBA.message',
                       'defaultArnoldRenderOptions.aovList[1]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_RGBA.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_RGBA.outputs[0].driver')
        mc.setAttr('aiAOV_RGBA.name', 'RGBA', type="string")
    else:
        mc.disconnectAttr('aiAOV_RGBA.message',
                          'defaultArnoldRenderOptions.aovList[1]')
        mc.delete('aiAOV_RGBA')


def diffIn_AOV(dif_inck, *args):
    valordiffin = mc.checkBox(dif_inck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_diffuse_indirect')
        mc.connectAttr('aiAOV_diffuse_indirect.message',
                       'defaultArnoldRenderOptions.aovList[2]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_diffuse_indirect.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_diffuse_indirect.outputs[0].driver')
        mc.setAttr('aiAOV_diffuse_indirect.name',
                   'diffuse_indirect', type="string")
    else:
        mc.disconnectAttr('aiAOV_diffuse_indirect.message',
                          'defaultArnoldRenderOptions.aovList[2]')
        mc.delete('aiAOV_diffuse_indirect')


def diffDir_AOV(dif_dirck, *args):
    valordiffin = mc.checkBox(dif_dirck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_diffuse_direct')
        mc.connectAttr('aiAOV_diffuse_direct.message',
                       'defaultArnoldRenderOptions.aovList[3]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_diffuse_direct.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_diffuse_direct.outputs[0].driver')
        mc.setAttr('aiAOV_diffuse_direct.name',
                   'diffuse_direct', type="string")
    else:
        mc.disconnectAttr('aiAOV_diffuse_direct.message',
                          'defaultArnoldRenderOptions.aovList[3]')
        mc.delete('aiAOV_diffuse_direct')


def z_AOV(zck, *args):
    valorZ = mc.checkBox(zck, q=True, value=True)
    if (valorZ == True):
        mc.createNode("aiAOV", name='aiAOV_Z')
        mc.createNode("aiAOVFilter", name='aiAOVFilter_Z')
        mc.setAttr('aiAOV_Z.type', 4)
        mc.setAttr('aiAOVFilter_Z.ai_translator', 'closest', type='string')
        mc.connectAttr('aiAOV_Z.message',
                       'defaultArnoldRenderOptions.aovList[4]')
        mc.connectAttr('aiAOVFilter_Z.message', 'aiAOV_Z.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_Z.outputs[0].driver')
        mc.setAttr('aiAOV_Z.name', 'Z', type="string")
    else:
        mc.disconnectAttr('aiAOV_Z.message',
                          'defaultArnoldRenderOptions.aovList[4]')
        mc.delete('aiAOV_Z')


def emission_AOV(emick, *args):
    valorEmis = mc.checkBox(emick, q=True, value=True)
    if (valorEmis == True):
        mc.createNode("aiAOV", name='aiAOV_emission')
        mc.connectAttr('aiAOV_emission.message',
                       'defaultArnoldRenderOptions.aovList[5]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_emission.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_emission.outputs[0].driver')
        mc.setAttr('aiAOV_emission.name', 'emission', type="string")
    else:
        mc.disconnectAttr('aiAOV_emission.message',
                          'defaultArnoldRenderOptions.aovList[5]')
        mc.delete('aiAOV_emission')


def sdw_Matte_AOV(shw_ck, *args):
    valordiffin = mc.checkBox(shw_ck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_shadow_matte')
        mc.connectAttr('aiAOV_shadow_matte.message',
                       'defaultArnoldRenderOptions.aovList[6]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_shadow_matte.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_shadow_matte.outputs[0].driver')
        mc.setAttr('aiAOV_shadow_matte.name', 'shadow_matte', type="string")
    else:
        mc.disconnectAttr('aiAOV_shadow_matte.message',
                          'defaultArnoldRenderOptions.aovList[6]')
        mc.delete('aiAOV_shadow_matte')


def spcDir_AOV(spc_dirck, *args):
    valordiffin = mc.checkBox(spc_dirck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_specular_direct')
        mc.connectAttr('aiAOV_specular_direct.message',
                       'defaultArnoldRenderOptions.aovList[7]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_specular_direct.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_specular_direct.outputs[0].driver')
        mc.setAttr('aiAOV_specular_direct.name',
                   'specular_direct', type="string")
    else:
        mc.disconnectAttr('aiAOV_specular_direct.message',
                          'defaultArnoldRenderOptions.aovList[7]')
        mc.delete('aiAOV_specular_direct')


def spcIn_AOV(spc_inck, *args):
    valordiffin = mc.checkBox(spc_inck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_specular_indirect')
        mc.connectAttr('aiAOV_specular_indirect.message',
                       'defaultArnoldRenderOptions.aovList[8]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_specular_indirect.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_specular_indirect.outputs[0].driver')
        mc.setAttr('aiAOV_specular_indirect.name',
                   'specular_indirect', type="string")
    else:
        mc.disconnectAttr('aiAOV_specular_indirect.message',
                          'defaultArnoldRenderOptions.aovList[8]')
        mc.delete('aiAOV_specular_indirect')


def sSSDir_AOV(sss_dirck, *args):
    valordiffin = mc.checkBox(sss_dirck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_sss_direct')
        mc.connectAttr('aiAOV_sss_direct.message',
                       'defaultArnoldRenderOptions.aovList[9]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_sss_direct.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_sss_direct.outputs[0].driver')
        mc.setAttr('aiAOV_sss_direct.name', 'sss_direct', type="string")
    else:
        mc.disconnectAttr('aiAOV_sss_direct.message',
                          'defaultArnoldRenderOptions.aovList[9]')
        mc.delete('aiAOV_sss_direct')


def sSSIn_AOV(sss_inck, *args):
    valordiffin = mc.checkBox(sss_inck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_sss_indirect')
        mc.connectAttr('aiAOV_sss_indirect.message',
                       'defaultArnoldRenderOptions.aovList[10]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_sss_indirect.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_sss_indirect.outputs[0].driver')
        mc.setAttr('aiAOV_sss_indirect.name', 'sss_indirect', type="string")
    else:
        mc.disconnectAttr('aiAOV_sss_indirect.message',
                          'defaultArnoldRenderOptions.aovList[10]')
        mc.delete('aiAOV_sss_indirect')


def tsIN_AOV(t_inck, *args):
    valordiffin = mc.checkBox(t_inck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_transmission_indirect')
        mc.connectAttr('aiAOV_transmission_indirect.message',
                       'defaultArnoldRenderOptions.aovList[11]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_transmission_indirect.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_transmission_indirect.outputs[0].driver')
        mc.setAttr('aiAOV_transmission_indirect.name',
                   'transmission_indirect', type="string")
    else:
        mc.disconnectAttr('aiAOV_transmission_indirect.message',
                          'defaultArnoldRenderOptions.aovList[11]')
        mc.delete('aiAOV_transmission_indirect')


def tsDir_AOV(t_dirck, *args):
    valordiffin = mc.checkBox(t_dirck, q=True, value=True)
    if (valordiffin == True):
        mc.createNode("aiAOV", name='aiAOV_transmission_direct')
        mc.connectAttr('aiAOV_transmission_direct.message',
                       'defaultArnoldRenderOptions.aovList[12]')
        mc.connectAttr('defaultArnoldFilter.message',
                       'aiAOV_transmission_direct.outputs[0].filter')
        mc.connectAttr('defaultArnoldDriver.message',
                       'aiAOV_transmission_direct.outputs[0].driver')
        mc.setAttr('aiAOV_transmission_direct.name',
                   'transmission_direct', type="string")
    else:
        mc.disconnectAttr('aiAOV_transmission_direct.message',
                          'defaultArnoldRenderOptions.aovList[12]')
        mc.delete('aiAOV_transmission_direct')


def cryObj_AOV(cryp_obj, *args):
    valordiffin = mc.checkBox(cryp_obj, q=True, value=True)
    if (valordiffin == True):
        if mc.objExists('_aov_cryptomatte'):
            mc.createNode("aiAOV", name='aiAOV_crypto_object')
            mc.connectAttr('aiAOV_crypto_object.message',
                        'defaultArnoldRenderOptions.aovList[13]')
            mc.connectAttr('defaultArnoldFilter.message',
                        'aiAOV_crypto_object.outputs[0].filter')
            mc.connectAttr('defaultArnoldDriver.message',
                        'aiAOV_crypto_object.outputs[0].driver')
            mc.connectAttr('_aov_cryptomatte.outColor',
                        'aiAOV_crypto_object.defaultValue')
            mc.setAttr('aiAOV_crypto_object.name', 'crypto_object', type="string")
        else:
            mc.createNode("cryptomatte", name='_aov_cryptomatte')
            mc.createNode("aiAOV", name='aiAOV_crypto_object')
            mc.connectAttr('aiAOV_crypto_object.message',
                        'defaultArnoldRenderOptions.aovList[13]')
            mc.connectAttr('defaultArnoldFilter.message',
                        'aiAOV_crypto_object.outputs[0].filter')
            mc.connectAttr('defaultArnoldDriver.message',
                        'aiAOV_crypto_object.outputs[0].driver')
            mc.connectAttr('_aov_cryptomatte.outColor',
                        'aiAOV_crypto_object.defaultValue')
            mc.setAttr('aiAOV_crypto_object.name', 'crypto_object', type="string")
    else:
        mc.disconnectAttr('aiAOV_crypto_object.message',
                          'defaultArnoldRenderOptions.aovList[13]')
        mc.delete('aiAOV_crypto_object')



def cryMtl_AOV(cryp_mtl, *args):
    valordiffin = mc.checkBox(cryp_mtl, q=True, value=True)
    if (valordiffin == True):
        if mc.objExists('_aov_cryptomatte'):
            mc.createNode("aiAOV", name='aiAOV_crypto_material')
            mc.connectAttr('aiAOV_crypto_material.message',
                        'defaultArnoldRenderOptions.aovList[14]')
            mc.connectAttr('defaultArnoldFilter.message',
                        'aiAOV_crypto_material.outputs[0].filter')
            mc.connectAttr('defaultArnoldDriver.message',
                        'aiAOV_crypto_material.outputs[0].driver')
            mc.connectAttr('_aov_cryptomatte.outColor',
                        'aiAOV_crypto_material.defaultValue')
            mc.setAttr('aiAOV_crypto_material.name', 'crypto_material', type="string")
            mc.setAttr('aiAOV_crypto_material.type', 5)
        else:
            mc.createNode("cryptomatte", name='_aov_cryptomatte')
            mc.createNode("aiAOV", name='aiAOV_crypto_material')
            mc.connectAttr('aiAOV_crypto_material.message',
                        'defaultArnoldRenderOptions.aovList[14]')
            mc.connectAttr('defaultArnoldFilter.message',
                        'aiAOV_crypto_material.outputs[0].filter')
            mc.connectAttr('defaultArnoldDriver.message',
                        'aiAOV_crypto_material.outputs[0].driver')
            mc.connectAttr('_aov_cryptomatte.outColor',
                        'aiAOV_crypto_material.defaultValue')
            mc.setAttr('aiAOV_crypto_material.name', 'crypto_material', type="string")
            mc.setAttr('aiAOV_crypto_material.type', 5)
    else:
        mc.disconnectAttr('aiAOV_crypto_material.message',
                          'defaultArnoldRenderOptions.aovList[14]')
        mc.delete('aiAOV_crypto_material')

 
def cryASS_AOV(cryp_ass, *args):
    valordiffin = mc.checkBox(cryp_ass, q=True, value=True)
    if (valordiffin == True):
        if mc.objExists('_aov_cryptomatte'):
            mc.createNode("aiAOV", name='aiAOV_crypto_asset')
            mc.connectAttr('aiAOV_crypto_asset.message',
                        'defaultArnoldRenderOptions.aovList[15]')
            mc.connectAttr('defaultArnoldFilter.message',
                        'aiAOV_crypto_asset.outputs[0].filter')
            mc.connectAttr('defaultArnoldDriver.message',
                        'aiAOV_crypto_asset.outputs[0].driver')
            mc.connectAttr('_aov_cryptomatte.outColor',
                        'aiAOV_crypto_asset.defaultValue')
            mc.setAttr('aiAOV_crypto_asset.name', 'crypto_material', type="string")
            mc.setAttr('aiAOV_crypto_asset.type', 5)
        else:
            mc.createNode("cryptomatte", name='_aov_cryptomatte')
            mc.createNode("aiAOV", name='aiAOV_crypto_asset')
            mc.connectAttr('aiAOV_crypto_asset.message',
                        'defaultArnoldRenderOptions.aovList[15]')
            mc.connectAttr('defaultArnoldFilter.message',
                        'aiAOV_crypto_asset.outputs[0].filter')
            mc.connectAttr('defaultArnoldDriver.message',
                        'aiAOV_crypto_asset.outputs[0].driver')
            mc.connectAttr('_aov_cryptomatte.outColor',
                        'aiAOV_crypto_asset.defaultValue')
            mc.setAttr('aiAOV_crypto_asset.name', 'crypto_material', type="string")
            mc.setAttr('aiAOV_crypto_asset.type', 5)
    else:
        mc.disconnectAttr('aiAOV_crypto_asset.message',
                          'defaultArnoldRenderOptions.aovList[15]')
        mc.delete('aiAOV_crypto_asset')       

### Create a new cam called RenderCam ###
def createCam(*args):
    cam = mc.camera(name='RenderCam')
    cam1 = mc.select(cam)
    mc.rename(cam1, 'RenderCam')

def renderSetupUI():
    '''
    The main function , creates a UI with all the settings to change 
    '''
    if mc.window("render", exists=True, sizeable=True):
        mc.deleteUI('render')

    myWindow = mc.window(
        "render", t="Render Setup", w=300, h=300)

    mc.columnLayout(adj=True)

    mc.text("Render Settings", backgroundColor=[1, 1, 1], height=20, width=20)

    mc.text(l='File Name')
    file_OUT = mc.textField('File_Name_Output', editable=True)
    mc.popupMenu()
    mc.menuItem(l='<RenderLayer>', c=partial(nameRenderLayer, file_OUT))
    mc.menuItem(l='<Camera>', c=partial(nameCamera, file_OUT))
    mc.button(h=30, l="Name File Output", command=partial(name_Out, file_OUT))

    mrg = mc.checkBox('MergeAOVS', label='Merge AOVs', value=0)
    mc.checkBox(mrg, e=1, cc=partial(mergeaovs, mrg))

    renderForm = mc.optionMenu(label='Render Formats')
    mc.menuItem(label='exr')
    mc.menuItem(label='png')
    mc.menuItem(label='jpeg')
    mc.optionMenu(renderForm, e=1, cc=partial(render_Form, renderForm))

    padding = mc.optionMenu(label='Render Ext', changeCommand=render_Ext)
    mc.menuItem(label='name.ext (Single Frame)')
    mc.menuItem(label='name_#.ext')
    
    
    sf = mc.textFieldGrp(l='Start Frame', editable=True, enable=0)
    mc.textFieldGrp(sf, e=1, changeCommand=partial(startFrame, sf))

    ef = mc.textFieldGrp(l='End Frame', editable=True, enable=0)
    mc.textFieldGrp(ef, e=1, cc=partial(endFrame, ef))
    
    mc.optionMenu(padding, e=1, cc=partial(render_Ext, padding, sf, ef))

    skp = mc.checkBox('SkipFrames', label='Skip existing Frames', value=0)
    mc.checkBox(skp, e=1, changeCommand=partial(skipFrames, skp))

    mc.separator(h=5, style='double')

    mc.button(l='Create Render Camera', command=partial(createCam))

    mc.separator(h=5, style='double')


    renderRes = mc.optionMenu(label='Render Resolution')
    mc.menuItem(label='HD_1080')
    mc.menuItem(label='HD_720')
    mc.menuItem(label='Proxy_540')
    mc.optionMenu(renderRes, e=1, cc=partial(rendRes, renderRes))
    mc.text("Arnold Renderer", backgroundColor=[1, 1, 1], height=20, width=20)

    adaptaSam = mc.checkBox(label='Adaptative Sampling', value=0)
    mc.checkBox(adaptaSam, e=1, cc=partial(adapSam, adaptaSam))
    
    arnoldDenoiser = mc.checkBox(label='Arnold Denoiser', value=0)
    mc.checkBox(arnoldDenoiser, e=1, cc=partial(arnoldDenoise, arnoldDenoiser))
    
    aACamera = mc.intSliderGrp(
        l="Camera AA", min=-10, max=10, field=True, value=4)
    diffuse = mc.intSliderGrp(l="Diffuse", min=-10,
                              max=10, field=True, value=3)
    specular = mc.intSliderGrp(
        l="Specular", min=-10, max=10, field=True, value=3)
    transmission = mc.intSliderGrp(
        l="Transmission", min=-10, max=10, field=True, value=0)
    sss = mc.intSliderGrp(l="SSS", min=-10, max=10, field=True, value=0)
    volume = mc.intSliderGrp(l="Volume Indirect", min=-10, max=10, field=True, value=0)
    
    mc.button(h=30, l="Apply", command=partial(
        apply_RS, aACamera, diffuse, specular, transmission, sss, volume))

    mc.text("AOVs", backgroundColor=[1, 1, 1], height=20, width=20)

    rgback = mc.checkBox( label='RGBA', changeCommand="RGBA_AOV()", value=0)
    zck = mc.checkBox(label='Z', changeCommand="Z_AOV()", value=0)
    diff_inck = mc.checkBox( label='diffuse_indirect', changeCommand="DiffIn_AOV()", value=0)
    diff_dirck = mc.checkBox(label='diffuse_direct',changeCommand="DiffDir_AOV()", value=0)
    emick = mc.checkBox(label='emission',changeCommand="Emission_AOV()", value=0)
    shwck = mc.checkBox(label='shadow_matte',changeCommand="Sdw_Matte_AOV()", value=0)
    spc_dirck = mc.checkBox( label='specular_direct',changeCommand="SpcDir_AOV()", value=0)
    spc_inck = mc.checkBox( label='specular_indirect',changeCommand="SpcIn_AOV()", value=0)
    sss_dirck = mc.checkBox(label='sss_direct',changeCommand="SSSDir_AOV()", value=0)
    sss_inck = mc.checkBox( label='sss_indirect',changeCommand="SSSIn_AOV()", value=0)
    t_inck = mc.checkBox( label='transmission_indirect',changeCommand="TsIN_AOV()", value=0)
    t_inck = mc.checkBox(label='transmission_direct', changeCommand="TsDir_AOV()", value=0)
    cry_objck = mc.checkBox( label='crypto_object',changeCommand="CryObj_AOV()", value=0)
    cry_matck = mc.checkBox(label='crypto_material',changeCommand="CryMtl_AOV()", value=0)
    cry_assck = mc.checkBox(label='crypto_material', changeCommand="CryMtl_AOV()", value=0)

    mc.checkBox( rgback, e=1, changeCommand=partial(rGBA_AOV, rgback))
    mc.checkBox(zck, e=1, changeCommand=partial(z_AOV,zck))
    mc.checkBox( diff_inck, e=1, changeCommand=partial(diffIn_AOV,diff_inck))
    mc.checkBox(diff_dirck, e=1,changeCommand=partial(diffDir_AOV,diff_dirck))
    mc.checkBox(emick, e=1,changeCommand=partial(emission_AOV,emick))
    mc.checkBox(shwck, e=1,changeCommand=partial(sdw_Matte_AOV,shwck))
    mc.checkBox( spc_dirck, e=1,changeCommand=partial(spcDir_AOV,spc_dirck))
    mc.checkBox( spc_inck, e=1,changeCommand=partial(spcIn_AOV,spc_inck))
    mc.checkBox(sss_dirck, e=1,changeCommand=partial(sSSDir_AOV,sss_dirck))
    mc.checkBox( sss_inck, e=1,changeCommand=partial(sSSIn_AOV,sss_inck))
    mc.checkBox( t_inck, e=1,changeCommand=partial(tsIN_AOV,t_inck))
    mc.checkBox(t_inck, e=1, changeCommand=partial(tsDir_AOV,t_inck))
    mc.checkBox( cry_objck, e=1,changeCommand=partial(cryObj_AOV,cry_objck))
    mc.checkBox(cry_matck, e=1,changeCommand=partial(cryMtl_AOV,cry_matck))
    mc.checkBox(cry_assck, e=1, changeCommand=partial(cryASS_AOV,cry_assck))

    mc.button(h=20, l="Test Render", backgroundColor=[
              1, 0, 1], command=partial(render_Out))
   

    mc.showWindow(myWindow)




renderSetupUI()
