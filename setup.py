from setuptools import setup, find_packages

INSTALL_REQUIREMENTS = ['fastapi', 'pydantic', 'SQLAlchemy', 'uvicorn']

setup(
	name = 'AddressBookApp',
	description = 'AddressBookApp to demonstarte FastAPI with CRUD Operations',
	version = 'v1',
	packages = find_packages(),
	install_requires = INSTALL_REQUIREMENTS
	)