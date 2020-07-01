import click

from clients.services import ClientService
from clients.models import Client


@click.group()
def clients():
    """Manages the clients lifecycle"""
    pass


@clients.command()
@click.option(
    '-n',
    '--name',
    type=str,
    prompt=True,
    help='The client name')
@click.option(
    '-c',
    '--company',
    type=str,
    prompt=True,
    help='The client company')
@click.option(
    '-e',
    '--email',
    type=str,
    prompt=True,
    help='The client email')
@click.option(
    '-p',
    '--position',
    type=str,
    prompt=True,
    help='The client position')
@click.pass_context
def create(ctx, name, company, email, position):
    """Creates a new client"""
    client = Client(name, company, email, position)
    client_service = ClientService(ctx.obj['clients_table'])

    client_service.create_client(client)

    # Listing clients after create one
    ctx.invoke(list)


@clients.command()
@click.pass_context
def list(ctx):
    """List all clients"""
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_clients()

    click.echo('-' * 100)
    click.echo(
        '                  ID                 |   NAME   |   COMPANY   |   EMAIL   |   POSITION   ')
    click.echo('-' * 100)

    for client in client_list:
        click.echo('{uid} | {name} | {company} | {email} | {position}'.format(
            uid=client['uid'],
            name=client['name'],
            company=client['company'],
            email=client['email'],
            position=client['position']
        ))

    click.echo('-' * 100)


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def update(ctx, client_uid):
    """Update a client"""
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client = _update_client_flow(Client(**client[0]))
        client_service.update_client(client)

        click.echo('Client updated')
    else:
        click.echo('Client not found')

    # Listing clients after create one
    ctx.invoke(list)


def _update_client_flow(client):
    click.echo('Leave empty if you don\'t want to modify the value')

    client.name = click.prompt(
        'Enter the new name', type=str, default=client.name)
    client.company = click.prompt(
        'Enter the new company', type=str, default=client.company)
    client.email = click.prompt(
        'Enter the new email', type=str, default=client.email)
    client.position = click.prompt(
        'Enter the new position', type=str, default=client.position)

    return client


@clients.command()
@click.argument('client_uid', type=str)
@click.pass_context
def delete(ctx, client_uid):
    """Deletes a client"""
    client_service = ClientService(ctx.obj['clients_table'])

    client_list = client_service.list_clients()

    client = [client for client in client_list if client['uid'] == client_uid]

    if client:
        client_service.delete_client(client[0])

        click.echo('Client deleted')
    else:
        click.echo('Client not found')

    # Listing clients after create one
    ctx.invoke(list)


all = clients
