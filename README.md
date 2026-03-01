# mt5-mac-native-bridge
Native Python injection for MetaTrader 5 on macOS (Silicon/M1-M3). Solves critical Wine IPC &amp; Docker freezes on 'mt5.initialize()'. By hijacking MetaEditor with an Embedded Python &amp; .pth auto-launch, it runs a headless RPyC server inside the MT5 terminal memory, allowing ultra-fast algorithm trading without Docker.
