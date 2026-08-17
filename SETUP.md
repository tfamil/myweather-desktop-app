# GitHub profile stats setup

1. Copy `README.md` into your `tfamil/tfamil` profile repository.
2. Copy `.github/workflows/grs.yml` into the same repository.
3. Commit and push both files.
4. Open the repository on GitHub.
5. Go to **Actions** → **Update README cards** → **Run workflow**.
6. Wait for the workflow to finish.
7. The workflow will create and commit:
   - `profile/stats.svg`
   - `profile/top-langs.svg`
8. Refresh your GitHub profile.

After the first manual run, the workflow refreshes the cards daily.

By default this uses GitHub's built-in `GITHUB_TOKEN`, so the cards use public repository data.
