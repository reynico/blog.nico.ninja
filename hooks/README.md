# Git hooks

This pre-commit hook prevents to commit images that contains sensitive metadata.

## Install

```bash
cd ../../.git/hooks
ln -s ../../hooks/git-commit.sh pre-commit
chmod +x pre-commit
```