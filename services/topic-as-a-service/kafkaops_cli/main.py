from __future__ import annotations

import json
from typing import Optional

import typer

from .catalog import load_catalog
from .health import cluster_health
from .topics import (
    alter_topic_configs,
    compute_lag,
    create_topic,
    delete_topic,
    describe_topic,
    get_topic_configs,
    list_topics,
)

app = typer.Typer(add_completion=False, help="KafkaOps CLI (standard operations for support/MCO).")
topics_app = typer.Typer(add_completion=False, help="Topic operations.")
app.add_typer(topics_app, name="topics")


@app.command("health")
def health(bootstrap: str = typer.Option(..., "--bootstrap", help="bootstrap.servers"), json_out: bool = typer.Option(False, "--json")):
    out = cluster_health(bootstrap)
    if json_out:
        typer.echo(json.dumps(out, indent=2))
    else:
        typer.echo(f"bootstrap={out['bootstrap']}")
        typer.echo(f"brokers={out['broker_count']} controller_id={out.get('controller_id')}")
        for b in out["brokers"]:
            typer.echo(f" - broker id={b['id']} {b['host']}:{b['port']}")


@topics_app.command("list")
def topics_list(
    bootstrap: str = typer.Option(..., "--bootstrap"),
    json_out: bool = typer.Option(False, "--json"),
):
    t = list_topics(bootstrap)
    out = {"count": len(t), "topics": t}
    typer.echo(json.dumps(out, indent=2) if json_out else "\n".join(t))


@topics_app.command("describe")
def topics_describe(
    name: str,
    bootstrap: str = typer.Option(..., "--bootstrap"),
    show_configs: bool = typer.Option(False, "--configs"),
):
    info = describe_topic(bootstrap, name)
    if show_configs:
        cfg = get_topic_configs(bootstrap, name)
        info["configs"] = cfg
    typer.echo(json.dumps(info, indent=2))


@topics_app.command("apply")
def topics_apply(
    bootstrap: str = typer.Option(..., "--bootstrap"),
    file: str = typer.Option(..., "-f", "--file", help="YAML catalog file"),
    dry_run: bool = typer.Option(False, "--dry-run"),
):
    specs = load_catalog(file)
    existing = set(list_topics(bootstrap))
    actions = []
    for s in specs:
        if s.name not in existing:
            actions.append(("create", s.name))
            if not dry_run:
                create_topic(bootstrap, s.name, s.partitions, s.replication_factor, s.configs)
        else:
            actions.append(("update", s.name))
            if not dry_run and s.configs:
                alter_topic_configs(bootstrap, s.name, s.configs)

    typer.echo(json.dumps({"dry_run": dry_run, "actions": actions}, indent=2))


@topics_app.command("delete")
def topics_delete(
    name: str,
    bootstrap: str = typer.Option(..., "--bootstrap"),
    confirm: bool = typer.Option(False, "--confirm"),
):
    if not confirm:
        raise typer.BadParameter("Deletion is protected. Add --confirm.")
    delete_topic(bootstrap, name)
    typer.echo(json.dumps({"status": "deleted", "topic": name}, indent=2))


@app.command("lag")
def lag(
    bootstrap: str = typer.Option(..., "--bootstrap"),
    group: str = typer.Option(..., "--group"),
    topic_prefix: Optional[str] = typer.Option(None, "--topic-prefix"),
):
    out = compute_lag(bootstrap, group, topic_prefix=topic_prefix)
    typer.echo(json.dumps(out, indent=2))


if __name__ == "__main__":
    app()
