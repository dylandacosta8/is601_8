## <h1 align=center>IS601_Midterm - Advanced Python Calculator</h1>
---
### Setting up your Local Environment 

<p>This repository contains the dependencies and code for the IS601 Midterm submission for Advanced Python Calculator along with its custom tests and newly added calculator functions</p>

<p><b> On cloning the repository, please use</b></p>
<div>

`pip install -r requirements.txt` or `pip3 install -r requirements.txt`

</div>

---

### Usage
<ol>
<li>To run tests with fake data generated using Faker, use</li>

`pytest --num_records=100 --cov --pylint` <b>OR ---> </b> view at <a href="https://github.com/dylandacosta8/is601_midterm/actions"><b>GitHub Actions</b></a>.

<li>To run the command line utility use one of the following command:</li>

`python main.py`

You can then use the various command line commands like add, subtract, multiply and divide as such:

`add 2 3` or `divide 5 0` or `history help`

<li>You can also use a <b>help</b> command to list the available commands and see a usage guide.</li>


</ol>

---

### Video Demonstration Link - <a href="https://drive.google.com/file/d/1kP6KHu9TradKfYHT4WU0Jt6W0NouZ4br/view?usp=sharing">here</a>

---

### The submission meets the following goals:

<ol>
<li><b>Add, Subtract, Multiply, and Divide</b></li>
<li>Throw exception for <b>divide by zero</b> and test that the exception is thrown.</li>
<li>Use at least one class, at least one <b>static method</b>, at least one <b>class method</b>.</li>
<li>It needs to store a <b>history of calculations</b>, so that you can retrieve the last calculation, add a calculation.</li>
<li><b>Near 100% test coverage, pass pylint</b></li>
<li>Type hints for input parameter types and return types.</li>
<li>Implements a <b>pytest fixture</b> to the tests.</li>
<li>Implements a new command to pytest to generate N number of records, so that you can run the following command: <b>pytest --num_records=100</b> to generate 100 records.</li>
<li>Added a main.py file to serve as an entry point to your program and provide <b>command line utilities</b>.</li>
<li>Covers <b>REPL</b> with four basic commands add, subtract, multiply and divide.</li>
<li>Implements a <b>help command line utility</b> that prints the command dictionary and gives and example of command usage</li>
<li>Uses <b>multiprocessing</b> capabilities to enable commands to run on separate cores.</li>
<li>Uses a <b>.env</b> file to set environment variables that are used for logging verbosity.</li>
<li>Uses <b>logging</b> statements to trace the flow of the program and track application usage and security. This is the log file that is generated when the program is run <a href="https://github.com/dylandacosta8/is601_midterm/blob/main/logs/calc.log"><b>Log File</b></a></li>
<li>Uses <b>Github Action Workflows</b> to run pytests.</li>
<li>Uses various <b>design patters</b> for scalable architecture</li>
<li>Implements try/catch exception blocks that adhere to <b>Look Before You Leap (LBYL)</b> and <b>Easier to Ask for Forgiveness than Permission (EAFP)</b></li>
<li>Includes a well explained, detailed <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/README.md">Documentation</a></b></li>
</ol>

---

### Packages Used

<ol>
<li><b>pytest:</b> The pytest framework makes it easy to write small, readable tests, and can scale to support complex functional testing for applications and libraries.</li>
<li><b>pytest-pylint:</b> Pylint analyses your code without actually running it. It checks for errors, enforces a coding standard, looks for code smells, and can make suggestions about how the code could be refactored.</li>
<li><b>pytest-cov: </b>Coverage.py is a tool for measuring code coverage of Python programs. It monitors your program, noting which parts of the code have been executed, then analyzes the source to identify code that could have been executed but was not.</li>
<li><b>Faker: </b>Faker is a Python package that generates fake data for you.</li>
<li><b><a href='https://docs.python.org/3/library/concurrent.futures.html'>concurrent.futures:</a></b> a high-level interface that asynchronously executes callables.</li>
<li><b>abc:</b> This module provides the infrastructure for defining abstract base classes (ABCs).</li>
<li><b>setuptools:</b> collection of enhancements to the Python distutils that allow developers to more easily build and distribute Python packages.</li>
<li><b>python-dotenv:</b> Used to load the environment variables from the .env file into the program.</li>
<li><b>pandas:</b> Used to create and load data frames into CSV files for advanced history management</li>
</ol>

---
## Core Functionalities

### 1. Calculator Functions using REPL:

<ol>
<li><b>Addition:</b> Adds two numbers</li>
<li><b>Subtraction:</b> Subtracts two numbers</li>
<li><b>Multiplication:</b> Multiplies two numbers</li>
<li><b>Division:</b> Divides two numbers and also catches the divide by zero exception</li>
<li><b>History:</b> Loads,saves,clears and deletes history of the calculator
<li><b>Help:</b> Provides a list of available commands and their usages </li>
</ol>

