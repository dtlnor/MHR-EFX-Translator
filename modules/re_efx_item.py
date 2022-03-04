#Author: NSA Cloud
from .gen_functions import textColors,raiseWarning,raiseError,getPaddingAmount,read_short,read_uint,read_int,read_uint64,read_float,read_ubyte,read_string,read_unicode_string,read_byte,write_uint,write_int,write_uint64,write_float,write_short,write_ubyte,write_string,write_unicode_string,write_byte
from .file_re_efx import EFXR

class PlayEfx():
    def __init__(self):
        self.efxPathLength = 0
        self.efxPath = "path\to\efx.efx"
    def read(self,file):
        self.efxPathLength = read_uint(file)
        self.efxPath = read_unicode_string(file)
    def write(self,file):
        write_uint(file,self.efxPathLength)
        write_unicode_string(file, self.efxPath)
    def getSize(self):
        return 4 + len(self.efxPath)*2 + 2

class PlayEmitter():
    def __init__(self):
        self.fileSize = 0
    def read(self,file):
        self.fileSize = read_uint(file)
        self.actionEFXR = EFXR()
        self.actionEFXR.fileSize = self.fileSize
        self.actionEFXR.read(file)
    def write(self,file):
        write_uint(file,self.fileSize)
        self.actionEFXR.write(file)
    def getSize(self):
        self.actionEFXR.updateSizes()
        return  4 + self.actionEFXR.fileSize

class PtBehavior():
    
    class propertySubStruct():
        def __init__(self):
            self.substructLength = 0
            self.substructLength = 0
            self.unkn1 = 0
            self.unkn2 = 0
            self.unkn3 = 0
            self.unkn4 = 0
        def read(self,file):
            self.substructLength = read_uint(file)
            self.unkn1 = read_uint(file)
            self.unkn2 = read_uint(file)
            self.unkn3 = read_uint(file)
            self.unkn4 = read_uint(file)
            self.behaviorString = file.read(self.substructLength -16).decode("utf-8")
        def write(self,file):
            write_uint(file,self.substructLength)
            write_uint(file,self.unkn1)
            write_uint(file,self.unkn2)
            write_uint(file,self.unkn3)
            write_uint(file,self.unkn4)
            write_string(file,self.behaviorString)
        def getSize(self,file):
            return 20 + len(self.behaviorString) + 1
        
    def __init__(self):
        self.unkn1 = 0
        self.stringLength = 0
        self.substructCount = 0
        self.propertySubStructList = []
    def read(self,file):
        self.unkn1 = read_uint(file)
        self.stringLength = read_uint(file)
        self.substructCount = read_uint(file)
        for i in range(0,self.substructCount):
            prop = self.propertySubStruct()
            prop.read()
            self.propertySubStructList.append(prop)
    def write(self,file):
        write_uint(file,self.unkn1)
        write_uint(file,self.stringLength)
        write_uint(file,self.substructCount)
        
    def getSize(self):
        currentSize = 0
        for prop in self.propertySubStructList:
            currentSize += prop.getSize()
        return 12 + len(self.behaviorString) + 1
