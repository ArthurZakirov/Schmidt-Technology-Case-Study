# **Case Study**: How Schmidt Technology can identify high risk supplier in their supply chain using their ERP data

### Table Of Contents

- [The Task](#the-task)
- [Setup](#setup)
- [Usage](#usage)

## The Task
Imagine you want to draft a first MVP showing how to calculate a quantitative risk score for each supplier based on the customer’s data. Think about the different types of risk that are possibly connected to managing a global supplier base.

You will use a Jupyter notebook (.ipynb) to clean the data, perform calculations and transform it into a table format. You can use all the data and come up with creative ideas what to infer from it. You’re free to make any assumption but be prepared to explain them.

As part of an internal alignment you will meet up with your team and discuss your approach. The following questions should serve as a guidance:

1. **Your result:** What is the result of your risk calculation? What are patterns in the data? Summarize the findings you generated.
2. **Your approach:** Guide us through your code and explain how you transformed the data. What did you notice?
3. **Next steps:** How would you improve this MVP for Schmidt if you had more time & resources? If you decided to scale this from 1 to 100+ customers - what would you change? What limitations could your MVP have?

## Setup
1. Create a new virtual environment by running the following in your command line
```bash
python -m venv venv
```

2. Activate the environment by running the following in your command line
```bash
venv/Scripts/activate
```

3. Install the required dependencies by running the following in your command line
```bash
pip install -r requirements.txt
```

4. Create an ```.env``` file inside the project root directory with your mysql database login data
```yml
USER=<your/user/name>
PASSWORD=<your/password>
```

5. Positon the raw data into the correct places
```python
file_paths = [
    'data/raw/customer/addresses.csv',
    'data/raw/customer/articles.csv',
    'data/raw/customer/orders.csv',

    'data/raw/external/indices.csv',
    "data/raw/external/suppliers.csv"
]
```

## Usage 
Open the jupyter notebook ```case_study_schmidt_technology.ipynb``` and run the cells.
