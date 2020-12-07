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
# ===-===================================================================-======
"""Base class for GPUs.
"""
from goose.devices.device import Device
from roma import censor


class GPU(Device):

  DEVICE_TYPE = 'GPU'

  def __init__(self, index, name, total_memory, free_memory=None,
               *args, **kwargs):
    # Call parent's constructor
    super().__init__(*args, **kwargs)
    # Special attributes
    self.index = censor.check_type(index, int)
    self.name = censor.check_type(name, str)
    self.total_memory = censor.check_type(total_memory, float)
    self.free_memory = censor.check_type(free_memory, float, nullable=True)





