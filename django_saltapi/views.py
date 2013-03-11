# -*- coding: utf-8 -*-

# Import our libs
from .control import (
    wildcardtarget,
    get_salt_client,
    get_api_client,
    )
from .forms import LowdataForm

# Import Python libs
import json

# Import Django libs
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse


def JsonResponse(what):
    return HttpResponse(json.dumps(what), content_type='application/json')

# Externally accessible functions

#@login_required
@wildcardtarget
def ping(request, tgt):
    client = get_salt_client()
    ret = client.cmd(tgt, 'test.ping', ret='json')
    return JsonResponse(ret)

#@login_required
@wildcardtarget
def echo(request, tgt, arg):
    client = get_salt_client()
    ret = client.cmd(tgt, 'test.echo', arg, ret='json')
    return JsonResponse(ret)

#@login_required
def minions(request, mid):
    client = get_salt_client()
    ret = client.cmd(mid or '*', 'grains.items', ret='json')
    return JsonResponse(ret)

#@login_required
def jobs(request, jid):
    client = get_api_client()
    lowdata = {
        'client': 'runner',
        'fun': 'jobs.lookup_jid' if jid else 'jobs.list_jobs',
        'jid': jid,
        }
    ret = client.run(lowdata)
    return JsonResponse(ret)

#@login_required
@csrf_exempt
def apiwrapper(request):
    if request.method == 'POST':
        form = LowdataForm(request.POST)

        if form.is_valid():
            client = get_api_client()
            lowdata = {
                'client': form.cleaned_data['client'],
                'tgt': form.cleaned_data['tgt'],
                'fun': form.cleaned_data['fun'],
                'arg': form.cleaned_data['arg'],
                }
            ret = client.run(lowdata)

            return JsonResponse(ret)

    elif request.method == 'GET':
        return render(request, 'index.html')
