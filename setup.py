from setuptools import setup

setup(
    name='Интернет-магазин Дмитрия Шаталова и Евгения Жарикова',
    packages=['OnlineShop'],
    include_package_data=True,
    install_requires=[
        'flask',
    ],
)

