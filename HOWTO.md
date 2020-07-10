# Packaging the project
Here is all the details: https://packaging.python.org/tutorials/packaging-projects/

Once you have an account on pypi.org the only thing you have to do to upload a new version/distribution is:
- Update `setup.py` with the version and all needed.
- `python3 setup.py sdist bdist_wheel`
- `python3 -m twine upload dist/*`
