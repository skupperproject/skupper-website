---
title: Using Skupper tokens
---
# Using Skupper tokens

Skupper tokens allow you to create links between sites.
You create a token on one site and use that token from the other site to create a link between the two sites.

**📌 NOTE**\
Although the linking process is directional, a Skupper link allows communication in both directions.

If both sites are equally accessible, for example, two public clouds, then it is not important where you create the token.
However, when using a token, the site you link to must be accessible from the site you link from.
For example, if you are creating a service network using both a public and private cluster, you must create the token on the public cluster and use the token from the private cluster.

There are two types of Skupper token:

* **Claim token (default)**

  A claim token can be restricted by:

  * time - prevents token reuse after a specified period.
  * usage - prevents creating multiple links from a single token.

  All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).
  A claim token is not a certificate, but is securely exchanged for a certificate during the linking process.
  By implementing appropriate restrictions (for example, creating a single-use claim token), you can avoid the accidental exposure of certificates.
* **Cert token**

  You can use a cert token to create a link to the site which issued that token, it includes a valid certificate from that site.

  All inter-site traffic is protected by mutual TLS using a private, dedicated certificate authority (CA).
  A cert token is a certificate issued by the dedicated CA.
  Protect it appropriately.

## Creating claim tokens

You can use a claim token to create a link to the site which issued that token.
It does not includes a certificate from that site, but a certificate is passed from the site when the claim token is used.
A claim token can be restricted by time or usage.

1. Log into the cluster.
2. Change to the namespace associated with the site.
3. Create a claim token, for example:

   ```bash
   $ skupper token create $HOME/secret.yaml --expiry 30m0s --uses 2 -t claim
   ```

   **📌 NOTE**\
   Claim tokens are the default, the `-t claim` section of the command is unnecessary.

   * **--expiry**\
   The amount of time the token is valid in minutes and seconds, default `15m0s`.
   * **--uses**\
   The number of times you can use the token to create a  link, default `1`.

* See the [Using the Skupper CLI](../cli/index.html) for information about using the token to create links.

## Creating cert tokens

A cert token allows you create many links to the service network from different sites without restrictions.

1. Log into the cluster.
2. Change to the namespace associated with the site.
3. Create a cert token:

   ```bash
   $ skupper token create $HOME/secret.yaml -t cert
   ```

   **📌 NOTE**\
   Cert tokens are always valid and can be reused indefinitely unless revoked as described in [Revoking access to a site](#revoking-access-to-a-site)

* See the [Using the Skupper CLI](../cli/index.html) for information about using the token to create links.

## Revoking access to a site

If a token is compromised, you can prevent unauthorized use of that token by invalidating  all the tokens created from a site.

This option removes all links to the site and requires that you recreate any links to restore the service network.

1. Procedure
2. Log into the cluster.
3. Change to the namespace associated with the site.
4. Check the status of the site:

   ```bash
   $ skupper status
   Skupper is enabled for namespace "west" in interior mode. It is linked to 2 other sites.
   ```
5. Check outgoing links from the site:

   ```bash
   $ skupper link status
   Link link1 is connected
   ```

   In this case, there are two links, and one outgoing link, meaning there is one incoming link.
6. Revoke access to the site from incoming links:

   ```bash
   $ skupper revoke-access
   ```
7. Check the status of the site to see the revocation of access:

   ```bash
   $ skupper status
   Skupper is enabled for namespace "west" in interior mode. It is linked to 1 other site.
   $ skupper link status
   Link link1 is connected
   ```

   The output shows that the `skupper revoke-access` command has revoked the incoming links, but outgoing links are still connected.

   You can remove that link using the `skupper link delete link1` command.
   To revoke access, you must follow this procedure while logged into the appropriate cluster.

   <dl><dt><strong>📌 NOTE</strong></dt><dd>

   After performing the `skupper revoke-access` command, the remote site still retains the link information and returns a `Already connected to <site>` message if you try to recreate the link.
   To recreate the link, you must first delete the link manually from the remote site context.
   </dd></dl>