### 2. Design Patterns for Plugins & Scalable Architecture:
<ol>
<li><u><b><a href="https://refactoring.guru/design-patterns/command">Command Pattern</b></u>:</a> The Command Pattern allowed me to encapsulate requests as objects which works perfectly for handling different commands within the REPL interface. Each calculator operation like add, subtract, multiply, divide and history is represented by a specific command class that inherits from a central Command class. This setup keeps the command behavior consistent and makes it easy to add new operations down the line.

You can see the central Command Class here at <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/calculator/command.py">calculator/command.py</a></b> and the individual subclasses in the files in <b><a href="https://github.com/dylandacosta8/is601_midterm/tree/main/calculator/plugins">calculator/plugins/*.py</a></b>

</li>
<li><u><b><a href="https://refactoring.guru/design-patterns/factory-method">Factory Method</b></u>:</a> The Factory Method pattern helped me create specific command objects based on user input through the CommandFactory class. This pattern supports dynamic command loading, which makes it much easier to integrate new plugins into the calculator without changing the REPL code. This was initially handled by <a href="https://github.com/dylandacosta8/is601_6/blob/main/setup.py">setup.py</a> in previous submissions which worked similarly but did not create the scalability that the Factory Method provides.

The CommandFactory class in <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/calculator/factory.py">calculator/factory.py</a></b> serves as a registry for all available commands and everytime a file is uploaded to the calculator/plugins directory it automatically registers, mapping its name to the corresponding command class. This lets me add new commands as plugins without touching the REPL code.

</li>
</ol>

### 3. Advanced Data Handling and Calculation History Management with pandas: 

Pandas is employed to manage calculation history effectively, providing functionalities to read from and write to CSV files. 

This enables users to keep track of and retreive their calculations using the `history show` command, save to a file using the `history save <filename>` command and load and access data from other save files using the `history load <filename>` command.

The history is stored by default in <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/data/history.csv">data/history.csv</a></b> unless specified otherwise.

### 4. Multicore Processing capabilities:

The calculator utilizes the `concurrent.futures` module to enable multicore processing, allowing commands to run on separate cores. 

This significantly improves performance and responsiveness during calculations.

### 5. Professional Logging Practices:

Logging is integrated into the application to monitor its behavior and capture essential events. This practice aids in debugging and provides insights into user interactions, ensuring a reliable user experience.

It has been implemented using the inbuilt logging module that reads the <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/.env">dotenv(.env)</a></b> file in the project directory to retreieve the `ENV` environment variable. This can be set to `dev`, `uat` or `prod` to adjust the verbosity of the logs with dev being the most verbose to prod having minimal verbosity for debugging. The logs are then written to <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/logs/calc.log">logs/calc.log</a></b> using a professional format.

### 6. Try/catch exception handling with LBYL and EAFP
<ol>
<li><b>Look Before You Leap (LBYL):</b> This approach checks for potential errors before executing operations, enhancing reliability.</li>
<li><b>Easier to Ask for Forgiveness than Permission (EAFP):</b> This principle allows for handling errors gracefully when they occur, providing a more streamlined user experience.</li>
</ol>

<ul><h4> Cases where LBYL and EAFP were used:</h4>
<li><b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/calculator/plugins/divide.py#L20">Handling Division by Zero:</a></b> EAFP was used here as it avoids preemptively checking all the possible division operations instead and directly handles the error when it occurs basically performing division and only asking for forgiveness if it fails due to a ZeroDivisionError.</li>
<li><b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/calculator/__init__.py#L54">Loading and Saving History Files:</a></b> LBYL is effective here as it prevents potentially problematic operations ahead of time. It was used to check if the file exists and meets the naming conventions(appropriate path) before proceeding to open it.</li>
<li><b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/main.py#L121">Command Validations in REPL:</a></b> LBYL is useful to validate user inputs and check if the command typed in exists in the command dictionary to avoid errors that might confuse or disrupt the user experience.</li>

### 7. Test Automation using pytest and Faker:

The application employs `pytest` for running tests and `Faker` for generating a vast amount of random and realistic test data, ensuring that various scenarios are covered and enhancing the reliability of the code.



### 8. Professional Code Coverage and Linting:

The submission averages above 90% code coverage using `pytest-cov` to ensure that extensive tests have been written to ensure a robust testing environment.

PEP 8 standards have also been maintained for the project using `pylint` to make sure the quality of the code adheres to industry best practices.

### 9. Code Management using Version Control:

Git best practices such as `maintaining separate branches` for each feature, `pull requests` to merge feature branches with the main branch and having `appropriate comments for each commit` to help keep track of work have been used throughout the duration of the project before pushing it to an online VCS like GitHub.

### 10. Continuous Integration (CI) using GitHub Actions:

GitHub Actions has been used to implement workflows for custom tests using pytest, Faker as well as linting using pylint and coverage using pytest-cov on commit to the main and pytest_updates branches as a first step towards CI.

You can find the <b><a href="https://github.com/dylandacosta8/is601_midterm/blob/main/.github/workflows/pytest.yml"> Pytest Workflow</a></b> here.

---

<b>Note:</b> Test Cases have 100% coverage for all the above Calculator Functions using pytest. Use the following commands to execute the tests.

`pytest`
`pytest --pylint`
`pytest --pylint --cov`

---