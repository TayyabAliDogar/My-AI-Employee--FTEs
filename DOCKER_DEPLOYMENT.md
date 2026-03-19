# AI Employee - Gold Tier - Docker Deployment

## Quick Start

### Prerequisites
- Docker Desktop installed
- Docker Compose installed
- 8GB RAM minimum
- 20GB disk space

### 1. Configure Environment
```bash
# Copy and edit .env file
cp .env.example .env
# Edit .env with your credentials
```

### 2. Start All Services
```bash
docker-compose up -d
```

### 3. Check Status
```bash
docker-compose ps
```

### 4. View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f odoo
docker-compose logs -f instagram-watcher
```

### 5. Stop Services
```bash
docker-compose down
```

### 6. Stop and Remove Data
```bash
docker-compose down -v
```

## Services

### Odoo (Port 8069)
- **URL:** http://localhost:8069
- **Database:** odoo_ai
- **User:** admin
- **Password:** admin

### PostgreSQL (Internal)
- **Host:** db
- **Port:** 5432
- **User:** odoo
- **Password:** odoo

### Watchers (Background)
- Gmail Watcher
- Instagram Watcher
- Facebook Watcher
- Twitter Watcher
- LinkedIn Watcher

### CEO Briefing (Scheduled)
- Runs every Monday at 8 AM
- Generates report in `Vault/CEO_Briefings/`

## Configuration

### Change CEO Briefing Schedule
Edit `docker-compose.yml`:
```yaml
ceo-briefing:
  environment:
    - SCHEDULE=0 8 * * 1  # Monday 8 AM
```

Cron format: `minute hour day month weekday`

Examples:
- Daily 9 AM: `0 9 * * *`
- Every Monday 8 AM: `0 8 * * 1`
- First of month: `0 9 1 * *`

### Disable a Watcher
Comment out in `docker-compose.yml`:
```yaml
# instagram-watcher:
#   build: ...
```

### Custom Odoo Configuration
Create `odoo-config/odoo.conf`:
```ini
[options]
admin_passwd = admin
db_host = db
db_port = 5432
db_user = odoo
db_password = odoo
```

## Troubleshooting

### Odoo Won't Start
```bash
# Check database
docker-compose logs db

# Restart Odoo
docker-compose restart odoo
```

### Watcher Not Running
```bash
# Check logs
docker-compose logs instagram-watcher

# Restart watcher
docker-compose restart instagram-watcher
```

### Database Connection Error
```bash
# Ensure database is healthy
docker-compose ps

# Check network
docker network inspect my-ai-employee-ftes_odoo-network
```

### Reset Everything
```bash
# Stop and remove all data
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Start fresh
docker-compose up -d
```

## Monitoring

### Resource Usage
```bash
docker stats
```

### Service Health
```bash
docker-compose ps
```

### Logs Location
- Container logs: `docker-compose logs`
- Vault logs: `./Vault/Logs/`
- CEO Briefings: `./Vault/CEO_Briefings/`

## Scaling

### Run Multiple Instances
```bash
docker-compose up -d --scale instagram-watcher=2
```

### Increase Resources
Edit Docker Desktop settings:
- Memory: 8GB+
- CPUs: 4+
- Disk: 20GB+

## Backup

### Backup Database
```bash
docker exec odoo_postgres pg_dump -U odoo odoo_ai > backup.sql
```

### Restore Database
```bash
docker exec -i odoo_postgres psql -U odoo odoo_ai < backup.sql
```

### Backup Vault
```bash
tar -czf vault-backup.tar.gz Vault/
```

## Production Deployment

### Use External Database
Edit `docker-compose.yml`:
```yaml
odoo:
  environment:
    - HOST=your-db-host.com
    - USER=odoo
    - PASSWORD=secure-password
```

### Enable HTTPS
Use nginx reverse proxy:
```yaml
nginx:
  image: nginx:alpine
  ports:
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf
    - ./ssl:/etc/nginx/ssl
```

### Set Resource Limits
```yaml
odoo:
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
```

## Updates

### Update Odoo
```bash
docker-compose pull odoo
docker-compose up -d odoo
```

### Update Watchers
```bash
docker-compose build --no-cache
docker-compose up -d
```

## Security

### Change Default Passwords
Edit `.env`:
```
ODOO_PASSWORD=your-secure-password
POSTGRES_PASSWORD=your-secure-password
```

### Restrict Network Access
```yaml
odoo:
  ports:
    - "127.0.0.1:8069:8069"  # Only localhost
```

### Enable Firewall
```bash
# Allow only necessary ports
ufw allow 8069/tcp
```

---

*Gold Tier AI Employee - Docker Deployment Guide*
*Built with Claude Code - March 2026*
