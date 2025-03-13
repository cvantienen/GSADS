# Project Setup

## Table of Contents

- [Clone repo](#clone-repo)
- [Virtual Environment](#environment)
- [Requirements](#requirements)

## Clone repo

Instructions on how to install and set up the project.

```bash
# Clone the repository -- ssh password protected
git clone git@github.com:cvantienen/GSADS.git 
```

```bash
# Clone the repository -- HTTP **read only** 
git clone https://github.com/cvantienen/GSADS.git
```

## Environment

1. Open a terminal and navigate to the project directory.

2. Create a virtual environment by running the following command:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        .\venv\Scripts\activate
        ```

    - On macOS and Linux:

        ```bash
        source venv/bin/activate
        ```

## Requirements

1. Ensure the virtual environment is activated.

2. Install the required packages by running:

    ```bash
    pip install -r requirements.txt
    ```
