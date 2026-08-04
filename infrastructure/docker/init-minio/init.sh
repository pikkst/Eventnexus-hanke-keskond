#!/bin/sh
mc alias set local http://minio:9000 eventnexus eventnexus
until mc ready local; do sleep 1; done
mc mb local/originals || true
mc mb local/artifacts || true
mc mb local/exports || true
mc mb local/temp || true