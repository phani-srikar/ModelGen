#!/usr/bin/env python3

from aws_cdk import (
    core
)

from stacks.build_and_unittest_stack import BuildAndUnitTestStack

app = core.App()

region = app.node.try_get_context("region")
account = app.node.try_get_context("account")
if region is None or account is None:
    raise ValueError(
        "Provide region and account in 'context' parameter, as in: cdk deploy app -c region=us-west-2 -c account=123456"  # noqa: E501
    )
print(f"AWS Account={account} Region={region}")

# get github repository related information
REPO='Modelgen'
github_owner=app.node.try_get_context("github_owner")
branch=app.node.try_get_context("branch")

build_and_unittest_stack_props = {
    'github_source': {
        'owner': github_owner,
        'repo': REPO ,
        'base_branch': branch
    },
    'codebuild_project_name_prefix': 'Modelgen'
}

build_and_unittest_stack = BuildAndUnitTestStack(app,
                                                 "build-and-unittest-stack",
                                                 build_and_unittest_stack_props,
                                                 description="CI/CD build and unit test assets for amplify-codegen")

app.synth()
