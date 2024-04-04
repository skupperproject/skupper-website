---
title: #Securing a service network
---
## Securing a service network

Skupper provides default, built-in security that scales across clusters and clouds.
This section describes additional security you can configure.

See [Securing a service network using policies](../policy/index.html) for information about creating granular policies for each cluster.

### Restricting access to services using a Kubernetes network policy

By default, if you expose a service on the service network, that service is also accessible from other namespaces in the cluster.
You can avoid this situation when creating a site using the `--create-network-policy` option.

1. Create the service network router with a Kubernetes network policy:

   ```bash
   $ skupper init --create-network-policy
   ```
2. Check the site status:

   ```bash
   $ skupper status
   ```
   The output should be similar to the following:
   ```
   Skupper enabled for namespace 'west'. It is not connected to any other sites.
   ```

You can now expose services on the service network and those services are not accessible from other namespaces in the cluster.

### Applying TLS to TCP or HTTP2 traffic on the service network

By default, the traffic between sites is encrypted, however the traffic between the service pod and the router pod is not encrypted.
For services exposed as TCP or HTTP2, the traffic between the pod and the router pod can be encrypted using TLS.

* Two or more linked sites
* A TCP or HTTP2 frontend and backend service

1. Deploy your backend service.
2. Expose your backend deployment on the service network, enabling TLS.

   For example, if you want to expose a TCP service:

   ```bash
   $ skupper expose deployment <deployment-name> --port 443 --enable-tls
   ```

   Enabling TLS creates the necessary certificates required for TLS backends and stores them in a secret named `skupper-tls-<deployment-name>`.
3. Modify the backend deployment to include the generated certificates, for example:

   ```yaml
   ...
       spec:
         containers:
         ...
           command:
           ...
           - "/certs/tls.key"
           - "/certs/tls.crt"
           ...
           volumeMounts:
           ...
           - mountPath: /certs
             name: certs
             readOnly: true
         volumes:
         - name: index-html
           configMap:
             name: index-html
         - name: certs
           secret:
             secretName: skupper-tls-<deployment-name>
   ```

   Each site creates the necessary certificates required for TLS clients and stores them in a secret named `skupper-service-client`.
4. Modify the frontend deployment to include the generated certificates, for example:

   ```yaml
   spec:
     template:
       spec:
         containers:
         ...
           volumeMounts:
           - name: certs
             mountPath: /tmp/certs/skupper-service-client
         ...
         volumes:
         - name: certs
           secret:
             secretName: skupper-service-client

   ```
5. Test calling the service from a TLS enabled frontend.
