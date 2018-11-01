#!/usr/bin/env python
# encoding: utf-8
"""
render.py
"""
import aiohttp_jinja2
from aiohttp import web

async def json(data, status, headers=None):
    response = web.json_response(data, status=status, headers=None, content_type='application/json')
    return response


async def raw_json(data, status, headers=None):
    response = web.Response(text=data, status=status, headers=None, content_type='application/json')
    return response


async def raw(data, status, headers=None):
    response = web.Response(text=data, status=status, headers=None, content_type='application/json')
    return response