'''OpenGL extension MESA.program_binary_formats

This module customises the behaviour of the 
OpenGL.raw.GLES2.MESA.program_binary_formats to provide a more 
Python-friendly API

Overview (from the spec)
	
	The get_program_binary exensions require a GLenum binaryFormat.
	This extension documents that format for use with Mesa.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/MESA/program_binary_formats.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GLES2 import _types, _glgets
from OpenGL.raw.GLES2.MESA.program_binary_formats import *
from OpenGL.raw.GLES2.MESA.program_binary_formats import _EXTENSION_NAME

def glInitProgramBinaryFormatsMESA():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION