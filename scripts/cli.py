#!/usr/bin/env python3
import subprocess
import json
import os
import time
from datetime import datetime

import boto3
from botocore.config import Config
import click


@click.group()
@click.option("--profile", default="single-cell-dev", help="AWS profile to use")
@click.pass_context
def cli(ctx, profile):
    ctx.ensure_object(dict)
    ctx.obj["aws_profile"] = profile
    os.environ["AWS_PROFILE"] = profile  # Lame hack. Need to make this smarter.
    aws_conf = Config(
        region_name="us-west-2", retries={"max_attempts": 2, "mode": "standard"}
    )
    client = boto3.client("cloudformation", config=aws_conf)
    ctx.obj["client"] = client


def get_secrets(ctx):
    output = run_aws_cmd(ctx, ["secretsmanager", "get-secret-value", "--secret-id", "happy/dp-rdev-config"])
    secrets = json.loads(output["SecretString"])
    return secrets


def run_aws_cmd(ctx, cmd, json_output=True):
    command = ["aws", "--profile", ctx.obj["aws_profile"]]
    command.extend(cmd)
    output = subprocess.check_output(command)
    if not json_output:
        return output
    return json.loads(output)


def get_stack(ctx, label):
    status_cmd = [
        "aws",
        "cloudformation",
        "describe-stacks",
        "--profile",
        ctx.obj["aws_profile"],
        "--stack-name",
        label,
    ]
    stack = json.loads(subprocess.check_output(status_cmd))["Stacks"][0]
    return stack


def get_outputs(ctx, label=None, stack=None):
    if not stack:
        stack = get_stack(ctx, label)
    outputs = {}
    for op in stack["Outputs"]:
        outputs[op["OutputKey"]] = op["OutputValue"]
    return outputs


def print_outputs(ctx, label=None, stack=None):
    outputs = get_outputs(ctx, label, stack)
    if not outputs:
        return
    print()
    print("Module Outputs --")
    for k, v in outputs.items():
        print(f"{k}: {v}")


def get_migration_taskdef(ctx, label):
    """Find the migration task definition in our CF stack"""
    path = ["DevEnv", "DevEnv", "MigrateDB", "TaskDefinition"]
    arn = label
    path_length = len(path)
    for i in range(path_length):
        cmd = [
            "aws",
            "cloudformation",
            "describe-stack-resources",
            "--profile",
            ctx.obj["aws_profile"],
            "--stack-name",
            arn,
        ]
        resources = json.loads(subprocess.check_output(cmd))["StackResources"]
        # Convert to a map of CloudFormation object name => AWS resource ARN
        resource_map = {
            item["LogicalResourceId"]: item["PhysicalResourceId"] for item in resources
        }
        arn = resource_map[path[i]]
    return arn

@cli.command()
@click.argument("label")
@click.pass_context
def migrate(ctx, label):
    """Run DB migration task in dev account"""
    secrets = get_secrets(ctx)
    cluster_arn = secrets["cluster_arn"]
    subnets = secrets["subnets"]
    security_groups = secrets["security_groups"]
    return _migrate(ctx, label, cluster_arn, subnets, security_groups)


