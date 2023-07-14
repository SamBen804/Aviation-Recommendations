# PrimeAir Aircraft Purchase Recommendations
Authors: [Catherine Langley](https://www.linkedin.com/in/catherine-langley-4b904a1ab/),  [Aung Si](https://www.linkedin.com/in/aungsi99/), and  [Sam Whitehurst](https://www.linkedin.com/in/sam-whitehurst23/) 

## Executive Summary 

This project analyzes the potential risks of three sizes of aircraft for private and commercial use by company new branch, PrimeAir. 

* Descriptive analysis of aviation accidents produced a Danger Zone Scale based on historic accidents related to plane models. 
* Descriptive analysis of the commercial aircraft inventory found the most commonly used commercial planes in three size categories. 
* The Danger Zone Scale was used to identify the aircraft models with the lowest historic reported risk. 

PrimeAir can use this analysis to select the lower risk planes for both commercial and private use from the most popular aircraft in recent commercial inventory. 

## Business Problem

PrimeAir may be able to reduce risks in their industry expansion by including the results of this analysis in their purchase decisions. Following these recommendations will: 

- Improve day-to-day operations by reducing potential interruptions, 
- Reduce the probability of aircraft repair/loss, and
- Reduce the probability of human injury and loss of life. 

## Our Data


### Aviation Accident Database

The National Transportation Safety Board’s (NTSB’s) Aviation Accident Database lists reported aviation accidents in the United States and related areas. The NTSB is required by law to investigate all civil aviation accidents and to publically report its findings. This database is a part of the mandated reporting process. 

This database shares all reported accidents with the date of the accident, the aircraft make and model, degree of damage to the aircraft and degree of injury/loss to human life. 

* Where we got it: 
    * Download from [Kaggle's Aviation Accident Database & Synopses, up to 2023](https://www.kaggle.com/datasets/khsamaha/aviation-accident-database-synopses). 
    * Includes  AviationData.csv and USState_Codes.csv.
* Original Data: 
    * Download from [NTSB](https://www.ntsb.gov/Pages/AviationQuery.aspx) website.  
* Explanatory Information: 
    * [GILS Aviation Accident Database](https://www.ntsb.gov/GILS/Pages/AviationAccident.aspx) webpage.
    * Includes a full definition of accidents vs. incidents.
* Data Limitations: 
    * Reports are primarily accidents: serious personal injury and serious aircraft damage. 
    * Reported aircraft incidents are in a separate Federal Aviation Administration [incident database](https://www.asias.faa.gov/).
    
### Inventory of Aircraft Database 

This BTS database lists the yearly aircraft inventory of large certified carriers in the United States.  Each entry includes the year of inventory, the plane's unique serial number, and the manufacturer and model of the aircraft. 

* Where we got it: 
    * The Bureau of Transportation Statistics’s (BTS) [Schedule B-43 Database: Annual Inventory of Airframe and Aircraft Engines](https://www.transtats.bts.gov/Fields.asp?gnoyr_VQ=GEH).
    * Found in T_F41SCHEDULE_B43.csv.
    * We downloaded the data from the website, selecting all years, and all columns into the file. 
* Explanatory information: 
    * The database is part of the  [Form 41 Financial Database: Air Carrier Financial Reports](https://www.transtats.bts.gov/Tables.asp?QO_VQ=EGI&QO_anzr=Nv4%FDPn44vr4%FDSv0n0pvny%FDer21465%FD%FLS14z%FDHE%FDSv0n0pvny%FDQn6n%FM&QO_fu146_anzr=Nv4%FDPn44vr4%FDSv0n0pvny). 
    * Form 41 Financial Reports is collected by the Office of Airline Information of the Bureau of Transportation Statistics from large certified carriers. 
    * More information on the BTS [TranStats](https://www.transtats.bts.gov/DatabaseInfo.asp?QO_VQ=EGI&Yv0x=D) webpage.   
* Data Limitations:
    * Only includes large certified carriers which are carriers that have the annual operating revenues of 20 million USD.  

### Special Feature: The Danger Zone Scale 

The danger zone scale attributes a scalar value to aircraft damage and human injury per accident
* Combines weighted values of aircraft damage with injury to human life.  
* Aircraft damage is weighted 75% since aircraft malfunction involves potentially greater human injury.

## Method

We used descriptive analysis which provides a useful insight into the historic risk level of the models of top ten most common models in recent inventory. 

## Data Understanding

Our two datasets originate from the National Transportation Safety Board (NTSB) and the Bureau of Transportation Statistics (BTS), respectively. The former comprises >87,000 records of mandated US aircraft accident data ranging from 1962 to 2022, with the inclusion of human injury and aircraft damage. The latter contains >120,000 records of mandated inventory data of US aircraft ranging from 2006-2022.

### Plane Inventory Data

Our plane inventory dataset contains information such as the serial number of the plane, its number of seats, an The records range from the years 2006 - 2022 - though the number of records are much greater than our accidents dataset, in terms of years this dataset is much smaller than our accidents dataset.

## Data Preparation and Cleaning

We now clean the two datasets by normalizing our column names and only keeping the relevant columns.

For our accidents dataset, we're only concerned information that tells us the year, make, model, extent of aircraft damage and human injury (we will later engineer a score off of each of these), and the count of the different types of injuries involved in the accident. To eventually be able to work with the two datasets in tandem, we transformed the make values to all lowercase, and only kept the manufacturer names as part of the value. For the model values, we stripped them of alphanumerics, and kept only the first three numbers of the model value.

For our inventory dataset, we keep the year, make, model, and number of seats columns (we will later engineer a plane size feature off of the number of seats). We transformed the makes and models of this dataset the same way we did for our accidents dataset.

Now that we have our datasets cleaned, we can engineer a few features within each that serve as the crux of our analysis.

## Feature Engineering

### Make-Model Feature

The first feature we engineer is the `make_model` feature. We do this for both datasets so that we can parse through these values for both easily.

### Human Injury and Aircraft Damage Features

An accident can be broken down into two metrics: the extent of aircraft damage, and the extent of injury it inflicts upon the passengers involved. We quantified these two metrics below, in order to eventually quantify the danger level of each plane.

![Large Plane Historic Inventory   Recorded Accident Counts (2)](https://github.com/SamBen804/Aviation-Recommendations/assets/132294191/b42ec646-3c0b-4ed5-9654-7850fcc569f6)

#### Human Injury Feature

We now engineer a `human_injury` feature, which categorizes the accidents as such:
1. We categorize the accident as `'Fatal'` if it has $>1$ fatalities.
2. We categorize the accident as `'Serious'` if it has $>1$ serious injuries.
3. We categorize the accident as `'Minor'` if it has $>1$ minor injuries.
4. We categorize the accident as `'Unknown'` if the injury data is missing.

Off of the  `human_injury`, we compute a `human_injury_numeric` in order to quantify the categories. The computation for this score is broken down as follows:
1. We give a score of 4 for all accidents labelled `'Fatal'`
2. We give a score of 3 for all accidents labelled `'Serious'`
3. We give a score of 2 for all accidents labelled `'Minor'`
4. We give a score of 1 for all accidents labelled `'Unknown'`

These raw scores are then transformed into our `human_injury_numeric` feature, which is the raw scores above min-max scaled and multiplied by 10 so as to give us a normalized score with ranging from 0-10.

#### Aircraft Damage Feature

The `'aircraft_damage'` column present in the accidents dataset already categorizes the damage experienced by the aircraft in a particular accident. Similar to how we scored the extent of human injury, we:
1. gave a score of 4 for all accidents labelled `'Destroyed'`
2. gave a score of 3 for all accidents labelled `'Substantial'`
3. gave a score of 2 for all accidents labelled `'Minor'`
4. gave a score of 1 for all missing labels within the `'aircraft_damage'` column.

These raw scores are then transformed into our `'aircraft_damage_numeric'` feature, which is the raw scores above min-max scaled and multiplied by 10 so as to give us a normalized score with ranging from 0-10.

### Aggregating a Danger Zone Score

Now that we have our two scores pertaining to human injuries and aircraft damage, respectively, we can aggregate them to get a danger zone score. The danger zone score is **computed as the weighted sum of `human_injury_numeric` and `aircraft_damage_numeric`**. We placed more weight on the `aircraft_damage_numeric`, as we believed the extent of plane damage is indicative of higher potential of lives lost.

![Mean Danger Score Calculated (1)](https://github.com/SamBen804/Aviation-Recommendations/assets/132294191/9eccf779-9af0-4b83-9c26-ccf8ac906884)

![Mean Danger Score Calculated](tableau_dashboard_and_visualizations/Mean Danger Score Calculated (1).png)

Mean Danger Score Calculated (1).png

### Plane Size Feature

To give a more granular account of danger levels across the plane, we categorized the planes by sizes within our inventory dataset: 
1. Planes with $3-20$ seats are categorized as `'small'`
2. Planes with $21-100$ seats are categorized as '`medium`'.
3. Planes with $>100$ seats are categorized as `'large'`.* 

### Analysis

To understand where each plane stood relative to each other in terms of the human_injury scores, aircraft damage scores, and danger zone scores, we took the mean of each of these scores with the planes binned into their respective sizes. 

We took the `number_of_planes` column to be the occurence of the plane make, model, and size within the inventory dataset, and the `recorded_accidents_for_plane_model` to be all the planes within the inventory set with recorded accidents within the accidents dataset. We then computed a '`record_accidents_per_plane_in_inventory'` metric, which is the former divided by the latter - we did this to get the likelihood/frequency of accidents of a specific model by factoring in the count of the plane in existence; had we not factored in the inventory count, the frequency of accidents of any given plane will be skewed.

![Large Plane Recorded Accident Ratio Per Inventory](https://github.com/SamBen804/Aviation-Recommendations/assets/132294191/50af2a97-1af6-4e49-865b-b7e0421f97f4)

## Tableau Dashboard

Our Tableau Dashboard can be found [here](https://public.tableau.com/app/profile/sam.whitehurst/viz/RegionalPlaneRecordedAccidentRatioPerInventory/PrimeAirAircraftPurchaseRecommendationsDashboard).
