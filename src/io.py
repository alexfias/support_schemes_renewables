def read_networks_for_analysis(scenario_name, network_files, network_names,homogenize_capital_costs=False,homogenize_marginal_costs=False):
    """
    Reads network files of a specific solved scenario

    Parameters:
    scenario_name (string): The name of the scenario
    network_files (list of strings): The locations of the network files
    network_names (list of strings): The names of the networks
    homogenize_capital_costs (binary): Homogenize the capital costs of the network with respect to the base network (first network in list)
    homogenize_marginal_costs (binary): Homogenize the marginal costs of the network with respect to the base network (first network in list)

    Returns:
    dictionary: Dictionary containing the network files

    """
    i = 0
    networks = {}
    for network in network_files:
        netcdf_path = network_files[i]
        networks[network_names[i]] = pypsa.Network()
        networks[network_names[i]].import_from_netcdf(path=netcdf_path)
        i += 1
    if homogenize_capital_costs:
        #homogenize capital costs
        for i, network in enumerate(networks):
            networks[network].generators.capital_cost = networks[network_names[0]].generators.capital_cost
    if homogenize_marginal_costs:
        #homogenize marginal costs
        for i, network in enumerate(networks):
            networks[network].generators.marginal_cost = networks[network_names[0]].generators.marginal_cost
        
    # Return the networks
    return networks
