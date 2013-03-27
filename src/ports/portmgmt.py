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

from . import port
from . import portstree
# get all installed ports and their corresponding version
# ports are directories under /var/db/pkg
# eg:
# /var/db/pkg/vim-7.2.411/
def get_installed_ports():
    ports = []
    for port in os.listdir('/var/db/pkg'):
        # ignore portupgrades pkgdb.db
        # TODO check if port is a directory, else ignore
        if (port == "pkgdb.db"):
            continue
        tmp = port.split('-')
        portversion = ''.join(tmp[-1:])
        portname = '-'.join(tmp[:-1])
        # get origin for package (needed since some packages do not use
        # the same name as the port has), eg: apache-2.2 -> www/apache22
        # TODO check if file exists !
        origin = ''
        try:
            ftmp = open('/var/db/pkg/' + port + '/+CONTENTS')
            for line in ftmp.readlines():
                if (line.startswith('@comment ORIGIN')):
                    origin = line[line.find(':')+1:-1]
                    break
            ftmp.close()
        except IOError as ioe:
            print "ERROR: could not open +CONTENTS for %s" % port
        #print 'DEBUG found port %s, %s, %s' % (portname, portversion, origin)
        ports.append((portname, portversion, origin))
    ports.sort(compare_ports)
    return ports


# get all ports from INDEX 
def get_all_ports():
    ports = []
    tree = portstree.PortsTree("/usr/ports")
    idx_path = tree.get_index()
    # check if INDEX is up to date
    idx_mtime = os.stat(idx_path).st_mtime
    if ((idx_mtime + 14*24*60*60) < time.time()):
        print "WARNING: portstree is older than 14 days"
        print "Please update tree using ``port sync``"
    idx_file = open(idx_path,'r')
    for line in idx_file.readlines():
        port = line[:line.find('|')]
        tmp = port.split('-')
        # get port name and version
        portversion = ''.join(tmp[-1:])
        portname = '-'.join(tmp[:-1])
        tmp_len = len(port) + 1
        # get port directory
        origin = line[tmp_len:line.find('|', tmp_len)]
        origin = origin.replace('/usr/ports/','')
        #print "DEBUG: found port %s, %s, %s" % (portname, portversion, origin)
        ports.append((portname, portversion, origin))
    idx_file.close()
    ports.sort(compare_ports)
    return ports
