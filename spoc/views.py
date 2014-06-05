# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.utils.translation import ugettext as _

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import authentication, permissions
# from django.core.urlresolvers import reverse

from spoc import models


# class TodoView(UiView):
#     """Simple view without a map."""
#     template_name = 'spoc/todo.html'
#     page_title = _('TODO view')


# class Todo2View(MapView):
#     """Simple view with a map."""
#     template_name = 'spoc/todo2.html'
#     page_title = _('TODO 2 view')

class ListLocations(viewsets.ModelViewSet):
    """ List dummy locations. """

    model = models.Location


    # def get(self, request, format=None):
    #     dummy_locations = [
    #         {"locationId": "1", "name": "ABC201"},
    #         {"locationId": "2", "name": "ABC202"},
    #         {"locationId": "3", "name": "ABC203"},
    #         {"locationId": "4", "name": "ABC204"}
    #     ]
    #     locations = [Location(**location) for location in dummy_locations]
    #     return Response(locations)
