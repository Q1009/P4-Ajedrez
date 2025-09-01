# AJEDREZ
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)  

![Books Online Logo](https://user.oc-static.com/upload/2020/09/22/16007793690358_chess%20club-01.png)  
*(Chess Tournament Management Solution)*

This program aims at managing your local chess club and organize round-robin tournaments. Keep track of players, their ELO, the tournaments' state and much more ! Works offline.
## Get started

> [!WARNING]  
> Make sure you have installed Python version 3.13.3, pip version 25.0.1 and git version 2.39.5.  

- Open any terminal and navigate through your desired directory using the `cd 'directory_name'` command line.

### Requirements

- Start by cloning the GitHub repository by typing the following:  
`git clone https://github.com/Q1009/P4-Ajedrez.git`
- Go in the downloaded directory by typing the following:  
`cd P4-Ajedrez`
- Create your virtual environment by typing the following:  
`python3 -m venv env`

### Installation

- Activate your virtual environment by typing the following:  

    - For Linux Based OS Or Mac-OS.  
`source env/bin/activate`  

    - For Windows With CMD.  
`.\env\Scripts\activate.bat` 

    - For Windows With Power shell.  
`.\env\Scripts\activate.ps1`  

    - For Windows With Unix Like Shells For Example Git Bash CLI.  
`source env/Scripts/activate`

- Install the required packages by typing the following:  
`pip install -r requirements.txt`  

## Running

> [!IMPORTANT]  
> In the main.py file, make sure the url of the website to scrape is correct:

```python
# Instance of object type str as the url of the website
url: str = 'https://books.toscrape.com/'
```

- Run the script by typing the following:  
`python main.py`
- The execution will last for about 5 to 10 mins.  

- Optionally, you can type in the following command to generate a Flake8 report on the code:  
`flake8 main.py --format=html --htmldir=flake-report`
    - In the newly created flake-report directory, open the index.html file with your web browser to see the report  

- Deactivate your virtual environment before closing the terminal by typing:  
`deactivate`

## Data collection

You will then find the **Books** directory in which sub directories, corresponding to every category of books, will contain the following files:

- Books' illustrations
- A .csv file containing:
    - product page url
    - universal product code
    - title
    - price including tax
    - price excluding tax
    - number available (in stock)
    - product description
    - category
    - review rating
    - image url
- A .txt file listing the book's url

## Author

- **Quentin Tellier** *alias* [@Q1009](https://github.com/Q1009)
