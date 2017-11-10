# URB

Brief description

## Installation

### 1. Setup development environment

#### Install necessary dependencies

```
pip install pipenv
pipenv install
```

#### Building g2o bindings

In order to build the bindings we need to install `g2o` and `eigen`. If you have already done this
you can skip to the next step.
```
brew install g2o
brew install eigen
```

To build the bindings you have to navigate to the `bindings` folder and run the default `cmake`, `make` command chain.
```
cd bindings && mkdir build && cd build
cmake ..
make
```

Verify that the binding is working by navigating to the `bindings` directory and running the following command
```
python3 g2o.py
```

It should output
```
WORKS!
None
```

#### 2. Running the project

```
pipenv run python main.py
```

### FAQ

1. Matplotlib cannot be found

```
pipenv shell
echo "backend: TkAgg" >> ~/.matplotlib/matplotlibrc
```
