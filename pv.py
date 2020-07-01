import click

from clients import commands as clients_commands

CLIENT_TABLE = '.clients.csv'


@click.group()
@click.pass_context
def cli(ctx):
    ctx.obj = {}
    ctx.obj['clients_table'] = CLIENT_TABLE


cli.add_command(clients_commands.all)