def _migrate(ctx, label, cluster_arn, subnets, security_groups):
    """Run DB migration task"""
    taskdef_arn = get_migration_taskdef(ctx, label)
    print(f"Using task definition {taskdef_arn}")
    command = [
        "aws",
        "ecs",
        "run-task",
        "--profile",
        ctx.obj["aws_profile"],
        "--cluster",
        cluster_arn,
        "--task-definition",
        taskdef_arn,
        "--network-configuration",
        f"awsvpcConfiguration={{subnets=[{subnets}],securityGroups=[{security_groups}],assignPublicIp='DISABLED'}}",
    ]
    task_info = json.loads(subprocess.check_output(command))["tasks"][0]
    print(f"Task {task_info['taskArn']} started")
    # Wait for the task to exit.
    status_cmd = [
        "aws",
        "ecs",
        "describe-tasks",
        "--tasks",
        task_info["taskArn"],
        "--profile",
        ctx.obj["aws_profile"],
        "--cluster",
        cluster_arn,
    ]
    log_stream = ""
    while True:
        taskinfo = json.loads(subprocess.check_output(status_cmd))["tasks"][0]
        try:
            status = taskinfo["containers"][0]["lastStatus"]
            reason = ""
            if reason in taskinfo["containers"][0]:
                reason = taskinfo["containers"][0]["reason"]
                print(f"{status}: {reason}")
            log_stream = taskinfo["containers"][0]["runtimeId"]
            if status == "STOPPED":
                break
        except:
            print("Container hasn't started yet")
    # Get logs
    print("getting taskdef info")
    taskdef_cmd = [
        "aws",
        "ecs",
        "describe-task-definition",
        "--profile",
        ctx.obj["aws_profile"],
        "--task-definition",
        taskdef_arn,
    ]
    taskdef = json.loads(subprocess.check_output(taskdef_cmd))["taskDefinition"]
    log_group = taskdef["containerDefinitions"][0]["logConfiguration"]["options"][
        "awslogs-group"
    ]
    print("Log Events:")
    log_cmd = [
        "aws",
        "logs",
        "get-log-events",
        "--log-group-name",
        log_group,
        "--log-stream-name",
        log_stream,
        "--profile",
        ctx.obj["aws_profile"],
    ]
    logs = json.loads(subprocess.check_output(log_cmd))["events"]
    for log in logs:
        print(log)
    print("done!")


def invoke_wait(ctx, label):
    last_status = ""
    while True:
        stack = get_stack(ctx, label)
        status = stack["StackStatus"]
        if status != last_status:
            print(f"{datetime.now().strftime('%H:%M:%S')} - {status}")
            last_status = status
        if status.endswith("IN_PROGRESS"):
            time.sleep(2)
        else:
            # We're done.
            print_outputs(ctx, stack=stack)
            return stack


@cli.command()
@click.argument("label")
@click.argument("tag")
@click.option(
    "--wait/--no-wait", is_flag=True, default=True, help="wait for this to complete"
)
@click.pass_context
def create(ctx, label, tag, wait):
    """Create a dev stack with a given tag"""
    print(f"creating {label}")
    command = [
        "aws",
        "cloudformation",
        "create-stack",
        "--template-body",
        "file://scripts/remotedev.yml",
        "--profile",
        ctx.obj["aws_profile"],
        "--on-failure",
        "DO_NOTHING",
        "--stack-name",
        label,
        "--parameters",
        f"ParameterKey=ImageTag,ParameterValue={tag}",
    ]
    subprocess.check_call(command)
    if wait:
        stack = invoke_wait(ctx, label)


@cli.command()
@click.argument("label")
@click.argument("tag")
@click.option(
    "--wait/--no-wait", is_flag=True, default=True, help="wait for this to complete"
)
@click.pass_context
def update(ctx, label, tag, wait):
    """Update a dev stack tag version"""
    print(f"updating {label}")
    command = [
        "aws",
        "cloudformation",
        "update-stack",
        "--template-body",
        "file://scripts/remotedev.yml",
        "--profile",
        ctx.obj["aws_profile"],
        "--stack-name",
        label,
        "--parameters",
        f"ParameterKey=ImageTag,ParameterValue={tag}",
    ]
    subprocess.check_call(command)
    if wait:
        invoke_wait(ctx, label)


@cli.command()
@click.argument("label")
@click.option(
    "--wait/--no-wait", is_flag=True, default=True, help="wait for this to complete"
)
@click.pass_context
def cancelupdate(ctx, label, wait):
    """Cancel a dev stack update"""
    print(f"Canceling update of {label}")
    command = [
        "aws",
        "cloudformation",
        "cancel-update-stack",
        "--profile",
        ctx.obj["aws_profile"],
        "--stack-name",
        label,
    ]
    subprocess.check_call(command)
    if wait:
        invoke_wait(ctx, label)


