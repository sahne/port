# Copyright (c) 2010 Daniel Walter <d.walter@0x90.at>
#
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#

import os
import subprocess
import fnmatch

# module providing all needed function within a ports tree
class PortsTree:
    def __init__(self, path='/usr/ports'):
        # check if portstree exist or exit 
        if (not os.path.exists(path)):
            execption_text = "Path not found : %s" % (path)
            raise Exception(exception_text)
        # check if portsnap exists and if executable
        portsnap_path = "/usr/sbin/portsnap"
        if (not (os.path.exists(portsnap_path) and
                 os.access(portsnap_path, os.X_OK))):
            raise Exception("portsnap missing or not executable")
        self.path = path
        self.portsnap = portsnap_path

    def sync (self, debug=1):
        # call portsnap fetch update
        portsnap = None
        try:
            if (debug):
                portsnap = subprocess.Popen([self.portsnap, "fetch", "update"],
                                            stderr=subprocess.PIPE)
            else:
                portsnap = subprocess.Popen([self.portsnap, "fetch", "update"],
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)
        except Exception as e:
            if (debug):
                print e
            raise Exception("Could not run portsnap")

        portsnap.wait()
        portsnap_output = portsnap.communicate()
        # check for errors and report them
        if (portsnap.returncode == 1):
            # get error
            error = None
            if (debug):
                error = portsnap_output[0]
            else:
                error = portsnap_output[1]
            raise Exception(error)

    # get currently used (?) index
    def get_index(self):
        # XXX change this if FreeBSD 10 is released
        try:
            tmp_idx = os.listdir(self.path)
        except OSError as ose:
            raise Exception("Could not find INDEX")
        else:
            tmp2_idx = fnmatch.filter(tmp_idx, 'INDEX-[0-9]')
            tmp2_idx.sort()
            tmp2_idx.reverse()
            return "/usr/ports/" + tmp2_idx[0]
