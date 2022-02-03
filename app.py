#!/usr/bin/env python3
import os
import aws_cdk as cdk
from pipeline_stack import AwsCdkPipelineStack
from workload_stack import AwsCdkWorkloadStack

environment = cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"])

app = cdk.App()

AwsCdkPipelineStack(app, "AwsCdkPipelineStack", env = environment)
# AwsCdkWorkloadStack(app, "AwsCdkWorkloadStack", env = environment)  # don't need to add it here since it's added into the pipeline stack via a Stage

app.synth()
