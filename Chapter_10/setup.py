import setuptools
setuptools.setup(
    name='rating_stars',
    version='0.1',
    author='YOUR-NAME',
    author_email='YOU-EMAIL@DOMAIN.com',
    description='INSERT-DESCRIPTION-HERE',
    long_description='INSERT-LONGER-DESCRIPTION-HERE',
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
       'Operating System :: OS Independent',
    ],
    keywords=['Python', 'Streamlit', 'React', 'JavaScript', 'Custom'],
    python_requires='>=3.6',
    install_requires=[
       'streamlit >= 0.86',
    ],
)
