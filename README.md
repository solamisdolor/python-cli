# python-cli
An unsophisticated cli template for python

## Usage

```python cli.py {command} {args...}```

Running cli.py without parameters will inspect the modules under ```commands``` and their corresponding ```run``` implementation, and print the list on screen.

To add a new command, copy one of the example files under ```commands``` and update ```commands/__init.py__```
