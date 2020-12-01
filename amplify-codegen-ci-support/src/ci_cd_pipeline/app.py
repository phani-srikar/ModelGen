#!/usr/bin/env python3

from aws_cdk import (
    core
)

from stacks.common_branch_stack import CommonBranchStack
from stacks.deploy_branch_stack import DeployBranchStack

app = core.App()

region = app.node.try_get_context("region")
account = app.node.try_get_context("account")
if region is None or account is None:
    raise ValueError(
        "Provide region and account in 'context' parameter, as in: cdk deploy app -c region=us-west-2 -c account=123456"
    )
print(f"Deploying to AWS Account={account} and Region={region}")

# get github repository related information
REPO = 'Modelgen'
github_owner = app.node.try_get_context("github_owner")

stack_props = {
    'github_source': {
        'owner': github_owner,
        'repo': REPO
    },
    'codebuild_project_name_prefix': REPO
}
deploy_branches = ["master", "release"]

CommonBranchStack(app,
                  "common-branch-stack",
                  stack_props,
                  deploy_branches,
                  description="CI/CD build and unit test assets for amplify-codegen")

for deploy_branch in deploy_branches:
    DeployBranchStack(app,
                      f"{deploy_branch}-branch-stack",
                      deploy_branch,
                      stack_props,
                      description="CI/CD build, unit test and deploy assets for amplify-codegen")

app.synth()
