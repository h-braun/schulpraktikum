# pong_schulpraktikum



## Getting started

Zuerst sollte eine neue virtuelle Umgebung für Python im Zielverzeichnis angelegt werden.

Für Windows:

```
py -m venv .
```

Die neue virtuelle Umgebung kann wie folgt aus dem Terminal gestartet werden

```
.\Scripts\activate.ps1
```

Eventuell müssen die Ausführungsrichtlien mit `Set-ExecutionPolicy RemoteSigned` in `powershell.exe` angepasst werden.
Dazu kann die powershell mithilfe von `powershell Start-process powershell -verb runas` geöffnet werden.

Anschließend müssen alle Abhängigkeiten (dependencies) aus der  `requirements.txt` Datei installiert werden.

```
pip install -r requirements.txt
```

Skizze:
https://docs.google.com/presentation/d/1tU_qScvGnyEERLrD6Z0X-YCYnflQOo3yPUPEZRteLug/edit?usp=sharing
