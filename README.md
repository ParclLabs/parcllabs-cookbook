![Logo](img/labs.jpg)
# Welcome to the Lab 🥼🧪

Welcome to the Parcl Labs repository. This repository contains examples of how to use the Parcl Labs API. The Parcl Labs API is a real-time, advanced real estate analytics data technology. It accelerates time to analysis, shifting the 80% of time typically spent on data wrangling to analysis.

We open source all of our content off of [X](https://twitter.com/ParclLabs). How we do it is 👇

## Sign Up for an API Key

To use the Parcl Labs API, you need an API key. To get an API key, sign up at [Parcl Labs](https://dashboard.parcllabs.com/signup).

## Installation

The fastest ways to get started are with Binder or Google Colab. Google Colab is embedded directly in each notebook. It is substantially faster than Binder and our recommended way to get started the fastest. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/ParclLabs/parcllabs-examples/main)

## Local Installation

You can fully reproduce the results of this repository on your own local machine. To do so, follow the steps below:

1. Clone the repository:

```bash
git clone https://github.com/ParclLabs/parcllabs-examples.git
```

2. Install the enviornment:

```bash
conda env create -f environment.yml
```

3. Activate Environment:

```bash
conda activate parcllabs-env
```

4. Run the Jupyter Notebook:

```bash
jupyter notebook
```

## Inspiration

We write all of our own content off of these notebooks. Here are some of the greatest hits: 

### [Market Supply and Demand Analysis Notebook](python/supply_demand.ipynb)

![Chart](python/assets/purchase_price_vs_new_listings_price.png)

### [Investor Share of Resale Listings Notebook](python/investor_share_of_resale_listings.ipynb)

![Chart](python/assets/atlanta_investor_share.png)

### [Map of where 1000+ unit portfolios own the most home, 3000+ counties notebook](python/map_of_investor_ownership.ipynb)

![Chart](python/assets/large_institutional_ownership.png)

### [Deep dive market analysis notebook](python/market_analysis.ipynb)

![Chart](python/assets/purchase_price_vs_list_price.png)

### [Map of where 1000+ unit portfolios own the most homes, in all zip codes in Georgia](python/map_of_investor_ownership_zip_code.ipynb)
![Chart](python/assets/atlanta_investor_ownership.png)

### [Which metros have the highest concentration of investor ownership notebook](python/table_of_investor_concentration.ipynb)

![Chart](python/assets/all_homes_owned_by_investors.png)

### [Are investor net buyers or sellers notebook?](python/table_of_purchase_to_sale_ratio.ipynb)

![Chart](python/assets/purchase_to_sale_ratio.png)

### [1000+ unit portfolio share of single family home resale listings market notebook](python/large_institutional_impact_on_resale_market.ipynb)

![Chart1](python/assets/percent_of_resale_market_by_1000_plus_unit_portfolios.png)

### [Gross Yield and Median Rental Price](python/gross_yield_vs_rental_price.ipynb)

![Chart1](python/assets/gross_yield_and_rent_price.png)

### [YoY Rental Price Changes for Every Zipcode Notebook](python/map_of_yoy_rental_rates_by_zip.ipynb)

![Chart1](python/assets/fl_yoy_rental_prices.png)

### [Which Metros Have the Highest Share of Mom and Pop Ownership? Institutional Ownership?](python/table_of_mom_and_pop_vs_institutions_ownership.ipynb)

![Chart1](python/assets/top100_metros_mom_and_pops.png)