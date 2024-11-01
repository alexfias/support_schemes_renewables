import pypsa

def apply_co2_price(network, co2_price):
    """
    Apply a CO2 price to the network.
    
    Parameters:
    network (pypsa.Network): The PyPSA network object.
    co2_price (float): The CO2 price to apply.
    """
    for carrier in network.carriers.index:
        if 'co2' in carrier:
            network.carriers.at[carrier, 'co2_emissions'] *= co2_price

    return network


def update_network_with_scenario(network, scenario_config):
    """
    Update the network with scenario-specific parameters.
    
    Parameters:
    network (pypsa.Network): The PyPSA network object.
    scenario_config (dict): Scenario-specific configuration.
    """
    if 'co2_price' in scenario_config:
        apply_co2_price(network, scenario_config['co2_price'])

    if 'storage_cost' in scenario_config:
        update_storage_cost(network, scenario_config['storage_cost'])
    
    if 'fossil_prices' in scenario_config:
        update_fossil_prices(network, scenario_config['fossil_prices'])

    if weather_year in scenario_config:
        update_weather_year(network, scenario_config['weather_year'])

    if transmission_expansion in scenario_config:
        update_transmission_expansion(network, scenario_config['transmission_expansion])
        
    return network
