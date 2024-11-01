def plot_market_value_across_networks_per_tech(networks):
    """
    Plots the market values of different technologies for different networks

    Parameters:
    networks: A dictionary of networks
    """    
    market_values_df2 = pd.DataFrame()
    
    for i, network_label in enumerate(networks):
        network = networks[network_label]
        generator_techs = network.generators.carrier.unique()
        market_values = {}
    
        for tech in generator_techs:
            # Select generators of the current technology
            generators_of_tech = network.generators.index[network.generators.carrier == tech]
        
            # Get the corresponding buses for these generators
            buses_of_tech = network.generators.loc[generators_of_tech, 'bus']
        
            # Get the generation data and marginal prices aligned with these generators
            generation_data = network.generators_t.p[generators_of_tech]
            marginal_prices = network.buses_t.marginal_price[buses_of_tech.values].values
        
            # Calculate the total generation and total weighted price for the current technology
            total_generation = generation_data.sum().sum()
            total_weighted_price = (generation_data * marginal_prices).sum().sum()
        
            # Calculate the market value for the current technology
            market_value = total_weighted_price / total_generation if total_generation != 0 else 0
            market_values[tech] = market_value/4.57
    
        # Add the market values for this network to the DataFrame
        market_values_df2 = market_values_df2.append(pd.DataFrame(market_values, index=[network_labels[i]]))

    # Plot the market values for each technology across all networks as lines
    ax = market_values_df2.plot(kind='line', marker='o', figsize=(14, 8), colormap="tab20")

    # Add grid
    ax.grid(True)

    # Add labels and title
    ax.set_xlabel('Network', fontsize=12, fontweight='bold')
    ax.set_ylabel('Market Value [€/MWh]', fontsize=12, fontweight='bold')
    ax.set_title('Market Values per Technology Across Networks', fontsize=16, fontweight='bold')

    # Customize x-ticks
    plt.xticks(ticks=range(len(network_labels)), labels=network_labels, rotation=45)

    # Add legend
    plt.legend(title='Technology', fontsize=10)

    # Adjust layout
    plt.tight_layout()

    # Display the plot
    plt.show()    
