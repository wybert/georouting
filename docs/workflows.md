# GitHub Workflows

## build-and-unit.yml
- **Triggers:** `push` and `pull_request` on `main`.
- **Purpose:** Install dependencies and run fast, deterministic tests without hitting external routing APIs (`pytest -m "not integration"`). Sets `RUN_REMOTE_ROUTER_TESTS=false` so remote calls are skipped.
- **Secrets:** None. Safe for forks and regular PRs.
- **Notes:** If you add new tests that call real services, mark them with `@pytest.mark.integration` so they stay out of this workflow.

## integration-remote.yml
- **Triggers:** `workflow_dispatch` (manual from GitHub Actions UI).
- **Purpose:** Run live integration tests that call external routing providers. Sets `RUN_REMOTE_ROUTER_TESTS=true` and executes `pytest -m "integration"`.
- **Secrets:** Requires provider API keys (`GOOGLE_KEY`, `BING_KEY`, `ESRI_KEY`, `BAIDU_KEY`, `TOMTOM_KEY`, `MAPBOX_KEY`, `HERE_KEY`, `ORS_KEY`) stored in the `integration-remote` environment.
- **Usage:** Trigger manually when you want to validate against real APIs. Consider restricting environment access to maintainers.
