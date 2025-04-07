# ⚽ 3D Fußballfeld-Simulation mit physikalischer Ballflugbahn

## 🎓 Studienprojekt – Angewandte Mathematik 2

Dieses Projekt wurde im Rahmen des Moduls **Angewandte Mathematik 2** im Studiengang *International Business Management* an der **Hochschule Bremen** erstellt. Ziel ist es, reale physikalische Kräfte auf einen Fußball zu simulieren und interaktiv in einer 3D-Umgebung darzustellen.

---

## 🧠 Projektbeschreibung

Die Anwendung simuliert den Schuss eines Fußballs in einem 3D-Modell eines Fußballfeldes. Dabei werden Gravitation, Luftwiderstand, Spin (Magnus-Effekt) und Bodenreibung berücksichtigt. Die Flugbahn wird visuell dargestellt, inklusive Kollision mit einer Wand zur besseren Analyse von Flugkurven.

---

## 🔍 Features

- **3D Visualisierung** des Fußballfeldes inkl. Tore, Mittelkreis, Strafräume und Ecken
- **Simulierbare Ballschüsse** mit:
  - Geschwindigkeit
  - horizontalem & vertikalem Winkel
  - Spin (X, Y, Z)
  - frei wählbarer Startposition
- **Physikalisch korrekte Bewegung** mit:
  - Gravitation
  - Luftwiderstand
  - Magnus-Kraft
  - Bodenreibung
- **Interaktive Oberfläche** mit:
  - Zoom & Rotation per Maus/Tastatur
  - „Messi“ & „Ronaldo“-Presets
  - Wandkollisionen mit Log-Ausgabe
  - Mehrfarbige Flugkurven
  - Zurücksetzen- und Clear-Funktionen

---

## 📁 Projektstruktur

```
Fussball/
├── Main.py               # GUI mit Simulation und Benutzerinteraktion
├── constants.py          # Alle Feld- und Physikkonstanten
├── physics.py            # Physikberechnungen (Kräfte, Bewegung, Kollisionen)
├── visualization.py      # Zeichnet Spielfeld, Ball, Tore und Wand
├── erklärung physik      # Erklärung der Physikfunktionen (z.B. Kommentare)
└── __pycache__/          # Python-Cache
```

---

## ⚙️ Technologien

- **Python 3**
- **Tkinter** – GUI
- **Matplotlib (3D)** – Darstellung & Ballanimation
- **NumPy** – Physikalische Berechnungen

---

## ▶️ Ausführen

**Voraussetzungen:**

```bash
pip install matplotlib numpy
```

**Starten:**

```bash
python Main.py
```

---

## 🧮 Verwendete Formeln

- **Gravitationskraft**:  
  \[ \vec{F}_g = m \cdot \vec{g} \]
- **Luftwiderstand**:  
  \[ \vec{F}_d = -\frac{1}{2} \cdot \rho \cdot c_d \cdot A \cdot v^2 \cdot \hat{v} \]
- **Magnus-Kraft**:  
  \[ \vec{F}_m = k \cdot \rho \cdot A \cdot (\vec{\omega} \times \vec{v}) \]
- **Reibung bei Bodenkontakt**:  
  \[ \vec{F}_r = -\mu \cdot F_n \cdot \hat{v} \]

---

## 🧑‍🎓 Autor

**Eyüphan Bayram**  
Studiengang: International Medieninformatik  
Modul: Angewandte Mathematik 2  
Hochschule Bremen  
📅 Jahr: 2023

---

## 💡 Weiterentwicklungsideen

- Live-Grafik mit Geschwindigkeit & Kraft
- Weitere Spielereignisse (z.B. Schüsse aufs Tor mit Keeper)
- Speichern/Laden von Schüssen
- Netzwerkversion mit Mehrspielermodus

---

Bei Fragen, Anmerkungen oder Verbesserungsvorschlägen freue ich mich über Feedback!
