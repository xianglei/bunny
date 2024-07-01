#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cherrypy


class DisableContentLengthTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_request_body', self.check_content_length, priority=10)

    def check_content_length(self):
        if 'Content-Length' not in cherrypy.request.headers:
            cherrypy.request.headers['Content-Length'] = 0


cherrypy.tools.disable_content_length = DisableContentLengthTool()
