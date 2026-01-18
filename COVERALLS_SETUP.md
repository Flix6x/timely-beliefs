# Setting Up Coveralls for Test Coverage Reporting

This document explains how to set up Coveralls to enable automated test coverage reporting for the timely-beliefs repository.

## Prerequisites

- Admin access to the GitHub repository
- Ability to add secrets to the repository

## Setup Steps

### 1. Create a Coveralls Account

1. Go to [coveralls.io](https://coveralls.io/)
2. Click "Sign in" or "Sign up with GitHub"
3. Authorize Coveralls to access your GitHub account
4. If this is your first time, you may need to grant Coveralls access to your repositories

### 2. Add the Repository to Coveralls

1. Once logged in to Coveralls, go to your repositories page
2. Click "Add Repos" or find the "+" button
3. Locate `Flix6x/timely-beliefs` in the list
4. Toggle the switch to enable coverage tracking for this repository
5. Click on the repository name to access its settings

### 3. Get the Repository Token

1. In the Coveralls repository settings page
2. Look for the "Repo Token" section
3. Copy the token (it will look something like: `AbCdEf123456...`)
4. **Keep this token secret!** Do not commit it to the repository

### 4. Add the Token to GitHub Secrets

1. Go to your GitHub repository: `https://github.com/Flix6x/timely-beliefs`
2. Click on "Settings" (repository settings, not your account)
3. In the left sidebar, click "Secrets and variables" → "Actions"
4. Click "New repository secret"
5. Set the name to: `COVERALLS_REPO_TOKEN`
6. Paste the token from Coveralls as the value
7. Click "Add secret"

### 5. Verify the Setup

Once the secret is added:

1. The next time the GitHub Actions workflow runs (on push or PR), it will:
   - Run the tests with coverage collection
   - Upload the coverage data to Coveralls
   - Coveralls will process and display the coverage report

2. You can verify it's working by:
   - Checking the "Actions" tab in GitHub - the workflow should complete without errors
   - Visiting your Coveralls dashboard to see the coverage report
   - The coverage badge in the README will update automatically once coverage data is uploaded

## Badge Configuration

The README already includes the Coveralls badge:

```markdown
[![Coverage Status](https://coveralls.io/repos/github/Flix6x/timely-beliefs/badge.svg?branch=main)](https://coveralls.io/github/Flix6x/timely-beliefs?branch=main)
```

This badge will:
- Show "unknown" until the first coverage report is uploaded
- Update automatically after each successful coverage upload
- Display the coverage percentage with color coding (red/yellow/green)
- Link to the detailed coverage report on Coveralls

## Alternative: Using GitHub Token Only

If you prefer not to use a Coveralls-specific token, the workflow is also configured to work with just the `GITHUB_TOKEN` (which is automatically available in GitHub Actions). However, using the `COVERALLS_REPO_TOKEN` is more reliable and provides better error messages.

## Troubleshooting

### Coverage not showing up on Coveralls

1. Check the GitHub Actions logs for errors in the "Upload coverage to Coveralls" step
2. Verify the `COVERALLS_REPO_TOKEN` secret is set correctly
3. Ensure the repository is enabled on Coveralls
4. Make sure the branch name matches (default is `main`, check your default branch)

### Badge showing "unknown"

- This is normal until the first coverage report is uploaded successfully
- Push a commit to trigger the workflow
- Wait for the workflow to complete
- Refresh the README to see the updated badge

### Permission errors

- Ensure Coveralls has been granted access to the repository
- Check that the repository token hasn't been regenerated on Coveralls (if so, update the GitHub secret)

## Updating Coverage

Coverage reports are automatically generated and uploaded on:
- Every push to any branch
- Every pull request

To manually check coverage locally:

```bash
make test  # Runs tests with coverage (pytest-cov is configured in pyproject.toml)
```

The coverage report will be displayed in the terminal and saved to `coverage.lcov` (which is gitignored).

## Additional Resources

- [Coveralls Documentation](https://docs.coveralls.io/)
- [Coveralls GitHub Action](https://github.com/marketplace/actions/coveralls-github-action)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)

## Notes

- Coverage is only uploaded from Python 3.12 builds to avoid duplicate reports
- The `coverage.lcov` file is excluded from git (see `.gitignore`)
- Coverage data includes all files in `timely_beliefs/` except test files
- See `TEST_COVERAGE_RECOMMENDATIONS.md` for guidance on improving coverage
