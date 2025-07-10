# Algorithmic Trading

Optimizing Algorithmic Trading

---

[![Made withJupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=for-the-badge&logo=Jupyter)](https://jupyter.org/try)	![GitHub License](https://img.shields.io/github/license/shortthirdman/AlgorithmicTrading?style=for-the-badge)	[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/shortthirdman/AlgorithmicTrading/main)	![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/shortthirdman/AlgorithmicTrading?style=for-the-badge)	![GitHub repo size](https://img.shields.io/github/repo-size/shortthirdman/AlgorithmicTrading?style=for-the-badge)	[![Static Badge](https://img.shields.io/badge/Jupyter_Notebooks_Python3-3-brightgreen?style=for-the-badge&logo=jupyter&logoSize=auto&label=Jupyter%20Notebooks%20(Python3))](/notebooks)

---

## Local Development Setup

  - Create a Python virtual environment and activate
	
	```shell
	$ python -m venv --upgrade-deps --clear dev
	$ ./dev/Scripts/activate
	$ export PIP_CONFIG_FILE=".\pip.conf"
	```

  - Install the packages and dependencies as listed in requirements file
	
	```shell
	$ pip install -U -r requirements.txt --no-cache-dir --disable-pip-version-check
	```

  - Start your development `Jupyter Notebook` or `Jupyter Lab` server
	
	```shell
	$ jupyter lab --notebook-dir=.\notebooks --no-browser
	```

---