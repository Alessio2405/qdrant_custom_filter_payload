## Qdrant Filter Runtime Generator

This script allows you to dynamically generate Qdrant filters at runtime for querying data using LLMS (Legal Language Models) with agents or tools. With this script, you can easily create complex filters based on specific criteria and apply them to your data queries.


## Features

- Dynamically generate Qdrant filters based on key-value pairs (all extracted from JSON/XML/similar strcture coming from LLM response)
- Easy integration with LLMS tools and agents for querying data.


## Requirements

- Python 3.10 (64 bit)
- Pip
- Qdrant client library


## Installation

- Clean this repository 
```bash
git clone repositoryurl
```

- Install required modules
```bash
pip install -r requirements.txt
```


## Usage

- Modify data inside 'main.py' with yours and then launch
```bash
python main.py
```