<!-- Copyright (c) ONNX Project Contributors -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Releasing DigestAI

## One-time PyPI setup

Track account ownership and publishing access in [issue #30](https://github.com/onnx/digestai/issues/30).
An authorized PyPI maintainer must configure the project (or a pending publisher)
with these GitHub Trusted Publisher values:

- Owner: `onnx`
- Repository: `digestai`
- Workflow filename: `release.yml`
- Environment: `pypi`

Create the GitHub `pypi` environment with the desired release reviewers and tag
restrictions. Once access is verified, set the repository Actions variable
`PYPI_PUBLISH_ENABLED` to `true`. No stored PyPI API token is required.
Until then, release builds and GitHub downloads work, and PyPI publishing is skipped.

## Prepare and verify a release

1. Merge the release fixes and require successful CI, including the installed-wheel
   and Windows executable checks.
2. Choose an unused version, update `project.version` in `pyproject.toml`, refresh
   `pixi.lock` with `pixi lock`, and update the release badge and `CHANGELOG.md`.
   Include supported Python versions and user-visible changes in the notes.
3. Commit those changes and create a matching `v<version>` tag on the reviewed commit.
   The release workflow rejects a tag that does not match the package version.
4. Run **Release artifacts** manually for that tag for a rehearsal. This builds,
   tests, and uploads workflow artifacts without creating a release or publishing
   to PyPI. Inspect the wheel, sdist, and Windows ZIP; manually exercise the GUI
   with a representative model, dynamic inputs, and a multi-model folder.
5. Publish a GitHub Release for that same tag with the prepared release notes.
   This triggers fresh builds and tests, attaches the Python distributions,
   `digestai-windows-x64.zip`, and `SHA256SUMS.txt`, then publishes to PyPI if enabled.
   Approve the `pypi` environment job if environment protection requires it.
6. Confirm the release downloads work. If PyPI is enabled, install the exact new
   version into a clean environment with `python -m pip install digestai==<version>`
   and launch `digest`.

Python wheels are built from the sdist and tested outside the checkout. GUI tests
use a deterministic similarity fixture; manually check real similarity analysis
as well. The Windows smoke test verifies startup, not every GUI interaction.

## Retry and recovery

Inspect failed Actions logs before retrying. GitHub assets are replaced on a rerun;
PyPI does not allow replacing an uploaded version. If PyPI upload succeeded, rerun
only failed jobs rather than the successful publishing job. Ship a new version to
correct published package contents. Do not move a released version tag.
