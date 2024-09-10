# Customer Service Setup Guide

This guide provides instructions for enabling the customer service webservice.

## Prerequisites

### 1. Kubernetes Cluster

For local testing, install Minikube:

#### macOS
```bash
brew install minikube
```

#### Linux
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

### 2. kubectl

Install the Kubernetes command-line tool:

#### macOS
```bash
brew install kubectl
```

#### Linux
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```

### 3. Helm

Install Helm, the Kubernetes package manager:

#### macOS
```bash
brew install helm
```

#### Linux
```bash
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash
```

## Installation and Usage Instructions

1. Start your Kubernetes cluster:
   * If using Minikube:
     ```bash
     minikube start
     ```

2. Verify the installation:
   ```bash
   kubectl version --short
   helm version --short
   ```
3. A docker image related to the app, arunbhargav/customer-service:latest has been published 
   to the public docker registry. Use your docker cred to authenticate to registry.
```bash
docker login
```

4.You're now ready to deploy applications to your local Kubernetes cluster!

## Next Steps

1. Git clone the repository
   ```bash
   git clone https://github.com/arunpotharaju-workspace/customer-service.git
    ```
2. Create the customer-service namespace
    ```bash
   kubectl create namespace customer-service 
   ```
3. Change directory into customer-service folder
   ```bash
   cd customer-service
   ```
4. Install the relevant customer-service helm chart
```bash
  helm install customer-service helm/ --namespace customer-service      
 ```

5. Ensure the relevant pods are created
   ```bash
   kubectl get pods -n customer-service                                     
   NAME                                                        READY   STATUS    RESTARTS   AGE
   customer-service-66876fcc75-skwfx                           1/1     Running   0          65m
   ```
6. Check for any events related to the pods, services
```bash 
kubectl get events -n customer-service           
LAST SEEN   TYPE     REASON              OBJECT                                   MESSAGE
98s         Normal   Scheduled           pod/customer-service-66876fcc75-7k8nb    Successfully assigned default/customer-service-66876fcc75-7k8nb to minikube
98s         Normal   Pulling             pod/customer-service-66876fcc75-7k8nb    Pulling image "arunbhargav/customer-service:latest"
97s         Normal   Pulled              pod/customer-service-66876fcc75-7k8nb    Successfully pulled image "arunbhargav/customer-service:latest" in 502ms (502ms including waiting). Image size: 212863627 bytes.
97s         Normal   Created             pod/customer-service-66876fcc75-7k8nb    Created container customer-service
97s         Normal   Started             pod/customer-service-66876fcc75-7k8nb    Started container customer-service
98s         Normal   SuccessfulCreate    replicaset/customer-service-66876fcc75   Created pod: customer-service-66876fcc75-7k8nb
98s         Normal   ScalingReplicaSet   deployment/customer-service              Scaled up replica set customer-service-66876fcc75 to 1
```
7. Ensure the service is available 
```bash 
kubectl get svc -n customer-service
NAME               TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
customer-service   ClusterIP   10.100.42.12   <none>        80/TCP    2m29s
```
8. Port forward from your local machine to the port on which the app is listening
```bash
kubectl port-forward service/customer-service 8080:80 -n customer-service &
Forwarding from 127.0.0.1:8080 -> 8000
```
9. Access the application endpoints for testing using the following URL
```bash
   http://127.0.0.1:8080/docs
```
10. Use "test/test" for authentication