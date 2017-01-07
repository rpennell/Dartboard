#!/usr/bin/env python
#
# Copyright 2009 Facebook
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import Defaults

from time import sleep
from sys import exit
from importlib import import_module
from functools import partial

from Manager import Manager
from debug_tools import *
from Web import *

def loop():
    iface.refresh(manager, partial(update_clients))

if __name__ == "__main__":
    try:
        manager = Manager()
        iface = getattr(import_module("Boards." + Defaults.Interface_Type), "Interface")()

        if (Defaults.Web_Enable):
            web_start(loop)
        else:
            while True:
                loop()
                sleep(0.1)
    except KeyboardInterrupt:
        iface.end()
    finally:
        iface.end()

iface.end()
