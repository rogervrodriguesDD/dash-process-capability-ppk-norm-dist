# Dashboard for Capability Control of Process (Ppk index)

## Description

This project is a simple example of a report for monitoring the *Ppk* index as parameter of the
Capability of the production process. In this example, the production process is considered continuous and
the probability distribution of the monitored variables is Gaussian. Also, the data used is generated
in the execution of the application.

**Screenshots of the application**

![Screenshot of the index report](./docs/screenshot_index_report.png)


![Screenshot of the control chart](./docs/screenshot_control_chart.PNG)


## Documentation

**Running the application**  

After cloning the project, install the application dependencies with the command `pip install -r requirements.txt`. Then, to run the application execute the command.

`python src/app.py --host=localhost --port=8080 --debug=False`

The arguments `--host`, `--port`, and `--debug` are optional and their default values are set in the `src/config/base/conf.yml` file.

**Basics on Capability Control of Process**
Read a little of the basics [here](docs/basics_on_cap_control.md).

**About the dashboard**
Undestand a little more about the dashboard [here](docs/about_the_dashboard.md).

## Structure of the project
------------

The project has the following structure.

```
├── docs               <- Project documentation
├── notebooks          <- Project related Jupyter notebooks
│
├── src                <- Project source code
|   |
|   ├── conf           <- Configuration files
|   |   |
|   |   ├── base       <- Configuration files that can be registered in the repository
|   |   |   |
|   |   |   └── conf.yml          <- File with all basic parameters needed to run the application
|   |   |
|   |   └── local     <- Configuration files with sensible informations (as credentials, for example)
|   |
|   ├── data          <- Files related to functions or classes to generate or load data
|   |
|   ├── logs          <- Files related to logging functions
|   |
|   ├── process_capability_index  <- Files related functions used to calculate the capability indices
|   |
|   ├── visualization <- Files related to functions or classes to generate the figures
|   |
|   └── app.py         <- Main file of the application, which has the execution function
|
└── .gitignore         <- Prevent staging of unnecessary files to git
```

## TODOs

- [x] 1. Need: Documentation of the classes and functions
- [x] 2. New feature: Add a Dropdown to access the reports for different plants
- [x] 3. Layout fix: Remove yticks values from the Histogram graph.
- [x] 4. Layout improvement: Add index values in the Bar graphs.
- [x] 5. Layout improvement: Add specification limits values in the Control Chart.
- [x] 6. Layout improvement: Add average value in the Control Chart.
- [x] 7. QA: Create unit tests.
- [x] 8. Improvement: Create function to change app configuration through line command arguments.
