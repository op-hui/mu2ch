# -*- coding: utf-8 -*-
# Соединяет две локации

from evennia import create_object
from evennia import settings

def locationTunnel(location1, location1_exit_name, location2, location2_exit_name): 

    exit1 = location2_exit_name if (location2_exit_name) else location2.key
    exit2 = location1_exit_name if (location1_exit_name) else location1.key
    print "Create tunnel between '%s' and '%s'" % ( exit1, exit2 ) 
    create_object(settings.BASE_EXIT_TYPECLASS, exit1, location = location1, destination = location2)
    create_object(settings.BASE_EXIT_TYPECLASS, exit2, location = location2, destination = location1)

def locationTunnelDefault(location1, location2): 
    return locationTunnel(location1, None, location2, None) 

