# SSH Configuration in Dev Container

This document explains how SSH is configured in the development container and how to troubleshoot common issues.

## 🔑 Overview

The dev container is configured to automatically mount your SSH keys and configuration from your host machine, allowing seamless Git operations using SSH authentication.

## 📋 How It Works

### 1. SSH Mount Configuration

In `devcontainer.json`, the following mount is configured:

```json
"mounts": [
  "source=${localEnv:HOME}${localEnv:USERPROFILE}/.ssh,target=/home/vscode/.ssh,type=bind,consistency=cached,readonly"
]
```

This mount:
- ✅ **Copies SSH keys** from host `~/.ssh` to container `/home/vscode/.ssh`
- ✅ **Read-only mount** - Your private keys remain secure on the host
- ✅ **Works on all platforms** - Uses `HOME` (Linux/Mac) or `USERPROFILE` (Windows)
- ✅ **Preserves SSH config** - Your `~/.ssh/config` is available in the container

### 2. Git Configuration Mount

```json
"mounts": [
  "source=${localEnv:HOME}${localEnv:USERPROFILE}/.gitconfig,target=/home/vscode/.gitconfig,type=bind,consistency=cached"
]
```

This ensures your Git identity and settings are available in the container.

### 3. SSH Agent Forwarding

```json
"remoteEnv": {
  "SSH_AUTH_SOCK": "${localEnv:SSH_AUTH_SOCK}"
}
```

Forwards the SSH agent socket from host to container (when available).

## 🚀 Getting Started

### Prerequisites on Host Machine

1. **Ensure SSH keys exist:**
   ```bash
   ls -la ~/.ssh/
   ```
   
   You should see files like:
   - `id_rsa` and `id_rsa.pub` (RSA key)
   - `id_ed25519` and `id_ed25519.pub` (Ed25519 key - recommended)
   - `config` (SSH configuration file)
   - `known_hosts` (Known server fingerprints)

2. **Generate SSH key if needed:**
   ```bash
   # Generate Ed25519 key (recommended)
   ssh-keygen -t ed25519 -C "your-email@example.com"
   
   # Or RSA key
   ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
   ```

3. **Add SSH key to Git provider:**
   ```bash
   # Display your public key
   cat ~/.ssh/id_ed25519.pub
   # or
   cat ~/.ssh/id_rsa.pub
   ```
   
   Copy the output and add it to:
   - **GitHub:** Settings → SSH and GPG keys → New SSH key
   - **GitLab:** Preferences → SSH Keys
   - **Bitbucket:** Personal settings → SSH keys

4. **Test SSH connection on host:**
   ```bash
   ssh -T git@github.com
   ssh -T git@gitlab.com
   ```

### Inside the Container

Once the container is running:

1. **Check SSH keys are mounted:**
   ```bash
   ls -la ~/.ssh/
   ```

2. **Test SSH connection:**
   ```bash
   # GitHub
   ssh -T git@github.com
   # Expected: "Hi username! You've successfully authenticated..."
   
   # GitLab
   ssh -T git@gitlab.com
   # Expected: "Welcome to GitLab, @username!"
   ```

3. **Use Git with SSH:**
   ```bash
   # Clone a repository
   git clone git@github.com:username/repo.git
   
   # Push/pull
   git push origin main
   git pull origin main
   ```

## 🔧 Advanced Configuration

### Custom SSH Key Names

If your SSH key has a custom name, create or edit `~/.ssh/config` on your **host machine**:

```bash
# GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/custom_github_key
  
# GitLab
Host gitlab.com
  HostName gitlab.com
  User git
  IdentityFile ~/.ssh/custom_gitlab_key
```

This configuration will be automatically available in the container.

### Multiple GitHub/GitLab Accounts

Configure different hosts in `~/.ssh/config`:

```bash
# Personal GitHub
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal
  
# Work GitHub
Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
```

Then use in Git:
```bash
# Personal repo
git clone git@github.com:personal/repo.git

# Work repo
git clone git@github-work:company/repo.git
```

### SSH Agent Setup (Optional)

If using SSH agent on the host:

**Linux/Mac:**
```bash
# Start SSH agent
eval "$(ssh-agent -s)"

# Add your key
ssh-add ~/.ssh/id_ed25519

# Verify
ssh-add -l
```

**Windows (PowerShell):**
```powershell
# Start SSH agent service
Start-Service ssh-agent

# Add your key
ssh-add $env:USERPROFILE\.ssh\id_ed25519

# Verify
ssh-add -l
```

## 🐛 Troubleshooting

