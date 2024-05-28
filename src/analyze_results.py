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
