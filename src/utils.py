import pypsa

def update_network(network,co2_tax=False,feedin_premium=False,load_upscaled=False,multiplier_storage=1.0,multiplier_fossil_price=1.0,transmission_grid_extension=1.0):
    """

    
    Parameters:

    """
    if multiplier_storage != 1.0:
        print('Storage cost is multiplied with: ' + str(multiplier_storage))
        network.storage_units['capital_cost'] = network.storage_units['capital_cost']*multiplier_storage
        output_file += '_mstor_'+str(multiplier_storage)
    if multiplier_fossil_price != 1.0:
        output_file += '_fossil_price_'+str(multiplier_fossil_price)    
        carriers_to_update = ['Hard coal', 'Natural gas', 'Lignite']
        network.generators.loc[network.generators['carrier'].isin(carriers_to_update), 'marginal_cost'] *= multiplier_fossil_price
    if transmission_grid_extension != 1.0:
        output_file += '_transmission_grid_extension_'+str(transmission_grid_extension)     
        for link in network.links.index:
            network.links.at[link, 'p_nom'] *= 3  # Increases the nominal capacity by a factor of 3



    # Update marginal costs and capital cost considering specific emissions and efficiency depending on the support scheme
    if co2_tax:
        for gen in network.generators.index:
            fuel_type = network.generators.at[gen, 'carrier']
            co2_emissions_per_unit = network.carriers.at[fuel_type, 'co2_emissions']  # CO2 emissions per unit of fuel
            efficiency = network.generators.at[gen, 'efficiency']  # Generator efficiency (MWh produced per unit of fuel)

            # Calculate specific CO2 emissions per MWh
            specific_emissions = co2_emissions_per_unit / efficiency

            # Calculate additional cost per MWh due to CO2 emissions
            co2_cost_per_mwh = specific_emissions * co2_tax * conv_factor

            # Update the marginal cost
            network.generators.at[gen, 'marginal_cost'] += co2_cost_per_mwh     
            
    return network

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
