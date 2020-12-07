# Copyright 2020 William Ro. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ------------------------------------------------------------------------------
# This file incorporates work covered by the following copyright and
# permission notice:
#
#   Copyright (c) 2017 anderskm
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to
#   deal in the Software without restriction, including without limitation the
#   rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#   sell copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#   IN THE SOFTWARE.
#
#   Author: Anders Krogh Mortensen (anderskm)
# ==-========================================================================-==
"""Class for NVIDIA GPUs.
"""
import os
import platform
from collections import OrderedDict
from distutils import spawn
from goose.devices.gpus.gpu import GPU
from roma import censor
from roma import console
from subprocess import Popen, PIPE


class NvidiaGPUs(GPU):

  DEVICE_TYPE = 'GPU'
  VENDOR = 'NVIDIA'
  SMI_QUERIES = OrderedDict(zip(
    ['index', 'name', 'total_memory', 'free_memory', 'uuid', 'driver_version',
     'display_active', 'display_mode', 'temperature'],
    ['index', 'name', 'memory.total', 'memory.free', 'uuid',
     'driver_version', 'display_active', 'display_mode', 'temperature.gpu']))

  # region: Constructor

  def __init__(self, index, name, total_memory, free_memory=None, uuid=None,
               driver_version=None, display_active=None, display_mode=None,
               temperature=None, *args, **kwargs):
    # Call parent's constructor
    super().__init__(index, name, total_memory, free_memory, *args, **kwargs)
    # Special attributes
    self.uuid = censor.check_type(uuid, str)
    self.driver_version = censor.check_type(driver_version, str)
    self.display_active = censor.check_type(display_active, str)
    self.display_mode = censor.check_type(display_mode, str)
    self.temperature = censor.check_type(temperature, float)

  # endregion: Constructor

  # region: Static Methods

  @staticmethod
  def get_gpus_by_smi_output(smi_out):
    censor.check_type(smi_out, str)
    # Split lines
    lines = [line.split(',') for line in smi_out.splitlines()]
    # Check format for each line
    for raw_args in lines: assert len(raw_args) == len(NvidiaGPUs.SMI_QUERIES)
    # Instantiate NVIDIA GPUs and return
    gpus = [NvidiaGPUs(*args) for args in lines]
    return gpus


  @staticmethod
  def get_nvidia_gpus():
    """Get all NVIDIA GPUs as a list.
    """
    # Find the terminal handler of nvidia-smi
    if platform.system() == "Windows":
      # Try to find nvidia-smi using spawn
      nvidia_smi = spawn.find_executable('nvidia-smi')
      # If not found, try to find it in system drive
      if nvidia_smi is None:
        nvidia_smi = os.path.join(
          os.environ['systemdrive'],
          "Program Files\\NVIDIA Corporation\\NVSMI\\nvidia-smi.exe")
        # Show warning if still not found
        if not os.path.exists(nvidia_smi):
          console.warning('Failed to find nvidia-smi.')
          return []
    else: nvidia_smi = "nvidia-smi"

    # Get ID, processing and memory utilization for all GPUs
    try:
      queries = ','.join(NvidiaGPUs.SMI_QUERIES.values())
      p = Popen([nvidia_smi, "--query-gpu={}".format(queries),
                 "--format=csv,noheader,nounits"], stdout=PIPE)
      stdout, _ = p.communicate()
      # Decode output
      smi_out = stdout.decode('UTF-8')
    except:
      console.warning('Failed to run nvidia-smi.')
      return []

    # Return GPU list
    return NvidiaGPUs.get_gpus_by_smi_output(smi_out)

  # endregion: Static Methods

  # region: Interfaces

  def refresh(self):
    pass

  # endregion: Interfaces


if __name__ == '__main__':
  gpus = NvidiaGPUs.get_nvidia_gpus()
  print()
