# Guess the Drawing

This is a project created by Andy Lau and Michael Singer for CSE 298 @ Lehigh University. The web app allows users to create and join rooms where they compete and draw to decide the ultimate winner for the best guesser or best drawer.  

## Installation

To set up the project environment, follow these steps:

1. Clone the repository to your local machine.

   ```bash
   git clone https://github.com/mis825/lau-singer.git
2. Create a Python virtual environment.

   ```bash
   cd lau-singer
   python -m venv venv
3. Activate the virtual environment. 

- On Windows
    ```bash 
    . venv\Scripts\activate
- On Unix or MacOS
    ```bash
    source venv/bin/activate
4. Make sure you select the venv python interpreter. If it doesn't show...
    - In VSCode open your command palette — Ctrl+Shift+P by default

    - Look for Python: Select Interpreter

    - In Select Interpreter choose Enter interpreter path... and then Find...

    - Locate env folder, open Scripts folder , and choose python or python3

5. Install the required dependencies using pip.
    ```bash
    pip install -r requirements.txt

## Configuration 
1. Create a .env file in the project root directory (**make sure that you don't commit this file!**).

    NOTE: The .env file is used for storing sensitive information and configuration parameters. Populate it with any required environment variables.

    Add the database url like this: 
    ```env
    DATABASE_URL=your_database_url 

2. Update the project code to use environment variables.
    ```python
    import os
    from dotenv import load_dotenv

    load_dotenv()

    # Access environment variables using os.getenv("VARIABLE_NAME")

## Usage
To do

## Contributing
To do

## License 



