from setuptools import find_packages, setup

requirements = [
    "dicom-anonymizer @ git+https://github.com/medcognetics/dicom-anonymizer.git@v1.0.7-fork",
    "colorama",
    "pydicom @ git+https://github.com/medcognetics/pydicom.git",
]

extras = {"dev": ["pytest", "black", "flake8", "autoflake", "autopep8", "isort"]}

setup(
    name="dicom_phi_check",
    version="0.0.0",
    packages=find_packages(),
    install_requires=requirements,
    extras_require=extras,
    python_requires=">=3.8.0",
)

