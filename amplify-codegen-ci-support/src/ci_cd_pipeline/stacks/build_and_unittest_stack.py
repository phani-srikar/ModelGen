from aws_cdk import core

from pull_request_code_builder import PullRequestCodeBuilder
from aws_cdk.aws_secretsmanager import Secret
import boto3
from aws_cdk.aws_codebuild import GitHubSourceCredentials


class BuildAndUnitTestStack(core.Stack):

    def __init__(self, scope: core.App, id: str, props, **kwargs):
        super().__init__(scope, id, **kwargs)
        required_props = ['github_source']
        for prop in required_props:
            if prop not in props:
                raise RuntimeError(f"Parameter {prop} is required.")

        codebuild_project_name_prefix = props['codebuild_project_name_prefix']

        github_source = props['github_source']
        owner = github_source['owner']
        repo = github_source['repo']
        base_branch = github_source['base_branch']

        # self.update_github_source_credential()
        pr = PullRequestCodeBuilder(self,
                               f"build-and-unittest-{base_branch}",
                               project_name=f"{codebuild_project_name_prefix}-{base_branch}-build-and-unittest",
                               github_owner=owner,
                               github_repo=repo,
                               base_branch=base_branch,
                               buildspec_path=f"codebuild_specs/{base_branch}-pr-builder-buildspec.yml")

        # core.Dependency(source=pr, target=github_source_credentials)


    # def update_github_source_credential(self):
    #     codebuild_client = boto3.client("codebuild")
    #     current_credentials = codebuild_client.list_source_credentials()
    #     print(current_credentials)
    #     print(type(current_credentials))
    #
    #     current_github_access_tokens = list(
    #         filter(lambda s: (s["serverType"] == "GITHUB"), current_credentials["sourceCredentialsInfos"]))
    #
    #     if len(current_github_access_tokens) > 0:
    #         print(f"deleting credentials:{current_github_access_tokens[0]['arn']}")
    #         codebuild_client.delete_source_credentials(arn=current_github_access_tokens[0]["arn"])
    #
    #     current_credentials = codebuild_client.list_source_credentials()
    #     print(current_credentials)
    #
    #     github_ops_access_token_secret = Secret.from_secret_name_v2(self,
    #                                                                 "github-ops-access-token",
    #                                                                 secret_name="github_ops_access_token")
    #
    #     ssm_client = boto3.client("secretsmanager")
    #     github_ops_access_token_secret_value = ssm_client.get_secret_value(SecretId=github_ops_access_token_secret.secret_name)["SecretString"]
    #
    #     response = codebuild_client.import_source_credentials(
    #         username='phani-srikar',
    #         token=github_ops_access_token_secret_value,
    #         serverType='GITHUB',
    #         authType='PERSONAL_ACCESS_TOKEN',
    #         shouldOverwrite=True
    #     )
    #     print(response)
    #
    #     current_credentials = codebuild_client.list_source_credentials()
    #     print(current_credentials)
    #
    #     # github_source_credentials = GitHubSourceCredentials(self,
    #     #                                                     f"{id}-access-token",
    #     #                                                     access_token=github_ops_access_token_secret.secret_value)
    #     # current_credentials = codebuild_client.list_source_credentials()
    #     # print(current_credentials)
    #     # return github_source_credentials