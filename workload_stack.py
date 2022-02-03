from aws_cdk import  Stack  #, CfnOutput
from constructs import Construct
from aws_cdk.aws_ec2 import Vpc  #, InstanceType, AmazonLinuxImage, AmazonLinuxGeneration
# from aws_cdk.aws_autoscaling import AutoScalingGroup
# from aws_cdk.aws_elasticloadbalancingv2 import ApplicationLoadBalancer
from aws_cdk.aws_ecs import ContainerImage  #, Cluster
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions
from aws_cdk.aws_cloudwatch import Alarm  #, Statistic, Metric, ComparisonOperator

class AwsCdkWorkloadStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        vpc = Vpc(self, "VPC", max_azs=2)

        # ECS
        container_image = ContainerImage.from_asset('workload_images/typescript')  # this also works: ContainerImage.from_registry('amazon/amazon-ecs-sample')
        svc = ApplicationLoadBalancedFargateService(self, 'ALBFargateService',
            vpc=vpc, memory_limit_mib=512, cpu=256, # remove desired_count for auto-scaling
            task_image_options=ApplicationLoadBalancedTaskImageOptions(image=container_image)
        )

        # Auto Scaling
        scaling_target = svc.service.auto_scale_task_count(min_capacity=1, max_capacity=2)
        scaling_target.scale_on_cpu_utilization('CpuScaling', target_utilization_percent=90)

        # CloudWatch Metric to track CPU utilisation and an Alarm based on it
        metric_cpu  = svc.service.metric_cpu_utilization()
        alarm_cpu   = Alarm(self, "CPUAlarm", metric=metric_cpu, threshold=95, evaluation_periods=3, datapoints_to_alarm=2)

        # EC2        
        # asg = AutoScalingGroup( self, "ASG",
        #                         vpc=vpc,
        #                         instance_type=InstanceType('t3a.nano'),
        #                         machine_image=AmazonLinuxImage(generation=AmazonLinuxGeneration.AMAZON_LINUX_2),
        #                         min_capacity=1, max_capacity=2
        # )
        # alb = ApplicationLoadBalancer(  self, "ALB",
        #                                 vpc=vpc,
        #                                 internet_facing=True
        # )
        # alb_listener = alb.add_listener("Listener", port=80)
        # alb_targets = alb_listener.add_targets("ALBTargets", port=80, targets=[asg])
        # alb_listener.connections.allow_default_port_from_any_ipv4('Open to the whole world')
        # asg.scale_on_cpu_utilization("Above95Pct", target_utilization_percent=95)

        # CfnOutput(self, "LoadBalancerDNSName", export_name="LoadBalancerDNSName", value=service.load_balancer.load_balancer_dns_name)  # ApplicationLoadBalancedFargateService defines this