@cli.command()
@click.argument("label")
@click.pass_context
def delete(ctx, label):
    """Delete a dev stack"""
    print(f"deleting {label}")
    command = [
        "aws",
        "cloudformation",
        "delete-stack",
        "--profile",
        ctx.obj["aws_profile"],
        "--stack-name",
        label,
    ]
    subprocess.check_call(command)


@cli.command()
@click.pass_context
def list(ctx):
    """List dev stacks"""
    print(f"Listing stacks")
    stacks = ctx.obj["client"].describe_stacks()
    for stack in stacks["Stacks"]:
        if stack.get("ParentId"):
            # For now, skip sub-stacks
            continue
        print(f"Stack: {stack['StackName']} / Status: {stack['StackStatus']}")


@cli.command()
@click.argument("tag")
@click.pass_context
def push(ctx, tag):
    """Wait until a dev stack is updated"""
    print("Building images...")
    subprocess.check_call(["docker-compose", "build"])
    secrets = get_secrets(ctx)
    frontend_ecr = secrets["frontend_ecr"]
    backend_ecr = secrets["backend_ecr"]
    print("logging in to ECR...")
    pwd = run_aws_cmd(ctx, ["ecr", "get-login-password", "--region", "us-west-2"], json_output=False)
    login_ecr = frontend_ecr.split("/")[0]
    cmd = subprocess.run(["docker", "login", "--username", "AWS", "--password-stdin", login_ecr], input=pwd)
    print("Tagging images...")
    subprocess.check_call(["docker", "tag", "corpora-frontend:latest", f"{frontend_ecr}:{tag}"])
    subprocess.check_call(["docker", "tag", "corpora-backend:latest", f"{backend_ecr}:{tag}"])
    print("Pushing images...")
    subprocess.check_call(["docker", "push", f"{frontend_ecr}:{tag}"])
    subprocess.check_call(["docker", "push", f"{backend_ecr}:{tag}"])


@cli.command()
@click.argument("label")
@click.pass_context
def watch(ctx, label):
    """Wait until a dev stack is updated"""
    invoke_wait(ctx, label)


@cli.command()
@click.argument("label")
@click.pass_context
def status(ctx, label):
    """Get detailed status info for a dev stack"""
    print(f"checking status for {label}")
    command = [
        "aws",
        "cloudformation",
        "describe-stacks",
        "--profile",
        ctx.obj["aws_profile"],
    ]
    output = subprocess.check_output(command)
    data = json.loads(output)
    outputs = {}
    for stack in data["Stacks"]:
        stack_path = stack.get("RootId") or stack.get("StackId")
        reason = stack.get("StackStatusReason")
        # Skip any stacks that aren't part of this one.
        if f"/{label}/" not in stack_path:
            continue
        print(
            f"Stack: {stack['StackName']} / Status: {stack['StackStatus']} / Reason: {reason}"
        )
        if reason:
            get_events = [
                "aws",
                "cloudformation",
                "describe-stack-events",
                "--profile",
                ctx.obj["aws_profile"],
                "--stack-name",
                stack["StackName"],
            ]
            events = subprocess.check_output(get_events)
            eventdata = json.loads(events)["StackEvents"]
            # Print most recent 3 events
            show_events = 3
            for event in eventdata:
                combo = [
                    event.get("ResourceType", ""),
                    event.get("LogicalResourceId", ""),
                    event.get("ResourceStatus", ""),
                    event.get("ResourceStatusReason", ""),
                ]
                print(" / ".join(combo))
                show_events -= 1
                if show_events <= 0:
                    break
        # Capture outputs from this stack to display to our users.
        if stack["StackName"] == label:
            outputs = get_outputs(ctx, stack=stack)
    print(outputs)


if __name__ == "__main__":
    cli()
