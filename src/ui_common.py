#!/usr/bin/env python
#-=- encoding: utf-8 -=-
#
#This file is part of Orgapp.
#
#Orgapp is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#Orgapp is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with Orgapp.  If not, see <http://www.gnu.org/licenses/>.

from cork import Cork
from bottle import request, abort


def is_ajax(fn):
    def is_ajax(fn):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return fn
        else:
            abort(404, "pfff")

auth = Cork('config')
