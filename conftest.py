import os

def pytest_configure(config):
  os.environ['SIMPLE_SETTINGS'] = 'config.test'
  return config

def pytest_unconfigure(config):
  os.environ['SIMPLE_SETTINGS'] = 'config.development'
  return config