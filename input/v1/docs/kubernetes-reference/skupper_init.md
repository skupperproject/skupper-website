---
title: skupper init
---
### skupper init

Initialise skupper installation

#### Synopsis

Setup a router and other supporting objects to provide a functional skupper
installation that can then be connected to other skupper installations

```
skupper init [flags]
```

#### Options

```
      --site-name string                           Provide a specific name for this skupper installation
      --ingress string                             Setup Skupper ingress to one of: [route|loadbalancer|nodeport|nginx-ingress-v1|contour-http-proxy|ingress|none]. If not specified route is used when available, otherwise loadbalancer is used.
      --router-mode string                         Skupper router-mode (default "interior")
      --labels strings                             Labels to add to resources created by skupper
      --router-logging string                      Logging settings for router. 'trace', 'debug', 'info' (default), 'notice', 'warning', and 'error' are valid values.
      --enable-console                             Enable skupper console must be used in conjunction with '--enable-flow-collector' flag
      --ingress-host string                        Hostname or alias by which the ingress route or proxy can be reached
      --create-network-policy                      Create network policy to restrict access to skupper services exposed through this site to current pods in namespace
      --console-auth string                        Authentication mode for console(s). One of: 'openshift', 'internal', 'unsecured' (default "internal")
      --console-user string                        Skupper console user. Valid only when --console-auth=internal
      --console-password string                    Skupper console password. Valid only when --console-auth=internal
      --console-ingress string                     Determines if/how console is exposed outside cluster. If not specified uses value of --ingress. One of: [route|loadbalancer|nodeport|nginx-ingress-v1|contour-http-proxy|ingress|none].
      --enable-rest-api                            Enable REST API
      --ingress-annotations strings                Annotations to add to skupper ingress
      --annotations strings                        Annotations to add to skupper pods
      --router-service-annotations strings         Annotations to add to skupper router service
      --router-pod-annotations strings             Annotations to add to skupper router pod
      --controller-service-annotation strings      Annotations to add to skupper controller service
      --controller-pod-annotation strings          Annotations to add to skupper controller pod
      --prometheus-server-pod-annotation strings   Annotations to add to skupper prometheus pod
      --enable-service-sync                        Participate in cross-site service synchronization (default true)
      --service-sync-site-ttl duration             Time after which stale services, i.e. those whose site has not been heard from, created through service-sync are removed.
      --enable-flow-collector                      Enable cross-site flow collection for the application network
      --routers int                                Number of router replicas to start
      --router-cpu string                          CPU request for router pods
      --router-memory string                       Memory request for router pods
      --router-cpu-limit string                    CPU limit for router pods
      --router-memory-limit string                 Memory limit for router pods
      --router-node-selector string                Node selector to control placement of router pods
      --router-pod-affinity string                 Pod affinity label matches to control placement of router pods
      --router-pod-antiaffinity string             Pod antiaffinity label matches to control placement of router pods
      --router-ingress-host string                 Host through which node is accessible when using nodeport as ingress.
      --router-load-balancer-ip string             Load balancer ip that will be used for router service, if supported by cloud provider
      --router-data-connection-count string        Configures the number of data connections the router will use when linking to other routers
      --controller-cpu string                      CPU request for controller pods
      --controller-memory string                   Memory request for controller pods
      --controller-cpu-limit string                CPU limit for controller pods
      --controller-memory-limit string             Memory limit for controller pods
      --controller-node-selector string            Node selector to control placement of controller pods
      --controller-pod-affinity string             Pod affinity label matches to control placement of controller pods
      --controller-pod-antiaffinity string         Pod antiaffinity label matches to control placement of controller pods
      --controller-ingress-host string             Host through which node is accessible when using nodeport as ingress.
      --controller-load-balancer-ip string         Load balancer ip that will be used for controller service, if supported by cloud provider
      --config-sync-cpu string                     CPU request for config-sync pods
      --config-sync-memory string                  Memory request for config-sync pods
      --config-sync-cpu-limit string               CPU limit for config-sync pods
      --config-sync-memory-limit string            Memory limit for config-sync pods
      --enable-cluster-permissions                 Enable cluster wide permissions in order to expose deployments/statefulsets in other namespaces
      --flow-collector-record-ttl duration         Time after which terminated flow records are deleted, i.e. those flow records that have an end time set. Default is 15 minutes.
      --flow-collector-cpu string                  CPU request for flow collector pods
      --flow-collector-memory string               Memory request for flow collector pods
      --flow-collector-cpu-limit string            CPU limit for flow collector pods
      --flow-collector-memory-limit string         Memory limit for flow collector pods
      --prometheus-cpu string                      CPU request for prometheus pods
      --prometheus-memory string                   Memory request for prometheus pods
      --prometheus-cpu-limit string                CPU limit for prometheus pods
      --prometheus-memory-limit string             Memory limit for prometheus pods
      --timeout duration                           Configurable timeout for the ingress loadbalancer option. (default 2m0s)
      --enable-skupper-events                      Enable sending Skupper events to Kubernetes (default true)
  -h, --help                                       help for init
```

#### Options inherited from parent commands

```
  -c, --context string      The kubeconfig context to use
      --kubeconfig string   Path to the kubeconfig file to use
  -n, --namespace string    The Kubernetes namespace to use
      --platform string     The platform type to use [kubernetes, podman]
```

#### SEE ALSO

* [skupper](index.html) 

<!-- ###### Auto generated by spf13/cobra on 29-May-2024
 -->