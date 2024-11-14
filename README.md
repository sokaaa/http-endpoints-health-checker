# HTTP Endpoints Health Checker

## Overview
This project implements a program to monitor the health of HTTP endpoints by periodically checking their response status and latency. The results are logged, displaying the availability percentage of each domain over time.

## Quick Start
1. Clone the repository and navigate to the directory.
2. Set up your `config.yaml` file and update the `.env` with its path.
3. Run `docker-compose up app` to start the service.
4. Run `docker-compose run --rm tests` to execute unit tests.

## Features
- Reads a YAML configuration file containing HTTP endpoints and related details.
- Checks the health of endpoints every 15 seconds.
- Logs the cumulative availability percentage of each domain.

## Prerequisites: Installing Docker

### Windows (Docker Desktop with WSL 2)

1. **Install WSL 2**:
   - Open PowerShell as Administrator and run:
     ```bash
     wsl --install
     ```
   - Restart your computer if prompted.

2. **Set WSL 2 as the Default Version**:
   ```bash
   wsl --set-default-version 2
   ```

3. **Download Docker Desktop**:
   - Visit [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) and download the installer.

4. **Install Docker Desktop**:
   - Run the downloaded installer and follow the on-screen instructions.
   - Ensure you check the option for **WSL 2** integration during installation.

5. **Configure Docker Desktop for WSL**:
   - Open Docker Desktop and go to **Settings** > **Resources** > **WSL Integration**.
   - Enable integration with your default WSL 2 distribution (e.g., Ubuntu).

6. **Verify the Installation**:
   - Open a WSL terminal or PowerShell and run:
     ```bash
     docker --version
     ```

### macOS

1. **Download Docker Desktop for macOS**:
   - Visit [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop/) and download the installer.

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file and drag the Docker icon to the **Applications** folder.
   - Launch Docker from the **Applications** folder.

3. **Verify the Installation**:
   - Open a terminal and run:
     ```bash
     docker --version
     ```

### Linux (Ubuntu/Debian-based)

1. **Uninstall Old Versions**:
   ```bash
   sudo apt-get remove docker docker-engine docker.io containerd runc
   ```

2. **Update the Package Index**:
   ```bash
   sudo apt-get update
   ```

3. **Install Required Packages**:
   ```bash
   sudo apt-get install -y ca-certificates curl gnupg lsb-release
   ```

4. **Add Docker’s Official GPG Key**:
   ```bash
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

5. **Set Up the Stable Repository**:
   ```bash
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

6. **Install Docker Engine**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io
   ```

7. **Start and Enable Docker**:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

8. **Verify the Installation**:
   ```bash
   docker --version
   ```

9. **Run Docker as a Non-root User (Optional)**:
   - Add your user to the `docker` group:
     ```bash
     sudo usermod -aG docker $USER
     ```
   - Log out and log back in for the changes to take effect.

---

### Notes:
- **Windows Users**: Ensure that your WSL distribution is set to WSL 2. You can check this by running `wsl -l -v`.
- **macOS Users**: Docker Desktop requires macOS 10.15 or newer.
- **Linux Users**: The installation instructions are specific to Ubuntu/Debian. For other distributions, refer to [Docker’s official documentation](https://docs.docker.com/engine/install/).
- **Docker Compose**: Ensure Docker Compose is installed. Check with:
  ```bash
  docker-compose --version
  ```
  [Install Docker Compose](https://docs.docker.com/compose/install/) if needed.


These steps will guide you through the process of installing Docker and setting up Docker Desktop (or Docker Engine) for your development environment.

## Installation and Setup

### 1. Clone the Repository
```bash
git clone https://github.com/sokaaa/http-endpoints-health-checker.git
cd http-endpoints-health-checker
```

### 2. Prepare Your Configuration

1. **Create or Use Your YAML Configuration File**:
   - Prepare a YAML file that specifies the HTTP endpoints to be monitored. Save this file in a location on your local system (e.g., `/path/to/your/config.yaml`).

   **Sample `config.yaml`**:
```yaml
- name: fetch index page
  url: https://fetch.com/
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor
- name: fetch careers page
  url: https://fetch.com/careers
  method: GET
  headers:
    user-agent: fetch-synthetic-monitor
- name: fetch post endpoint
  url: https://fetch.com/some/post/endpoint
  method: POST
  body: '{"foo":"bar"}'
  headers:
    content-type: application/json
    user-agent: fetch-synthetic-monitor
```

2. **Edit the `.env` File**:
   - In the project root directory, edit the `.env` file and add the path to your configuration file:
     ```env
     CONFIG_PATH=/path/to/your/config.yaml
     ```

   - Docker Compose reads the `.env` file to set environment variables referenced in the `docker-compose.yml` file.

3. **Verify Your `.env` File**:
   - Double-check that the `CONFIG_PATH` in the `.env` file points to the correct location of your configuration file on your host machine.

### Example `.env` File:
```env
CONFIG_PATH=/home/reviewer/myconfig/config.yaml
```

### 3. Run the Program
Once the `.env` file is set, run the following command to build and start the container:
```bash
docker-compose up app
```

### 4. Running Unit Tests
To run the unit tests, use the following command:
```bash
docker-compose run --rm tests
```

## Expected Output
After running `docker-compose up app`, you should see logs indicating the status checks and availability percentages:
```
2024-11-14 03:37:29,986 - Starting endpoint monitoring... Press CTRL+C to stop.
2024-11-14 03:37:30,166 - fetch index page (https://fetch.com/) is UP, latency: 150.44 ms
2024-11-14 03:37:30,166 - fetch careers page (https://fetch.com/careers) is UP, latency: 139.18 ms
2024-11-14 03:37:30,166 - fetch some fake post endpoint (https://fetch.com/some/post/endpoint) is DOWN, latency: 121.68 ms
2024-11-14 03:37:30,166 - fetch rewards index page (https://www.fetchrewards.com/) is UP, latency: 167.65 ms
2024-11-14 03:37:30,166 - fetch.com has 67% availability percentage
2024-11-14 03:37:30,166 - www.fetchrewards.com has 100% availability percentage
...
```

## Troubleshooting
### Common Issues
- **Mounting File Errors**: Ensure the path in `CONFIG_PATH` is an absolute path and points to a valid file.
- **Permissions**: Verify that Docker has access to the file specified in `CONFIG_PATH`.

### Checking Logs
To see real-time logs from the running container:
```bash
docker logs -f health-checker-app
```
