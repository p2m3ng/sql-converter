import os
import click

from sql_converter.settings.settings import Config, CONFIG_FILES_PATH


@click.group()
def cli():
    """"""


@cli.command("config")
@click.option('--name', '-n', required=True, help='Database name')
@click.option('--host', '-h', default='localhost', show_default=True, help='Database host')
@click.option('--port', '-c', type=int, default=3306, show_default=True, help='Database port')
@click.option('--user', '-u', default='root', show_default=True, help='Database username')
@click.option('--password', '-p', required=True, help='Database password')
@click.option(
    '--file', '-f', default=os.path.join(CONFIG_FILES_PATH, 'config.yaml'), show_default=True, help='Config file path'
)
def config(name, host, port, user, password, file):
    """Config file management"""
    config = {
        'db': {
            'name': name, 'host': host, 'port': port, 'user': user, 'password': password
        }
    }
    Config(file=file).dump_to_config_file(config=config)
    click.echo('New config file generated.')
