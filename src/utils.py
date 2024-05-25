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

def update_network_with_scenario(network, scenario_config):
    """
    Update the network with scenario-specific parameters.
    
    Parameters:
    network (pypsa.Network): The PyPSA network object.
    scenario_config (dict): Scenario-specific configuration.
    """
    if 'co2_price' in scenario_config:
        apply_co2_price(network, scenario_config['co2_price'])
