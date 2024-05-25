import os
import yaml

# Load the main config file
configfile: "config/config.yaml"

# Extract CO2 price range
co2_start = config['scenarios']['co2_pric2']['co2_price']['start']
co2_end = config['scenarios']['co2_pric2']['co2_price']['end']
co2_step = config['scenarios']['co2_price']['co2_price']['step']
co2_prices = range(co2_start, co2_end + 1, co2_step)

# Generate rule inputs for each CO2 price
def expand_scenarios(co2_prices):
    return expand("results/co2_price/co2_price_{price}", price=co2_prices)

rule all:
    input:
        expand_scenarios(co2_prices)

rule run_scenario:
    input:
        base_config="config/base_config.yaml",
        network_data="data",
    output:
        directory("results/co2_price/co2_price_{price}")
    params:
        co2_price="{price}"
    script:
        "src/main.py {params.co2_price}"

rule analyze_and_plot:
    input:
        expand("results/co2_price/co2_price_{price}/data", price=co2_prices)
    output:
        "plots/comparison/network_results_comparison.png"
    params:
        co2_prices=co2_prices
    script:
        "src/analyze_and_plot.py {params.co2_prices}"
