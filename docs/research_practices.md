# Artifact provenance and reuse

`manifest.json` records SHA256 hashes for packaged files and the original source files used for portable components. Provenance paths are relative source labels, not machine-specific runnable paths.

The quarantine module is an unchanged source copy. The constructor is a portable extraction of the fixed core and Gemma `native_statement_record` variant, not every frozen model configuration.

Model checkpoints, upstream corpus text, private credentials, and exploratory API records are not distributed. Obtain models and data from their providers under the applicable licenses. A repository-wide software license has not yet been selected.

See the [reproduction guide](reproduction.md) for required inputs and current availability. Unpublished frozen inputs are not downloadable from this initial package.
