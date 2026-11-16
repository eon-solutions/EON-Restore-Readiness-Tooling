# Eon Restore Readiness

Check your cloud environment before an Eon restore.

This repository brings together two ways to assess restore readiness:

- **Standalone recipes** — small, focused scripts you can copy onto a VM and run independently.
- **Full CLI** — a unified interface for running readiness checks and collecting results.

Start with a recipe for a specific question. Use the CLI for a broader assessment.

> Readiness checks validate specific prerequisites. Passing checks does not guarantee that a restore will succeed. Each check documents what it covers and what remains unverified.

## Choose your approach

| Approach | Best for |
|---|---|
| Standalone recipes | Quick troubleshooting, restricted environments, and testing one prerequisite |
| Full CLI | Running multiple checks with consistent configuration, output, and reporting |

Recipes are independently runnable. They do not require the Eon readiness CLI.

Dependencies and authentication requirements vary by check. Each recipe and CLI check documents them explicitly.

## Repository layout

```text
recipes/
  aws/
    ec2-network/
      README.md
      aws_restore_check.py
      aws_restore_check.sh
  azure/
  gcp/
cli/
docs/
```

Recipes are organized by cloud and purpose. Cloud directories do not imply that checks are available yet.

## Available checks

| Check | Interface | Status | Coverage |
|---|---|---|---|
| AWS EC2 restore network smoke test | Python or shell recipe | Initial version | HTTPS connectivity to regional S3, SQS, DynamoDB, and supplied hostnames |
| Unified readiness assessment | CLI | Planned | Check catalog and commands to be documented as implemented |

## Quick start: AWS network recipe

Run either script on a test VM in the VPC, subnet, and security groups intended for the restore.

### Python

Requires Python 3; no additional packages.

```sh
python3 recipes/aws/ec2-network/aws_restore_check.py us-east-1
```

### Shell

Requires a POSIX shell and `curl`.

```sh
sh recipes/aws/ec2-network/aws_restore_check.sh us-east-1
```

Neither version requires AWS credentials or AWS CLI.

The recipe checks DNS resolution, TCP connectivity on port 443, TLS certificate validation, and an HTTP response.

See [the recipe README](recipes/aws/ec2-network/README.md) for additional endpoints, result interpretation, limitations, and troubleshooting.

## Full CLI

The CLI provides a single entry point for readiness checks.

Installation instructions, supported checks, authentication requirements, and command examples will be added as the CLI becomes available.

Standalone recipes remain usable without installing the CLI.

## Understanding results

Read each check's scope before interpreting its result.

For example, the AWS network recipe treats an unauthenticated HTTP `403` as evidence that an endpoint is reachable. It does not establish that the restore has permission to access that service.

Network connectivity, permissions, resource configuration, and service capacity are separate prerequisites. A successful check in one area does not validate the others.

## Safety and privacy

Read the documentation before running a recipe or CLI check. It should state:

- What requests it makes
- Which dependencies and credentials it requires
- Whether it changes resources or configuration
- What information appears in its output

The initial AWS network recipe makes unauthenticated HTTPS requests and does not modify cloud resources.

Review output before sharing it. Hostnames, bucket names, resource IDs, and internal IP addresses may be sensitive. Never share credentials, access keys, session tokens, or private keys.

Do not disable certificate verification or broadly open network access to make a check pass.

## Contributing checks

Keep standalone recipes focused and easy to run.

Each check should document:

- Purpose and supported environment
- Prerequisites and dependencies
- Authentication requirements
- A copy-and-run example
- Expected output and exit codes
- Limitations and troubleshooting
- Any side effects and sensitive output

Where a recipe and CLI check cover the same prerequisite, keep their behavior and interpretation aligned.