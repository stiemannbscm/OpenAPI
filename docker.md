# Linux-Server Setup – Todo-Listen-Verwaltung

Diese Anleitung beschreibt die vollständige Einrichtung eines Linux-Servers (in diesem Fall auf Raspberry Pi OS) über die Konsole. Ziel ist der Betrieb einer containerisierten Web-App mit statischer Netzwerkkonfiguration.

## Voraussetzungen

- Frisches Raspberry Pi OS oder Pi OS Lite, da keine Desktop Umgebung gebraucht wird
- Internetverbindung
- Zugriff über SSH – bei Installation des Betriebssystems kann dies direkt aktiviert werden
- Bei der Installation kann ein Nutzer angelegt werden. Erstelle den Nutzer `fernzugriff` mit einem gewählten Passwort

---
Schließe den Raspberry an Strom an und warte ein wenig bis er hochgefahren ist.

## 1. SSH Verbindung mit dem Raspberry Pi herstellen

### Über das `Terminal`
```bash
  ssh fernzugriff@raspberrypi.local
```
Akzeptiere die Verbindung und gebe dein Passwort ein und du bist mit dem Raspberry verbunden

## 2. Statische IP-Adresse setzen
### Über `systemd-networkd`

1. **Deaktiviere den DHCP-Client** (falls aktiv), damit `systemd-networkd` die Kontrolle übernimmt:

```bash
  sudo systemctl disable dhcpcd   # verhindert Start bei Boot
  sudo systemctl stop dhcpcd      # stoppt laufenden Dienst sofort
```
Es können Fehlermeldungen ausgegeben werden, wenn der Client nicht läuft. Diese können dann Ignoriert werden.

2. **Bestehende Netzwerkkonfiguration abrufen**
```bash
  cat /etc/resolv.conf # gibt das aktuelle standard Gateway aus
```
Beispielausgabe:
```ini
# Generated by NetworkManager
nameserver 192.168.1.1 # diese Adresse ist das Standartgateway
```
Der nameserver gibt das Standard Gateway an

```bash
  ip route # gibt den DNS Server aus
```
Beispielausgabe: 
```ini
default via 192.168.1.1 dev wlan0 proto dhcp src 192.168.1.111 metric 600 # die erste Adresse ist der DNS Server
192.168.1.0/24 dev wlan0 proto kernel scope link src 192.168.1.111 metric 600 
```
Hier ist `default via 192.168.1.1` wichtig

3. **Konfigurationsdatei für statische IP erstellen**:

```bash
  sudo nano /etc/systemd/network/10-static.network #öffnet eine Datei für die Netzwerkkonfiguration
```

Inhalt der Datei (gegebenenfalls Interface anpassen):

```ini
[Match]
Name=eth0  # oder wlan0, je nach Verbindung

[Network]
Address=192.168.1.42/24 # oder die gewünschte IP-Adresse
Gateway=192.168.1.1 # die Adresse aus 'cat /etc/resolv.conf'
DNS=192.168.1.1 # die Adresse aus 'ip route'
```

> ⚠ `eth0` ist das kabelgebundenes Netzwerk, `wlan0` das eingebaute WLAN. 

4. **Netzwerkdienst aktivieren und starten:**

```bash
  sudo systemctl enable systemd-networkd   # startet Dienst bei jedem Boot
  sudo systemctl start systemd-networkd    # startet Dienst jetzt sofort
```

5. **System neu starten, um Änderungen zu übernehmen:**

```bash
  sudo reboot
```

---

## 2. Benutzer einrichten

### Willi (Standardnutzer ohne sudo-Rechte und ohne SSH rechte):
1. Nutzer erstellen
```bash
  sudo useradd -m willi        # erstellt Benutzer mit Home-Verzeichnis
  sudo passwd willi            # setzt Passwort (wird interaktiv abgefragt)
```
2. SSH zugriff einschränken

```bash
sudo nano /etc/ssh/sshd_config
```
Am Ende der Datei `AllowUsers fernzugriff` einfügen und dann SSH mit 
```bash
  sudo systemctl restart ssh
```
neustarten.

---

## 3. Docker & Docker Compose installieren

### Docker:

```bash
  curl -sSL https://get.docker.com | sh  # installiert Docker automatisch
  sudo usermod -aG docker fernzugriff    # erlaubt fernzugriff die Nutzung von Docker
```

### Docker Compose:

```bash
  sudo apt install -y docker-compose  # installiert docker-compose über apt
```

### Neustart:

```bash
  sudo reboot
```

---

## 4. Todo-App als Container deployen

### Verzeichnis anlegen und vorbereiten:

```bash
  sudo mkdir -p /opt/todo-app                  # Zielordner für die App
  sudo chown fernzugriff:fernzugriff /opt/todo-app  # Besitzerrechte anpassen
  cd /opt/todo-app
```

### Skript erstellen, dass das Repository klont, alle nötigen Dateien erstellt und den Container startet
```bash
  sudo nano /opt/todo-app/setup.sh
```
In diese Datei muss folgender Inhalt kopiert werden:
```ini
#!/bin/bash
set -e

mkdir -p backend
git clone https://github.com/stiemannbscm/OpenAPI.git backend

# Dockerfile erstellen
cat <<EOF > backend/Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "server.py"]
EOF

# docker-compose.yml erstellen
cat <<EOF > docker-compose.yml
version: "3.8"
services:
  todo-backend:
    build: ./backend
    ports:
      - "5000:5000"
    restart: always
EOF

# Docker-Container starten
docker-compose up -d
```
Mit
```bash
  chmod +x setup.sh
```
wird das script ausführbar gemacht, dann
```bash
  ./setup.sh
```
um den Container zu Installieren und zu starten.

---

## 5. Optional: Autostart

Docker beim Boot automatisch starten:

```bash
  sudo systemctl enable docker
```

---

## 6. Fertig!

## 7. Test

### Um zu testen ob alles geklappt hat, im SSH Terminal des Raspberrys:
```bash
  curl http://localhost:5000/todo-lists
```
### ausführen. Es sollte ein leeres Array zurück gegeben werden.