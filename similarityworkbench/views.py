from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseBadRequest, HttpResponse
from simplejson import dumps
from sdftools.moleculeformats import batch_smiles_to_smiles, batch_sdf_to_smiles
from similarityworkbench import funcs
from myCompounds.views import getMyCompounds

import os
from django.conf import settings

def get_workbench_compounds(request):
	ret = []
	from hashlib import md5
	page, compounds = getMyCompounds(request)
	for compound in compounds:
		md5id = md5(compound.cid).hexdigest()
		img = "/compounds/" + str(compound.id) + "/png"	
		ret.append(dict(img=img, md5=md5id, title=compound.name, smiles=compound.smiles))
	return ret

def add_compounds(smiles):
	"""given SMILES, generate a list of dictionaries, one for each compound,
	in format that is accepted at the client side""" 
	ret = []
	from hashlib import md5			# for md5 ID of compounds
	for i, c in enumerate(smiles.splitlines()):
		md5id = md5(c).hexdigest()
		try:
			s, name = c.split(None, 1)
		except:
			s = c
			name = 'Unnamed:' + md5id[:5]
		img = 'http://chemmine.ucr.edu/renderer/smiles;' + s
		ret.append(dict(img=img, md5=md5id, title=name, smiles=c))
	return ret

def ui(request):
	if request.method == 'GET':
		# on GET, show the UI page
		try:
			preload = dumps(get_workbench_compounds(request))
		except:
			preload = ''
		return render_to_response('similarityworkbench.html',
				dict(preload=preload),
				context_instance=RequestContext(request))
	else:
		# on POST, do actual work; the form tells what function to invoke
		func = request.POST.get('func', None)
		# there can be overrring function in the form. mostly javascript uses
		# this to override form-specified function
		if 'func-override' in request.POST:
			func = request.POST.get('func-override')
		# first type of function is compound upload
		if func in ['sdf', 'smiles']:
			if func == 'smiles':
				# process SMILES upload
				# first, format the SMILES
				smiles, err = batch_smiles_to_smiles(
					request.POST.get('smiles', ''))
			elif func == 'sdf':
				# process SDF upload
				sdff = request.FILES.get('sdffile', None)
				if not sdff or not sdff.size: return HttpResponseBadRequest()
				sdf = sdff.read()
				smiles, err = batch_sdf_to_smiles(sdf)

			# for each compound passed the format test, let the client know
			status = add_compounds(smiles)
			# also notify about the failed ones
			failed = err
			return HttpResponse(
					dumps(dict(failed=failed, status=status)),
					mimetype='text/json')

		# the other type is actually processing request. Check whether the
		# the requested function is supported
		elif hasattr(funcs, func):
			# there is correponding processor function in the funcs module
			f = getattr(funcs, func)
			ret = f(*request.POST.getlist('compound'))
			return HttpResponse(dumps(ret), mimetype='text/json')

		# we don't know how to process this request
		else:
			return HttpResponseBadRequest()
