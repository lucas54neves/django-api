# GitHub Actions CI/CD Workflow

This directory contains the GitHub Actions workflows for continuous integration (CI) of the project.

## 📋 Workflow: CI - Lint and Tests

**File:** `ci.yml`

### When is it executed?

The workflow is automatically triggered on:
- ✅ **Push** to the `main` branch
- ✅ **Pull Request** targeting the `main` branch

### What does the workflow do?

The workflow executes the following steps on an Ubuntu machine with multiple Python versions (3.11 and 3.12):

#### 1. 🔍 Formatting Check (Black)
- Checks if the code is formatted according to Black standards
- **Fails if:** there is unformatted code
- **How to fix:** Run `make format` or `black .`

#### 2. 📦 Import Organization (isort)
- Checks if imports are properly organized
- **Fails if:** there are unorganized imports
- **How to fix:** Run `make format` or `isort .`

#### 3. 🐍 Code Linting (Flake8)
- Checks for syntax errors and style issues
- Checks cyclomatic complexity (max: 10)
- Checks line length (max: 127 characters)
- **Fails if:** there are critical violations
- **How to fix:** Run `flake8 .` and fix the issues

#### 4. 🔬 Static Analysis (Pylint)
- Analyzes code for errors and issues
- Focuses on errors (E) and fatal issues (F)
- **Warning:** Does not fail the build, only warns
- **How to fix:** Run `pylint --disable=all --enable=E,F **/*.py`

#### 5. 🧪 Django Tests
- Runs all project tests
- Uses Django test runner
- **Fails if:** any test fails
- **How to fix:** Run `make test` and fix the tests

#### 6. 📊 Test Coverage
- Generates code coverage report
- Creates HTML report
- **Warning:** Does not fail the build
- **How to view:** Download the artifact after execution

### Python Version Matrix

The workflow tests the code on:
- Python 3.11
- Python 3.12

This ensures compatibility across versions.

## 🚀 How to use locally

Before pushing or creating a PR, run locally:

```bash
# Install development dependencies
make install-dev

# Run ALL checks (same as CI)
make check

# Or run individually:
make lint          # All linting checks
make test          # All tests
make test-coverage # Tests with coverage
make format        # Fix formatting automatically
```

## 📈 Viewing results on GitHub

1. Access your repository on GitHub
2. Click on the **"Actions"** tab
3. Select the **"CI - Lint and Tests"** workflow
4. Click on a specific run to see details
5. Each step shows detailed logs
6. Artifacts (coverage reports) are available for 30 days

## 🔧 Linter Configurations

Linter configurations are located in:

- **Flake8:** `.flake8` - Style settings and exclusions
- **Black/isort/Pylint:** `pyproject.toml` - Formatting settings
- **Coverage:** `pyproject.toml` - Coverage settings

### .flake8 File

```ini
[flake8]
max-line-length = 127
exclude = venv, migrations, __pycache__
ignore = E203, W503, E501
max-complexity = 10
```

### pyproject.toml Section

```toml
[tool.black]
line-length = 127
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 127
```

## 🛠️ Customizing the Workflow

To modify the workflow:

1. Edit the `ci.yml` file
2. You can:
   - Add more Python versions to the matrix
   - Add new linters or tools
   - Modify failure conditions
   - Add notifications (Slack, Discord, etc)
   - Add automatic deployment after success

### Example: Add Python 3.13

```yaml
strategy:
  matrix:
    python-version: ['3.11', '3.12', '3.13']
```

### Example: Add Slack notification

```yaml
- name: Notify Slack
  if: failure()
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 📊 Badges for README

You can add badges to your README to show CI status:

```markdown
![CI Status](https://github.com/your-username/your-repo/workflows/CI%20-%20Lint%20and%20Tests/badge.svg)
```

## ❓ Common Issues

### ❌ Error: "Black would reformat"
**Solution:** Run `make format` or `black .` locally

### ❌ Error: "Imports are incorrectly sorted"
**Solution:** Run `make format` or `isort .` locally

### ❌ Error: "Flake8 found errors"
**Solution:** Run `flake8 .` and fix the reported issues

### ❌ Error: "Test failed"
**Solution:** Run `make test` locally and fix the tests

### ⚠️ Workflow didn't run
**Check:**
- If you have permission to run workflows
- If Actions are enabled in the repository (Settings > Actions)
- If the `.github/workflows/ci.yml` file is in the correct branch

## 🔒 Branch Protection

To ensure no untested code is merged, configure branch protection:

1. Go to **Settings > Branches**
2. Add rule for the `main` branch
3. Enable:
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
4. Select the **"lint-and-test"** check

This will prevent merging PRs with failing tests or lint!

## 📚 Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Black Documentation](https://black.readthedocs.io/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Coverage.py Documentation](https://coverage.readthedocs.io/)
