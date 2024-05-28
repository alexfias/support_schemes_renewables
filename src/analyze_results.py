import pandas as pd
import pypsa


def calculate_generation_shares_per_tech(network):
    """
    Calculate the share of generated energy per technology in the PyPSA network.

    Parameters:
    network (pypsa.Network): The PyPSA network object containing the simulation results.

    Returns:
    pd.Series: A series with the share of generated energy per technology.
    """
    # Summing the generated energy across all times for each generator
    total_generated_energy = network.generators_t.p.sum()
    
    # Join the total generated energy back to the generators DataFrame
    generators_with_total_energy = network.generators.join(total_generated_energy.rename('total_energy'), how='inner')
    
    # Group by 'bus' and 'technology', then sum the total energy for each group
    energy_per_bus_technology = generators_with_total_energy.groupby(['bus', 'technology'])['total_energy'].sum().unstack(fill_value=0)
    
    # Calculate the total energy per technology by summing over all buses
    total_energy_per_technology = energy_per_bus_technology.sum()
    
    # Calculate the share of each technology by dividing by the total generated energy
    generation_shares = total_energy_per_technology / total_energy_per_technology.sum()
    
    return generation_shares

# Example usage:
# Assuming 'network' is a PyPSA Network object that has been properly initialized and run.
# generation_shares = calculate_generation_shares_per_tech(network)
# print(generation_shares)


def calculate_market_prices(network,per_tech=False):
    """
    Calculate the market price of a technology as the average revenue per energy unit dispatched.

    Parameters:
    network (pypsa.Network): The PyPSA network object containing the simulation results.

    Returns:
    pd.DataFrame: A DataFrame where each element represents the revenue per energy unit dispatched
                  for each generator over time.
    """
    # Extract power generation (in MW)
    generators_p = network.generators_t.p

    # Extract marginal prices (in €/MWh)
    marginal_prices = network.buses_t.marginal_price

    # Map generators to their buses
    generators_buses = network.generators.bus

    # Create an empty DataFrame to store the aligned marginal prices
    aligned_marginal_prices = pd.DataFrame(index=generators_p.index, columns=generators_p.columns)

    # Align the marginal prices with the generators
    for gen in generators_p.columns:
        bus = generators_buses.loc[gen]
        aligned_marginal_prices[gen] = marginal_prices[bus]

    # Multiply generators power with marginal prices at the corresponding bus to get the revenue
    revenue = generators_p * aligned_marginal_prices

    # Calculate the market price of each generator as the average revenue per unit of energy dispatched
    market_price_per_tech = revenue.mean() / generators_p.mean()
    
    if per_tech:
        # Calculate the market price of each technology as the average revenue per unit of energy dispatched
        market_prices_per_tech = {}
        for tech in network.generators['technology'].unique():
            tech_indices = network.generators[network.generators['technology'] == tech].index
            tech_market_price = (market_price_per_tech[tech_indices] * network.generators_t.p.loc[:, tech_indices].sum()).sum() / network.generators_t.p.loc[:, tech_indices].sum().sum()
            market_prices_per_tech[tech] = tech_market_price
        return pd.Series(market_prices_per_tech, name="Market Price per Technology")    
    else:
        return market_price_per_tech

# Example usage:
# Assuming 'network' is a PyPSA Network object that has been properly initialized and run.
# market_prices = calculate_market_price_of_tech(network)
# print(market_prices)
