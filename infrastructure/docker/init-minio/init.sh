#!/bin/sh
mc alias set local http://minio:9000 "${MINIO_ROOT_USER:-eventnexus}" "${MINIO_ROOT_PASSWORD}"
until mc ready local; do sleep 1; done
mc mb local/originals || true
mc mb local/artifacts || true
mc mb local/exports || true
mc mb local/temp || true