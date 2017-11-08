# URB

Brief description

## Installation

#### 1. Install pipenv

```
pip install pipenv
```

#### 2. Install dependencies

```
pipenv install
```

#### 3. Run the project

```
pipenv run python main.py
```

### FAQ

1. Matplotlib cannot be found

```
pipenv shell
echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
```
