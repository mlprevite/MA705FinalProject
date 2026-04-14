# MA705 Final Project

This repository contains files used in the MA705 dashboard project.

The final dashboard is deployed on Heroku [here](https://ma705masscand2020donations.herokuapp.com/).

## Data Respository Set Up
This data repository is set up into three different folder, CleaningContributionData, CleaningCandidateData, and FinalDataFrame. The CleaningContributionData folder holds the raw candidates file and the code file of CleaningCandidateData cleans up this data frame. The CleaningContributionData folder holds the raw Contributions202 file and the code file of CleaningContributionData cleans up this data frame. The FinalDataFrame folder holds the cleaned up CandidatesMaster dataframe and the Contributions2020Master dataframe, and the code file of FinalDataFrame that created the final data frame used in the dashboard. The dashboard files are not in a folder for ease of access. 



## Dashboard Description

The dashboard summarizes all of the campaign donation information for all candidates running for office in the 2020 election cycle in Massachusetts obtained from https://www.ocpf.us/Home/Index. It allows a user to find out information on campaign donations given to candidates over the 2020 election cycle based on the following three search criteria:
- Office Sought: a list of all offices in Massachusetts that are being run for.
- Office District: a list of all districts in Massachusetts that have an office being run for.
- Campaign Donation Measures: a measure of campaign donations with three categories; Sum, Count, and Average.

Please note that this Dashboard is functional in design and presentation.


### Data Sources

Candidate data was pre cleaned in excel. Empty rows were deleted in excel. Candidates who had "Statewide" in the column "Office Type Sought" had their office title from the column "District Name Sought" as this was the only office that had the office title within the "District Name Column". Because these offices were statewide offices corisponding to no districts, the state name, Massachusetts, was put in place of the district name in the "District Name Sought" column. So for every statewide office, the name of the office is included within the "Office Type Sought" column.

List of data sources and references used in this course project:

https://www.ocpf.us/Home/Index

https://dash.plotly.com/installation

https://dash.plotly.com/advanced-callbacks

https://dash.plotly.com/datatable/callbacks

https://dash.plotly.com/dash-html-components

https://towardsdatascience.com/reordering-pandas-dataframe-columns-thumbs-down-on-standard-solutions-1ff0bc2941d5

https://stackoverflow.com/questions/23668427/pandas-three-way-joining-multiple-dataframes-on-columns

https://dash.plotly.com/urls

Note: Some sources were used in the preprocessing and cleaning of data.


