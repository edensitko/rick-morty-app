#!/bin/sh
# Healthcheck script for Kubernetes liveness/readiness
curl -f http://localhost/healthcheck || exit 1