def getEFXItemStruct(itemType,game = "MHRise"):
    #if game == "MHRise":
        """
        0:Unknown,
        1:FixRandomGenerator,
        2:EffectOptimizeShader,
        3:Spawn,
        4:SpawnExpression,
        5:Transform2D,
        6:Transform2DModifierDelayFrame,
        7:Transform2DModifier,
        8:Transform2DClip,
        9:Transform2DExpression,
        10:Transform3D,
        11:Transform3DModifierDelayFrame,
        12:Transform3DModifier,
        13:Transform3DClip,
        14:Transform3DExpression,
        15:ParentOptions,
        16:EmitterColor,
        17:EmitterColorClip,
        18:PtSort,
        19:TypeBillboard2D,
        20:TypeBillboard2DExpression,
        21:TypeBillboard3D,
        22:TypeBillboard3DExpression,
        23:TypeBillboard3DMaterial,
        24:TypeBillboard3DMaterialClip,
        25:TypeBillboard3DMaterialExpression,
        26:TypeMesh,
        27:TypeMeshClip,
        28:TypeMeshExpression,
        29:TypeRibbonFollow,
        30:TypeRibbonLength,
        31:TypeRibbonChain,
        32:TypeRibbonFixEnd,
        33:TypeRibbonLightweight,
        34:TypeRibbonParticle,
        35:TypeRibbonFollowMaterial,
        36:TypeRibbonFollowMaterialClip,
        37:TypeRibbonFollowMaterialExpression,
        38:TypeRibbonLengthMaterial,
        39:TypeRibbonLengthMaterialClip,
        40:TypeRibbonLengthMaterialExpression,
        41:TypeRibbonChainMaterial,
        42:TypeRibbonChainMaterialClip,
        43:TypeRibbonChainMaterialExpression,
        44:TypeRibbonFixEndMaterial,
        45:TypeRibbonFixEndMaterialClip,
        46:TypeRibbonFixEndMaterialExpression,
        47:TypeRibbonLightweightMaterial,
        48:TypeRibbonLightweightMaterialClip,
        49:TypeRibbonLightweightMaterialExpression,
        50:TypeStrainRibbonMaterial,
        51:TypeStrainRibbonMaterialClip,
        52:TypeStrainRibbonMaterialExpression,
        53:TypeRibbonFollowExpression,
        54:TypeRibbonLengthExpression,
        55:TypeRibbonChainExpression,
        56:TypeRibbonFixEndExpression,
        57:TypePolygon,
        58:TypePolygonClip,
        59:TypePolygonExpression,
        60:TypePolygonMaterial,
        61:TypeRibbonTrail,
        62:TypePolygonTrail,
        63:TypePolygonTrailMaterial,
        64:TypeNoDraw,
        65:TypeNoDrawExpression,
        66:Velocity2DDelayFrame,
        67:Velocity2D,
        68:Velocity2DExpression,
        69:Velocity3DDelayFrame,
        70:Velocity3D,
        71:Velocity3DExpression,
        72:RotateAnimDelayFrame,
        73:RotateAnim,
        74:RotateAnimExpression,
        75:ScaleAnimDelayFrame,
        76:ScaleAnim,
        77:ScaleAnimExpression,
        78:VanishArea3D,
        79:VanishArea3DExpression,
        80:Life,
        81:LifeExpression,
        82:UVSequence,
        83:UVSequenceModifier,
        84:UVSequenceExpression,
        85:UVScroll,
        86:TextureUnit,
        87:TextureUnitExpression,
        88:TextureFilter,
        89:EmitterShape2D,
        90:EmitterShape2DExpression,
        91:EmitterShape3D,
        92:EmitterShape3DExpression,
        93:AlphaCorrection,
        94:ContrastHighlighter,
        95:ColorGrading,
        96:Blink,
        97:Noise,
        98:TexelChannelOperator,
        99:TexelChannelOperatorClip,
        100:TexelChannelOperatorExpression,
        101:TypeStrainRibbon,
        102:TypeStrainRibbonExpression,
        103:TypeLightning3D,
        104:TypeLightning3DExpression,
        105:TypeLightning3DMaterial,
        106:ShaderSettings,
        107:ShaderSettingsExpression,
        108:Distortion,
        109:DistortionExpression,
        110:VolumetricLighting,
        111:RenderTarget,
        112:PtLife,
        113:PtBehavior,
        114:PtBehaviorClip,
        
        116:FadeByAngle,
        117:FadeByAngleExpression,
        118:FadeByEmitterAngle,
        119:FadeByDepth,
        120:FadeByDepthExpression,
        121:FadeByOcclusion,
        122:FadeByOcclusionExpression,
        123:FakeDoF,
        124:LuminanceBleed,
        125:ScaleByDepth,
        126:TypeNodeBillboard,
        127:TypeNodeBillboardExpression,
        128:UnitCulling,
        129:FluidEmitter2D,
        130:FluidSimulator2D,
        """
        itemTypeDict = {
        115:PlayEfx,
        131:PlayEmitter,
        
        
        }
        """
        132:PtTransform3D,
        133:PtTransform3DClip,
        134:PtTransform2D,
        135:PtTransform2DClip,
        136:PtVelocity3D,
        137:PtVelocity3DClip,
        138:PtVelocity2D,
        139:PtVelocity2DClip,
        140:PtColliderAction,
        141:PtCollision,
        142:PtColor,
        143:PtColorClip,
        144:PtUvSequence,
        145:PtUvSequenceClip,
        146:MeshEmitter,
        147:MeshEmitterClip,
        148:MeshEmitterExpression,
        149:ScreenSpaceEmitter,
        150:Vector,
        151:VectorFieldParameterClip,
        152:VectorFieldParameterExpression,
        153:GlobalVectorField,
        154:GlobalVectorFieldClip,
        155:GlobalVectorFieldExpression,
        156:DirectionalFieldParameter,
        157:DirectionalFieldParameterClip,
        158:DirectionalFieldParameterExpression,
        159:DepthOperator,
        160:PlaneCollider,
        161:PlaneColliderExpression,
        162:DepthOcclusion,
        163:ShapeOperator,
        164:ShapeOperatorExpression,
        165:WindInfluence3DDelayFrame,
        166:WindInfluence3D,
        167:Attractor,
        168:AttractorClip,
        169:AttractorExpression,
        170:CustomComputeShader,
        171:TypeGpuBillboard,
        172:TypeGpuBillboardExpression,
        173:TypeGpuPolygon,
        174:TypeGpuRibbonFollow,
        175:TypeGpuRibbonLength,
        176:TypeGpuMesh,
        177:TypeGpuMeshExpression,
        178:TypeGpuMeshTrail,
        179:TypeGpuMeshTrailClip,
        180:TypeGpuMeshTrailExpression,
        181:TypeGpuLightning3D,
        182:EmitterPriority,
        183:DrawOverlay,
        184:VectorField,
        185:VolumeField,
        186:DirectionalField,
        187:AngularVelocity3DDelayFrame,
        188:AngularVelocity3D,
        189:PtAngularVelocity3D,
        190:PtAngularVelocity3DExpression,
        191:AngularVelocity2DDelayFrame,
        192:AngularVelocity2D,
        193:PtAngularVelocity2D,
        194:PtAngularVelocity2DExpression,
        195:IgnorePlayerColor,
        196:ProceduralDistortionDelayFrame,
        197:ProceduralDistortion,
        198:ProceduralDistortionClip,
        199:ProceduralDistortionExpression,
        200:TestBehaviorUpdater,
        201:StretchBlur,
        202:StretchBlurExpression,
        203:EmitterHSV,
        204:EmitterHSVExpression,
        205:FlowMap,
        206:RgbCommon,
        207:RgbWater,
        208:EmitMask,
        209:TypeModularBillboard,
        210:ItemNum,
        """
        return(itemTypeDict.get(itemType,None))