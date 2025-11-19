
## Prerequisites

- Docker and Docker Compose
- Signal account (for bot)
- ATAK or WinTAK installed and configured to receive UDP CoT messages on port 4242

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd SignalATAK
```

### 2. Configure Environment Variables

Edit `envs/integration.env`:

```bash
# Signal Configuration
SIGNAL_SERVICE_HOST=signal-api
SIGNAL_SERVICE_PORT=8080
BOT_PHONE=+380971111111 # you can send to yourself

# ATAK Configuration
ATAK_HOST=192.168.0.157  # IP address of ATAK/WinTAK machine
ATAK_PORT=4242
ATAK_TIMEOUT=5
```

**Configuration Notes:**

- **Mac\Linux Setup**: Set `ATAK_HOST` to the Windows PC's IP or Android IP (e.g., `192.168.0.157`)
- **Windows Setup**: Set `ATAK_HOST` to `192.168.0.157` (your own LAN IP) or `host.docker.internal` for localhost

### 3. Link Signal Account (First Time Only)

The Signal CLI needs to be linked to your Signal account via QR code.

**Step 1:** Start signal-api in normal mode:

```bash
MODE=normal docker compose up signal-api
```

**Step 2:** Open your browser and navigate to:

```
http://127.0.0.1:8080/v1/qrcodelink?device_name=signal-atak-bot
```

**Step 3:** In your Signal mobile app:
- Open Settings → Linked Devices
- Tap "+" or "Link New Device"
- Scan the QR code displayed in your browser

**Step 4:** Wait for confirmation, then stop the container (Ctrl+C)

**Step 5:** Verify the link by checking:

```
http://127.0.0.1:8080/v1/about
```

Your account should be listed.

## Running the Bot

### Start All Services

```bash
docker compose up
```

Or run in detached mode:

```bash
docker compose up -d
```

### Stop Services

Press `Ctrl+C` if running in foreground, or:

```bash
docker compose down
```

## Usage

### Supported Commands

Send these commands to the bot via Signal:

#### Help Command
```
help
```
Shows usage instructions and examples.

#### List Target Types
```
types
```
Displays all supported target types.

#### Send Coordinates
```
LAT LON DESCRIPTION
```

**Examples:**
```
48.567123 39.87897 tank
50.450001 30.523333 aircraft
49.123456 31.654321 artillery
```

### Supported Target Types

| Keyword | CoT Type | Description |
|---------|----------|-------------|
| tank | a-h-G-E-V-A-T | Tank |
| apc | a-h-G-E-V-A-A | Armored Personnel Carrier |
| vehicle | a-h-G-E-V | Generic Vehicle |
| truck | a-h-G-E-V-C | Truck |
| artillery | a-h-G-E-W-A | Artillery |
| sam | a-h-G-E-W-M-A-L | Surface-to-Air Missile |
| mortar | a-h-G-E-W-O | Mortar |
| aircraft | a-h-A-M | Aircraft |
| bomber | a-h-A-M-F-B | Bomber |
| fighter | a-h-A-M-F-F | Fighter |
| helicopter | a-h-A-M-H | Helicopter |
| uav | a-h-A-M-F-Q | UAV/Drone |
| infantry | a-h-G-U-C-I | Infantry |

### Message Format

- **Latitude**: Decimal degrees (e.g., 48.567123)
- **Longitude**: Decimal degrees (e.g., 39.87897)
- **Description**: Must match one of the supported target types (case-insensitive)
- Coordinates can be positive or negative
- Spaces separate the three components

## ATAK/WinTAK Configuration

### Enable UDP Reception

**In WinTAK:**
1. Settings → Network Preferences → Network Connections
2. Add a new UDP input on port 4242
3. Set to "Listen on all interfaces" or specific IP

**In ATAK:**
1. Settings → Network Preferences → Input
2. Add UDP input on port 4242

### Firewall Configuration

Make sure UDP port 4242 is allowed through your firewall:

## Deployment Scenarios

### Scenario 1: Mac\Linux → Windows PC with WinTAK

**On Mac:**
```bash
# envs/integration.env
ATAK_HOST=192.168.0.157  # Windows PC's IP address

docker compose up
```

### Scenario 2: Windows with WinTAK (localhost)

**On Windows:**
```bash
# envs/integration.env
ATAK_HOST=192.168.0.157  # Your own IP (or host.docker.internal)

docker compose up
```
