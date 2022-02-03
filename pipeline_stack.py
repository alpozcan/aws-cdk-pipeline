from aws_cdk import Stack, SecretValue
from constructs import Construct
from aws_cdk.pipelines import CodePipeline, CodePipelineSource, ShellStep
from workload_stage import AwsCdkWorkloadStage

class AwsCdkPipelineStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pipeline = CodePipeline(self, "CICDPipeline",
                                pipeline_name = "CICDPipeline",
                                synth=ShellStep("Synthesize",
                                                input=CodePipelineSource.git_hub(
                                                    'alpozcan/aws-cdk-pipeline', 'main',
                                                    authentication=SecretValue.secrets_manager(secret_id='arn:aws:secretsmanager:ap-southeast-2:<REDACTED_ACCOUNT_ID>:secret:github-token-EAORWa', json_field='value')
                                                ),
                                    commands = ["npm install -g aws-cdk", 
                                                "python -m pip install -r requirements.txt", 
                                                "cdk synth"]
                                )
        )

        pipeline.add_stage(AwsCdkWorkloadStage(self, 'WorkloadStage'))
