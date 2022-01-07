Solidfire Storage Backend for Cinder
-------------------------------

## Overview

This charm provides a Solidfire storage backend for use with the Cinder charm.

To use:

    juju deploy cinder
    juju deploy cinder-solidfire
    juju add-relation cinder-solidfire cinder

## Configuration

This section covers common and/or important configuration options. See file `config.yaml` for the full list of options, along with their descriptions and default values. See the [Juju documentation][juju-docs-config-apps] for details on configuring applications.

### `volume-backend-name`

Service name to present to Cinder

### `san-ip`

IP address of SAN controller

### `san-login`

Username for SAN controller

### `san-password`

Password for SAN controller  

### `allow-template-caching`

Create an internal cache of copy of images when a bootable volume is created to eliminate fetch from glance and qemu-conversion on subsequent calls.

### `allow-tenant-qos`

Allow tenants to specify QOS on create

### `api-port`

SolidFire API port. Useful if the device api is behind a proxy on a different port.

### `emulate-512`

Set 512 byte emulation on volume creation

### `enable-vag`

Utilize volume access groups on a per-tenant basis.

### `enable-volume-mapping`

Create an internal mapping of volume IDs and account. Optimizes lookups and performance at the expense of memory, very large deployments may want to consider setting to False.

### `svip`

Overrides default cluster SVIP with the one specified. This is required or deployments that have implemented the use of VLANs for iSCSI networks in their cloud.

### `template-account-name`

Account name on the SolidFire Cluster to use as owner of template/cache volumes (created if does not exist).

### `volume-prefix`

Create SolidFire volumes with this prefix. Volume names are of the form <sf_volume_prefix><cinder-volume-id>. The default is to use a prefix of ‘UUID-‘.

## Deployment

This charm's primary use is as a backend for the cinder charm. To do so, add a relation betweeen both charms:

    juju add-relation cinder-solidfire:storage-backend cinder:storage-backend

# Documentation

The OpenStack Charms project maintains two documentation guides:

* [OpenStack Charm Guide][cg]: for project information, including development
  and support notes
* [OpenStack Charms Deployment Guide][cdg]: for charm usage information

[cg]: https://docs.openstack.org/charm-guide
[cdg]: https://docs.openstack.org/project-deploy-guide/charm-deployment-guide
