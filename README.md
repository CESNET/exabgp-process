# ExaBGP Process Package

[![PyPI version](https://badge.fury.io/py/exabgp-process.svg)](https://badge.fury.io/py/exabgp-process)
[![PyPI](https://img.shields.io/pypi/v/exabgp-process.svg)](https://pypi.org/project/exabgp-process/)

This application is a simple API that interfaces with the [ExaBGP service](https://github.com/Exa-Networks/exabgp/tree/main).

Each time this app receives a new command, it forwards the command to ExaBGP via stdout. The registered ExaBGP service monitors the stdout of this API application.

## Installation

Install the package using pip:
```bash
pip install exabgp-process
```

Alternative installation methods:
```bash
# Using uv
uv pip install exabgp-process

# Using Poetry (create a new project first)
poetry new my-exabgp-project
cd my-exabgp-project
poetry add exabgp-process
```

## Configuration

### 1. Generate Configuration File
After installation, generate the configuration file:
```bash
exabgp-process --generate-config > process.conf
```

### 2. Edit Configuration
Open `process.conf` and configure according to your needs:

**For RabbitMQ (recommended for production):**
```ini
[api]
type = rabbitmq
```
Don't forged to set you rabbitmq host, username, password etc.

**For HTTP (development/testing only - no security layer):**
```ini
[api]
type = http
```
You can then configure the server IP and PORT if you need.

### 3. Set Up Log Directory
Ensure the log directory exists and is writable by the ExaBGP process:
```bash
# Create the log directory specified in your config
sudo mkdir -p /var/log/myapp
sudo chown exabgp:exabgp /var/log/myapp  # Adjust user/group as needed
```

### 4. Install Configuration
Copy the configuration file to the appropriate location:
```bash
sudo mv process.conf /etc/exabgp/process.conf
```

The application searches for configuration files in the following locations (in order):
- `api.conf` (current directory)
- `process.conf` (current directory)
- `/etc/exabgp_process/process.conf`
- `/etc/exabgp/process.conf`
- `/usr/local/etc/exabgp_process/process.conf`

## Integration with ExaBGP

Add the following to your ExaBGP configuration file:
```
process flowspec {
    run /usr/local/bin/exabgp-process;
    encoder json;
}
```

**Note:** The exact path to `exabgp-process` may vary depending on your installation. You can find it using:
```bash
which exabgp-process
```

## Usage

### Standalone Mode (for testing)
You can run the process directly for testing:
```bash
exabgp-process
```

### Message Format
The application expects JSON messages with the following structure:
```json
{
    "author": "username",
    "source": "application_name",
    "command": "announce route 192.0.2.1/32 next-hop 192.0.2.254"
}
```

- `author`: For logging purposes (who initiated the command)
- `source`: For logging purposes (which application sent the command)
- `command`: The actual ExaBGP command to execute

### RabbitMQ Setup
When using RabbitMQ, ensure your RabbitMQ server is running and accessible with the credentials specified in your configuration file.

### HTTP Setup
**Security Warning:** The HTTP version has no authentication or encryption. Only use it for development/testing, and restrict access to localhost only. It also uses only Flask development server, that is also not recomended for production usage. 

## Development and Testing

For development and testing, the HTTP version is available. However, please note that this web app lacks any security layer. Therefore, it's recommended to:
- Restrict access to localhost only
- Use RabbitMQ for production environments
- Never expose the HTTP API to public networks

For more information, refer to the [ExaBGP documentation](https://github.com/Exa-Networks/exabgp/wiki/Controlling-ExaBGP-:-possible-options-for-process).

## Troubleshooting

### Package Not Found
If `exabgp-process` command is not found after installation:
```bash
# Verify installation
pip show exabgp-process

# Find the executable
which exabgp-process

# If using a virtual environment, make sure it's activated
source venv/bin/activate
```

### Permission Errors
Ensure the log directory has proper permissions:
```bash
sudo chown -R <exabgp-user>:<exabgp-group> /var/log/myapp
```

### Connection Issues with RabbitMQ
- Verify RabbitMQ is running: `sudo systemctl status rabbitmq-server`
- Check credentials and vhost configuration
- Ensure the queue exists or the user has permissions to create it

## Changelog

- **1.0.4** - Fixed template for config file
- **1.0.3** - New format of message from server - JSON with keys: `author`, `source`, `command`. Author and source are for logging purposes, command is sent to the process
- **1.0.2** - Switch to pyproject.toml for better description

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.