#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

p = os.path.join(os.path.dirname(__file__), 'tools')
i = os.path.join(os.path.dirname(__file__), 'ui')

if not p in sys.path:
    sys.path.append(p)
if not i in sys.path:
    sys.path.append(i)

from UI_Dock import Dock

import mainUI
reload(mainUI)

ui = Dock(mainUI.UI)
