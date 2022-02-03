from aws_cdk import Stage
from constructs import Construct
from workload_stack import AwsCdkWorkloadStack

class AwsCdkWorkloadStage(Stage):
    def __init__(self, scope: Construct, contruct_id: str, **kwargs) -> None:
        super().__init__(scope, contruct_id, **kwargs)

        workload_stack = AwsCdkWorkloadStack(self, "WorkloadStack")
