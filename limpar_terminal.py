#!/usr/bin/env python3
"""
Script para limpar terminal e logs
"""

import os
import sys

def limpar_terminal():
    """Limpa o terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("🧹 Terminal limpo!")
    print("📁 Logs antigos removidos")
    print("-" * 30)

def limpar_logs():
    """Remove logs antigos"""
    logs_dir = 'logs'
    if os.path.exists(logs_dir):
        for file in os.listdir(logs_dir):
            if file.endswith('.log'):
                os.remove(os.path.join(logs_dir, file))
        print("🗑️  Logs antigos removidos")

if __name__ == '__main__':
    limpar_terminal()
    limpar_logs()
    print("✅ Limpeza concluída!") 