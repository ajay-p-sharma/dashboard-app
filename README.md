# dashboard-app
## About
Dash is an open source library for creating interactive dashboards. This app is to demonstrate how you can build a dashboard with different types of plots for data visualization. Dash can be used to create web based application and Jupyter applications.
- Core and HTML are the two components of Dash. 

- The **dash_html_components** library has a component for every HTML tag. 

- The **dash_core_components** describe higher-level components that are interactive and are generated with **JavaScript, HTML, and CSS** through the **React.js** library. 

- A callback function is a python function that is automatically called by Dash whenever an input component's property changes. Callback function is decorated with `@app.callback` decorator. 

- Callback decorator function takes two parameters: Input and Output. Input and Output to the callback function will have component id and component property. Multiple inputs or outputs should be enclosed inside either a list or tuple.

You can read more about Dash here https://dash.plotly.com/


## Downloading the app
You can download and test this app on your local computer in two ways. 
1. Clone this repository on your local machine using git CLI
```bash
$ git clone https://github.com/ajay-p-sharma/dashboard-app.git
```
2. Download the client code using the link https://github.com/ajay-p-sharma/dashboard-app/archive/master.zip

## Installation
The app is built using python3.9. It will work best with python3.9 or higher. After you have downloaded the app from github, do the follwing

```bash
$ cd <cloned project directory>
```
#### Create virtual environment using python3
```bash
$ python3 -m venv env
```
#### Activate virtual environment
```bash
$ source env/bin/activate
```
#### Install project dependencies
```bash
$ cat requirements.txt | xargs -n 1 pip install
```
## To run the client locally
```bash
$ python main.py
```
To test go to url http://127.0.0.1:8050/. You should see dropdown options for creating reports.
