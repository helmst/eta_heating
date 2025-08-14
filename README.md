# ETA Heizung Home Assistant Integration

Diese Integration bindet die REST-Schnittstelle deiner ETA-Heizung in Home Assistant ein und stellt verschiedene Werte als Entitäten bereit.

## Installation (HACS)
1. Dieses Repository in HACS als Custom Repository hinzufügen.
2. Die Integration `eta_heizung` installieren.
3. Über die Home Assistant Oberfläche konfigurieren (IP/Port angeben).
4. Entitäten/Sensoren/Schalter/Nummern nach Bedarf konfigurieren.

## Konfiguration

### Beispiel für `configuration.yaml`:

```yaml
eta_heizung:
  host: 192.168.1.100
  port: 8080
  sensors:
    - name: "Kesseltemperatur"
      uri: "/112/10021/0/0/12180"
      unit: "°C"
    - name: "Pelletsbehälter"
      uri: "/112/10021/0/0/12011"
      unit: "kg"
  switches:
    - name: "Entaschentaste"
      uri: "/112/10021/0/0/12112"
      on_value: "1803"
      off_value: "1802"
    - name: "Ein/Aus Taste"
      uri: "/112/10101/0/0/12080"
      on_value: "1"
      off_value: "0"
  numbers:
    - name: "Heizzeit Montag Zeitfenster 1"
      uri: "/112/10101/12113/0/1082"
      min: 0
      max: 96
```

### Entitäten finden

Die URI und Bezeichnung findest du im Menübaum deiner ETA-Heizung (`/user/menu`). Für editierbare Werte muss die URI aus der XML extrahiert werden.

## Features

- Automatische Menübaum-Integration
- Konfigurierbare Sensoren, Switches, Numbers
- Deutschsprachige Oberfläche
- Fehlerabfrage als Sensor möglich (`/user/errors`)
- Editierbare Entitäten (z.B. Heizzeiten, Tasten)

## Hinweise

- Die Integration ist experimentell und kann weiter ausgebaut werden!
- Feedback und PRs gerne willkommen!
