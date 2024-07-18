# HBP survey plots 
This repository hosts the survey plots of the paper `Multidisciplinary and collaborative training in neuroscience: Insights from the Human Brain Project Education Programme`.
The figures 8-11 in the paper are created by the Python file `plot_survey_results.py`. The plots are controlled via arguments which can be specified via the terminal (for details see [Usage](https://github.com/alperyeg/hbp_survey_plots?tab=readme-ov-file#usage)). 

## Description 
The script `plot_survey_results.py` plots a figure depending on the input:
- If the input is `SGA1-2_summary2.xlsx`, the figure depicts the pooled average results from participants across several HBP conferences conducted in SGA1 and SGA2. It has three subplots (`Benefit for participant`, `Quality of Lectures` and `Overall Satisfaction`) and visualizes the survey outcome of several questions as horizontal stacked bars.
- If the input is `SGA3_summary.xlsx` the plots shows the outcomes for the SGA3 phase. This plot has four subfigures (`Benefit for participant`, `Quality`, `Virtual format` and `Overall Satisfaction`).
- The plot with the input `YRE Surveys_SGA1-2_summary.xlsx` displays the average survey results of the `Young Researcher Events` held in SGA1 and SGA2. The structure follows the plot as for the HBP conferences in SGA1 and SGA2. 
- Similarly, the plot with the input `YRE Surveys_SGA3_summary.xlsx` shows the results of the `Young Researcher Events` in SGA3. 

Another file is `plot_teaslides_survey.py`, which was used in an early version of the paper, and is uploaded here for completeness. It is a single figure and only shows the participants' (average) `Overall Satisfaction` pooled from all Tea and Slides online events. 


## Requirements
There are not many requirements to run the code, the additional, three Python packages are: 
- matplotlib
- pandas
- seaborn

Optionally to create a [Likert graph](https://github.com/nmalkin/plot-likert) (can be installed via `pip install plot-likert`): 
- plot_likert 

## Usage
The file `plot_survey_results.py` requires the input data `SGA1-2_summary2.xlsx`, `SGA3_summary.xlsx` `YRE Surveys_SGA1-2_summary.xlsx` or `YRE Surveys_SGA3_summary.xlsx`. These files are located in the main repository. 
To load one of the files and plot a figure use the argument `--filename`, e.g. `python plot_survey_results.py --filename SGA1-2_summary2.xlsx`. 
- `--filename`, requires the name of the file as a string. A path can also be supplied. If no filename is given then the script assumes the file `SGA1-2_summary2.xlsx`
- `--total_mean`, if specified it prints out the average response rate of the participants.
- `--total_std`, if specified it prints out the standard deviation of the participants' response rate. 
- `--plot_type`, defines the type of the plot. Available are `stacked` plotting horizontal stacked histograms or `likert` for Likert graphs. If not specified the default is `stacked`. 
- `--percentage`, defines if percentages or absoulte values will be printed on the bars.
- Thus, if no arguments are given, i.e. `python plot_survey_results.py`, the script assumes that `python plot_survey_results.py --filename SGA1-2_summary2.xlsx` is called.

For the final version of the manuscript we decided not use the plot for the tea and slides survey. The script `plot_teaslides_survey.py` follows the same command scheme as above. The file requires the input `HBPTeaandSlides_overall_satisfaction.xlsx`. 

### Figure specific commands
Below are the arguments to create the figures from the manuscript: 
- Fig.8: `python plot_survey_results.py --filename SGA1-2_summary2.xlsx --plot_type stacked --total_mean --percentage`
- Fig.9: `python plot_survey_results.py --filename SGA3_summary.xlsx --total_mean --percentage`
- Fig.10: `python plot_survey_results.py --filename YRE Surveys_SGA1-2_summary.xlsx --total_mean --percentage`
- Fig.11: `python plot_survey_results.py --filename YRE Surveys_SGA3_summary.xlsx --total_mean --percentage`
