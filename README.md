Solidfire Storage Backend for Cinder
-------------------------------

## Overview

This charm provides a Solidfire storage backend for use with the Cinder charm.

To use:

    juju deploy cinder
    juju deploy cinder-solidfire
    juju add-relation cinder-solidfire cinder

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
