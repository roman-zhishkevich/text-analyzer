#!/usr/bin/env python3
"""
Desktop Launcher for Text Analyzer
Starts Streamlit server and opens browser automatically
"""

import sys
import os
import webbrowser
import time
import subprocess
import socket
from pathlib import Path

def find_free_port():
    """Find a free port to run Streamlit on"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def main():
    """Launch the Streamlit app"""
    # Get the directory where the executable is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = Path(sys._MEIPASS)
    else:
        # Running as script
        base_path = Path(__file__).parent

    # Set up paths
    app_path = base_path / "src" / "app.py"
    
    # Find a free port
    port = find_free_port()
    
    print("🚀 Запуск Text Analyzer...")
    print(f"📍 Порт: {port}")
    
    # Start Streamlit in a subprocess
    env = os.environ.copy()
    env['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
    
    cmd = [
        sys.executable if not getattr(sys, 'frozen', False) else 'streamlit',
        'run',
        str(app_path),
        '--server.port', str(port),
        '--server.headless', 'true',
        '--server.address', 'localhost',
        '--browser.gatherUsageStats', 'false',
    ]
    
    try:
        # Start Streamlit
        process = subprocess.Popen(
            cmd,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait a bit for server to start
        time.sleep(3)
        
        # Open browser
        url = f'http://localhost:{port}'
        print(f"🌐 Открытие браузера: {url}")
        webbrowser.open(url)
        
        print("\n✅ Text Analyzer запущен!")
        print("📝 Приложение открыто в браузере")
        print("⚠️  Не закрывайте это окно!")
        print("🛑 Для остановки нажмите Ctrl+C\n")
        
        # Keep running
        process.wait()
        
    except KeyboardInterrupt:
        print("\n🛑 Остановка приложения...")
        process.terminate()
        process.wait()
        print("✅ Приложение остановлено")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        input("Нажмите Enter для выхода...")
        sys.exit(1)

if __name__ == "__main__":
    main()


