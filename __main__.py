import pulumi
import pulumi_kubernetes as k8s

# Namespace
namespace = k8s.core.v1.Namespace(
    "fintech",
    metadata={"name": "fintech"}
)

labels = {"app": "risk-service"}

# Deployment
deployment = k8s.apps.v1.Deployment(
    "risk-service",
    metadata={
        "namespace": "fintech",
        "name": "risk-service"
    },
    spec={
        "replicas": 1,
        "selector": {
            "matchLabels": labels
        },
        "template": {
            "metadata": {
                "labels": labels
            },
            "spec": {
                "containers": [{
                    "name": "risk-service",
                    "image": "risk-service:latest",
                    "imagePullPolicy": "Never",
                    "ports": [{
                        "containerPort": 8000
                    }],
                    "resources": {
                        "requests": {
                            "cpu": "100m",
                            "memory": "128Mi"
                        },
                        "limits": {
                            "cpu": "200m",
                            "memory": "256Mi"
                        }
                    }
                }]
            }
        }
    }
)

# Service
service = k8s.core.v1.Service(
    "risk-service",
    metadata={
        "namespace": "fintech",
        "name": "risk-service"
    },
    spec={
        "type": "ClusterIP",
        "selector": labels,
        "ports": [{
            "port": 80,
            "targetPort": 8000
        }]
    }
)

# HPA
hpa = k8s.autoscaling.v2.HorizontalPodAutoscaler(
    "risk-service-hpa",
    metadata={
        "namespace": "fintech",
        "name": "risk-service-hpa"
    },
    spec={
        "scaleTargetRef": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "name": "risk-service"
        },
        "minReplicas": 1,
        "maxReplicas": 5,
        "metrics": [{
            "type": "Resource",
            "resource": {
                "name": "cpu",
                "target": {
                    "type": "Utilization",
                    "averageUtilization": 50
                }
            }
        }]
    }
)

pulumi.export("namespace", namespace.metadata["name"])