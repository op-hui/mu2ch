# Соединяет две локации
def locationTunnel(location1, location1_exit_name, location2, location2_exit_name): 
    create_object(settings.BASE_EXIT_TYPECLASS, location2_exit_name if (location2_exit_name) else location2.key, location = location1, destination = location2)
    create_object(settings.BASE_EXIT_TYPECLASS, location1_exit_name if (location1_exit_name) else location1.key, location = location2, destination = location1)

def locationTunnelDefault(location1, location2): 
    return locationTunnel(location1, location2.key, location2, location1.key) 

