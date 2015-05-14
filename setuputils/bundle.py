# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional log.information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

#-----------------------------------------------------------------------------
#  This bundling code is largely adapted from pyzmq's code
#  PyZMQ Developers, which is itself Modified BSD licensed.
#-----------------------------------------------------------------------------

import os
import shutil
import stat
import sys
import tarfile
from glob import glob
from subprocess import Popen, PIPE

try:
    # py2
    from urllib2 import urlopen
except ImportError:
    # py3
    from urllib.request import urlopen

from . import log


#-----------------------------------------------------------------------------
# Constants
#-----------------------------------------------------------------------------
min_qpid_proton = (0, 9)
min_qpid_proton_str = "%i.%i" % min_qpid_proton

bundled_version = (0,9,1)
bundled_version_str = "%i.%i.%i" % (0,9,1)
libqpid_proton = "qpid-proton-%s.tar.gz" % bundled_version_str
libqpid_proton_url = ("http://www.apache.org/dist/qpid/proton/%s/%s" %
                      (bundled_version_str, libqpid_proton))

HERE = os.path.dirname(__file__)
ROOT = os.path.dirname(HERE)


def fetch_archive(savedir, url, fname):
    """Download an archive to a specific location

    :param savedir: Destination dir
    :param url: URL where the archive should be downloaded from
    :param fname: Archive's filename
    """
    dest = os.path.join(savedir, fname)

    if os.path.exists(dest):
        log.info("already have %s" % fname)
        return dest

    log.info("fetching %s into %s" % (url, savedir))
    if not os.path.exists(savedir):
        os.makedirs(savedir)
    req = urlopen(url)
    with open(dest, 'wb') as f:
        f.write(req.read())
    return dest


def fetch_libqpid_proton(savedir):
    """Download qpid-proton to `savedir`."""
    dest = os.path.join(savedir, 'qpid-proton')
    if os.path.exists(dest):
        log.info("already have %s" % dest)
        return
    fname = fetch_archive(savedir, libqpid_proton_url, libqpid_proton)
    tf = tarfile.open(fname)
    member = tf.firstmember.path
    if member == '.':
        member = tf.getmembers()[1].path
    with_version = os.path.join(savedir, member)
    tf.extractall(savedir)
    tf.close()
    shutil.move(with_version, dest)
