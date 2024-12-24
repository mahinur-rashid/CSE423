'''Autogenerated by xml_generate script, do not edit!'''
from OpenGL import platform as _p, arrays
# Code generation uses this
from OpenGL.raw.GL import _types as _cs
# End users want this...
from OpenGL.raw.GL._types import *
from OpenGL.raw.GL import _errors
from OpenGL.constant import Constant as _C

import ctypes
_EXTENSION_NAME = 'GL_ARB_sample_locations'
def _f( function ):
    return _p.createFunction( function,_p.PLATFORM.GL,'GL_ARB_sample_locations',error_checker=_errors._error_checker)
GL_FRAMEBUFFER_PROGRAMMABLE_SAMPLE_LOCATIONS_ARB=_C('GL_FRAMEBUFFER_PROGRAMMABLE_SAMPLE_LOCATIONS_ARB',0x9342)
GL_FRAMEBUFFER_SAMPLE_LOCATION_PIXEL_GRID_ARB=_C('GL_FRAMEBUFFER_SAMPLE_LOCATION_PIXEL_GRID_ARB',0x9343)
GL_PROGRAMMABLE_SAMPLE_LOCATION_ARB=_C('GL_PROGRAMMABLE_SAMPLE_LOCATION_ARB',0x9341)
GL_PROGRAMMABLE_SAMPLE_LOCATION_TABLE_SIZE_ARB=_C('GL_PROGRAMMABLE_SAMPLE_LOCATION_TABLE_SIZE_ARB',0x9340)
GL_SAMPLE_LOCATION_ARB=_C('GL_SAMPLE_LOCATION_ARB',0x8E50)
GL_SAMPLE_LOCATION_PIXEL_GRID_HEIGHT_ARB=_C('GL_SAMPLE_LOCATION_PIXEL_GRID_HEIGHT_ARB',0x933F)
GL_SAMPLE_LOCATION_PIXEL_GRID_WIDTH_ARB=_C('GL_SAMPLE_LOCATION_PIXEL_GRID_WIDTH_ARB',0x933E)
GL_SAMPLE_LOCATION_SUBPIXEL_BITS_ARB=_C('GL_SAMPLE_LOCATION_SUBPIXEL_BITS_ARB',0x933D)
@_f
@_p.types(None,)
def glEvaluateDepthValuesARB():pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint,_cs.GLsizei,arrays.GLfloatArray)
def glFramebufferSampleLocationsfvARB(target,start,count,v):pass
@_f
@_p.types(None,_cs.GLuint,_cs.GLuint,_cs.GLsizei,arrays.GLfloatArray)
def glNamedFramebufferSampleLocationsfvARB(framebuffer,start,count,v):pass
