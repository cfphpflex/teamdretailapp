#!/bin/bash

# Copyright 2019 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

printf "Enabling Cloud Build APIs..."
gcloud services enable cloudbuild.googleapis.com > /dev/null 2>&1
printf "Completed.\n"

printf "Building Monolith Container..."
cd ~/monolith-to-microservices/monolith
gcloud builds submit --tag gcr.io/${GOOGLE_CLOUD_PROJECT}/monolith:1.0.0 . > /dev/null 2>&1
printf "Completed.\n"

printf "Deploying Monolith To GKE Cluster..."
kubectl create deployment monolith --image=gcr.io/${GOOGLE_CLOUD_PROJECT}/monolith:1.0.0 > /dev/null 2>&1
kubectl expose deployment monolith --type=LoadBalancer --port 80 --target-port 8080 > /dev/null 2>&1
printf "Completed.\n\n"

printf "Please run the following command to find the IP address for the monolith service:  kubectl get service monolith\n\n"

printf "Deployment Complete\n"