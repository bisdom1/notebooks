# 🛢️ PGK 👶 🐍 workshop
Introduction to python data analysis with an example analysing whether there is any correlation between seismicity and production/injection in an oil field.

To run this script, you need a Python 3.x environment with **numpy**, **pandas** and **plotly**.

## 🛠️ Recommended set-up
There are multiple ways to install Python on your system, but for this workshop the below steps are the easiest.
1. Install the Anaconda python environment from the [Anaconda website](https://www.anaconda.com/products/individual). This includes python, Jupyter notebooks, and a set of pre-installed packages for data analysis and machine learning.
2. The **plotly** package does not come pre-installed, but can be added by:
    1. Starting **Anaconda Prompt** (search for anaconda prompt in your windows program folder)
    2. A window opens showing something like `(base) C:\>`. 
    3. Type `conda install plotly` and press enter, the **plotly** library and other dependencies will be automatically installed (if this does not work, try `pip install plotly` instead).
    4. Close the window once done.
    
## 🖥️ Running python code
In this workshop we use jupyter notebooks to easily run code and show results. You can use any text editor to write python scripts, but the interactive environment of these notebooks is a good place to start when you're new to Python. Note that Anaconda comes with a pre-installed python code editor called **Spyder** and with **jupyter** notebooks. Both can be found under the Anaconda program folder. To run jupyter:
1. Look for/search for **jupyter** in your programs folder (it's installed under Anaconda).
2. A juypter command window will open, and shortly after a browser window will be opened that brings you to the jupyter home page.
3. From this page, you can start a new notebook via the **New** button (top right), or you can upload and open an existing notebook file using **Upload**.
4. You can also use **Upload** to upload data files that you are using in your scripts.

For more info see https://jupyter-notebook.readthedocs.io/en/stable/

## 🥅 of this workshop
Using spreadsheet data as a basis, we will do some basic data processing and analysis to look into a microseismic dataset and a set of wells to see if there is any pattern between production/injection and seismicity. For data analysis we make use of **pandas**, a popular library for processing structured data (i.e. spreadsheets) and for plotting we make use of **plotly**, which is optimized for plotting pandas objects.

The aim of this workshop is to demonstrate some of the data processing and visualization powers of python and to show specifically some of the advantages of python over Excel.
___