### ❌ Permission denied (publickey)

**Symptoms:**
```bash
git@github.com: Permission denied (publickey).
```

**Causes & Solutions:**

1. **SSH key not added to Git provider**
   ```bash
   # On host, display public key
   cat ~/.ssh/id_ed25519.pub
   # Add to GitHub/GitLab settings
   ```

2. **Wrong key being used**
   ```bash
   # Check which key is being offered
   ssh -vT git@github.com
   
   # Specify key explicitly
   ssh -i ~/.ssh/your_key -T git@github.com
   ```

3. **SSH agent not running on host**
   ```bash
   # Start agent and add key
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

### ❌ SSH keys not visible in container

**Symptoms:**
```bash
ls ~/.ssh/
# Returns: ls: cannot access '/home/vscode/.ssh': No such file or directory
```

**Solutions:**

1. **Verify SSH directory exists on host:**
   ```bash
   # On your host machine
   ls -la ~/.ssh/
   ```

2. **Rebuild the container:**
   - `F1` → `Dev Containers: Rebuild Container`

3. **Check devcontainer.json mounts:**
   - Ensure the mounts section includes the SSH mount

### ❌ Permission too open warning

**Symptoms:**
```bash
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for '/home/vscode/.ssh/id_rsa' are too open.
```

**Solution:**

SSH keys are mounted read-only. The `post-create.sh` script handles this automatically by copying keys to a writable location:

```bash
# Manual fix if needed
mkdir -p ~/.ssh-temp
cp -r ~/.ssh/* ~/.ssh-temp/
chmod 700 ~/.ssh-temp
chmod 600 ~/.ssh-temp/id_*

# Use the copied keys
ssh-add ~/.ssh-temp/id_ed25519
```

### ❌ Host key verification failed

**Symptoms:**
```bash
The authenticity of host 'github.com' can't be established.
```

**Solution:**

This is normal on first connection. Accept the fingerprint:
```bash
# Manually add known hosts
ssh-keyscan github.com >> ~/.ssh/known_hosts
ssh-keyscan gitlab.com >> ~/.ssh/known_hosts
ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts
```

Or accept interactively:
```bash
ssh -T git@github.com
# Type 'yes' when prompted
```

### ❌ Git still asking for password

**Symptoms:**
Git prompts for username/password instead of using SSH.

**Cause:**
Repository is using HTTPS URL instead of SSH.

**Solutions:**

1. **Check remote URL:**
   ```bash
   git remote -v
   # If shows https://github.com/... it's using HTTPS
   ```

2. **Change to SSH URL:**
   ```bash
   git remote set-url origin git@github.com:username/repo.git
   ```

3. **Configure Git to always use SSH for GitHub:**
   ```bash
   git config --global url."git@github.com:".insteadOf "https://github.com/"
   ```

## 🔒 Security Best Practices

1. **✅ Use Ed25519 keys** - More secure and faster than RSA
   ```bash
   ssh-keygen -t ed25519 -C "your-email@example.com"
   ```

2. **✅ Use passphrase-protected keys** - Add extra security layer
   ```bash
   # Keys will prompt for passphrase when added to SSH agent
   ssh-add ~/.ssh/id_ed25519
   ```

3. **✅ Read-only mount** - Keys are mounted read-only by default, preventing container from modifying them

4. **✅ Different keys for different purposes**
   - Personal projects: `~/.ssh/id_ed25519_personal`
   - Work projects: `~/.ssh/id_ed25519_work`
   - Servers: `~/.ssh/id_ed25519_server`

5. **✅ Regular key rotation** - Rotate SSH keys periodically

6. **❌ Never commit private keys** - Only public keys (*.pub) should be shared

## 📊 Verification Checklist

Before opening an issue, verify:

- [ ] SSH keys exist on host: `ls ~/.ssh/`
- [ ] Public key added to Git provider (GitHub/GitLab)
- [ ] SSH connection works on host: `ssh -T git@github.com`
- [ ] Container has SSH keys mounted: `ls ~/.ssh/` (inside container)
- [ ] Correct remote URL: `git remote -v` shows `git@github.com:...`
- [ ] SSH config is valid: `cat ~/.ssh/config`
- [ ] Container was rebuilt after config changes

## 📚 Additional Resources

- [GitHub SSH Documentation](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitLab SSH Documentation](https://docs.gitlab.com/ee/user/ssh.html)
- [Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [SSH Config File Documentation](https://www.ssh.com/academy/ssh/config)

---

**Configured with 🔒 security and 🚀 convenience in mind!**

