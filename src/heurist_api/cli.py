import click

from heurist_api.dump_records import dump_records


@click.group
def cli():
    pass


@cli.command("dump")
@click.option("-d", "--database", type=click.STRING, required=False)
@click.option("-l", "--login", type=click.STRING, required=False)
@click.option("-p", "--password", type=click.STRING, required=False)
@click.option("-o", "--outdir", type=click.Path(), required=True)
@click.option("-f", "--form", type=click.Choice(["json", "csv"], case_sensitive=False))
@click.option("-i", "--id", type=click.STRING, multiple=True)
def dump(database, login, password, outdir, form, id):
    """_summary_"""
    dump_records(
        database=database,
        login=login,
        password=password,
        output=outdir,
        record_ids=id,
        form=form,
    )


if __name__ == "__main__":
    cli(obj={})
