#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012-2021, Cenobit Technologies, Inc. http://cenobit.es/
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# * Neither the name of the Cenobit Technologies nor the names of
#    its contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# isort:skip_file
import os
import sys

from flask import Flask, request

PROJECT_DIR, PROJECT_MODULE_NAME = os.path.split(os.path.dirname(os.path.realpath(__file__)))

FLASK_JSONRPC_PROJECT_DIR = os.path.join(PROJECT_DIR, os.pardir)
if os.path.exists(FLASK_JSONRPC_PROJECT_DIR) and FLASK_JSONRPC_PROJECT_DIR not in sys.path:
    sys.path.append(FLASK_JSONRPC_PROJECT_DIR)

from flask_jsonrpc import JSONRPC, JSONRPCView  # noqa: E402   pylint: disable=C0413


class UnauthorizedError(Exception):
    pass


class AuthorizationView(JSONRPCView):
    def check_auth(self) -> bool:
        username = request.headers.get('X-Username')
        password = request.headers.get('X-Password')
        return username == 'username' and password == 'secret'

    def dispatch_request(self):
        if not self.check_auth():
            raise UnauthorizedError()
        return super().dispatch_request()


app = Flask('auth')
jsonrpc = JSONRPC(app, '/api', jsonrpc_site_api=AuthorizationView)


@jsonrpc.method('App.index')
def index() -> str:
    return 'Welcome to Flask JSON-RPC'


@jsonrpc.method('App.echo')
def echo(name: str = 'Flask JSON-RPC') -> str:
    return 'Hello {0}'.format(name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
