import os
import platform
import sys


class TBag:
    @staticmethod
    def get_machine_info(base=None):
        if base:
            text_ = os.name + ' - ' + platform.machine() + '\n'
            text_ += base.win.gsg.driver_renderer + '\n'
            text_ += platform.system() + ' (' + platform.release() + ')\n'
            text_ += 'Texture limit: ' + str(base.win.getGsg().getMaxTextureStages()) + '\n'
            return text_
        else:
            print('Error!')

    @staticmethod
    def get_tech_info(base=None):
        gsg = base.win.getGsg()
        ogl_version = gsg.getDriverVersion()
        ogl_vendor = gsg.getDriverVendor()
        ogl_renderer = gsg.getDriverRenderer()
        print("OpenGL Version:", ogl_version)
        print("Vendor:", ogl_vendor)
        print("Renderer:", ogl_renderer)

