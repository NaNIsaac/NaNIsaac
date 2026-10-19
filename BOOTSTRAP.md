# Bootstrap

Entry point for an empty machine. The real setup lives in the private repo `NaNIsaac/DotFiles`; this page only gets you far enough to read it.

1. Install GitHub CLI and sign in. Signing in is a manual step.
   - Windows: `winget install --id GitHub.cli -e`
   - Linux/WSL: see https://github.com/cli/cli/blob/trunk/docs/install_linux.md
   - Then `gh auth login`
2. Set `DEV`, the root where all repositories live as `$DEV/<owner>/<repo>`. One value per machine, per OS (WSL is its own machine).
   - Windows: `[Environment]::SetEnvironmentVariable('DEV', 'D:\dev', 'User')`, then open a new shell
   - Linux/WSL: `export DEV=~/dev` in the shell profile
3. Clone DotFiles and follow its README.
   ```
   gh repo clone NaNIsaac/DotFiles $DEV/NaNIsaac/DotFiles
   ```

Agents: do step 1 only after the user has confirmed they are signed in. Do not enter credentials.
