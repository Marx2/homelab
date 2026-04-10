Scale-to-Zero with KEDA HTTP Add-on
=====================================

This directory contains the KEDA HTTP Add-on, which enables scale-to-zero for HTTP workloads.
When a deployment has 0 replicas, the interceptor proxy holds incoming requests and triggers
KEDA to scale the deployment up before forwarding them.

Architecture
------------

  Internet → nginx ingress → interceptor proxy (networking namespace)
               ↓ if replicas==0: hold request, trigger scale-up
               ↓ if replicas>=1: forward to target service

Prerequisites
-------------

- keda Flux Kustomization must be deployed (this one depends on it)
- The target service must be reachable from the interceptor in the networking namespace

Files in this directory
-----------------------

  ks.yaml                - Flux Kustomization that deploys the HTTP add-on to the networking namespace
  app/helmrelease.yaml   - HelmRelease for keda-add-ons-http; interceptor stays at 1 replica always;
                           operator watches both `networking` and `default` namespaces
  app/kustomization.yaml - Kustomize entrypoint for the app/ folder


How to add scale-to-zero to a service
======================================

Assume you have an app called `myapp` in the `default` namespace, served on port 8080,
accessible at myapp.<SECRET_DOMAIN>.

1. Create: cluster/apps/default/myapp/app/interceptor-service.yaml
   ---------------------------------------------------------------
   An ExternalName Service that bridges the default namespace to the interceptor
   living in the networking namespace (ingress backends must be same-namespace):

     apiVersion: v1
     kind: Service
     metadata:
       name: keda-http-interceptor-proxy
       namespace: default
     spec:
       type: ExternalName
       externalName: keda-add-ons-http-interceptor-proxy.networking.svc.cluster.local
       ports:
         - port: 8080
           targetPort: 8080
           protocol: TCP

   NOTE: This file is identical for every app in the default namespace. If two apps
   share the same namespace, only one copy of this Service is needed — you can reference
   the same Service from multiple HTTPScaledObjects.

2. Create: cluster/apps/default/myapp/app/httpscaledobject.yaml
   ------------------------------------------------------------
   Tells KEDA which deployment to scale and which host/port to watch:

     apiVersion: http.keda.sh/v1alpha1
     kind: HTTPScaledObject
     metadata:
       name: myapp
       namespace: default
     spec:
       hosts:
         - myapp.${SECRET_DOMAIN}
       pathPrefixes:
         - /
       scaleTargetRef:
         name: myapp
         kind: Deployment
         apiVersion: apps/v1
         service: myapp        # the real app Service (not the interceptor)
         port: 8080            # the port the app Service exposes
       replicas:
         min: 0
         max: 1
       scaledownPeriod: 300    # seconds of no traffic before scaling back to 0

3. Edit: cluster/apps/default/myapp/app/kustomization.yaml
   --------------------------------------------------------
   Add the two new files to the resources list:

     resources:
       - ./helmrelease.yaml
       - ./interceptor-service.yaml
       - ./httpscaledobject.yaml

4. Edit: cluster/apps/default/myapp/app/helmrelease.yaml — three changes
   ----------------------------------------------------------------------

   a) Set initial replicas to 0 so Flux doesn't fight KEDA on first deploy:

        controllers:
          myapp:
            replicas: 0    # <-- add this line
            containers:
              ...

   b) Point the ingress at the interceptor proxy instead of the real app Service.
      Change the ingress path service reference from identifier-based to name-based:

        # Before:
        service:
          identifier: app
          port: http

        # After:
        service:
          name: keda-http-interceptor-proxy
          port: 8080

   c) Add a driftDetection ignore rule for /spec/replicas so Flux does not reset
      the replica count that KEDA is managing:

        driftDetection:
          mode: enabled
          ignore:
            - paths:
                - /spec/containers/resources/limits
              target:
                kind: Pod
            - paths:
                - /spec/replicas        # <-- add this block
              target:
                kind: Deployment

5. Edit: cluster/apps/default/myapp/ks.yaml
   -----------------------------------------
   Add a dependsOn so the HTTPScaledObject CRD exists before this Kustomization runs:

     dependsOn:
       - name: keda-http

Flux dependency chain
---------------------

  keda (networking) → keda-http (networking) → myapp (default)

Verification
------------

  flux get ks                                    # all Kustomizations reconciled
  kubectl get pods -n networking | grep keda     # interceptor and operator running
  kubectl get deploy -n default myapp            # should show 0/0 replicas when idle
  # visit myapp.<domain> — brief cold-start delay, then app loads
  # wait 5+ minutes idle → replicas drop back to 0
