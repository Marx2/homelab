# Agent Configuration

This file contains configuration and instructions for AI agents working in this project.

## Project Context

It's a directory containing kubernetes configuration managed with gitops approach using FluxCD,
updated with Renovate bot.

## Documentation (context7 MCP)

Use the context7 MCP server to fetch up-to-date documentation for the following libraries used in this project:

- **FluxCD**: `/websites/fluxcd_io_flux` (3233 snippets) — GitOps, HelmRelease, Kustomization, reconciliation
- **bjw-s App Template helm chart**: `/websites/bjw-s-labs_github_io_helm-charts` (110 snippets) — universal Helm chart used by most deployments
- **Renovate**: `/websites/renovatebot` (3308 snippets) — automated dependency update configuration

Always prefer context7 docs over web search or training data for these libraries.

## Agent Behaviors

### Code Style

- subfolders contains namespaces configurations
- subfolders in namespace contains definition of deployment of specific service
- most deployments uses universal App Template helm chart, which documentation is available
  at: https://bjw-s-labs.github.io/helm-charts/docs/app-template/
