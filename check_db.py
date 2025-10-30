#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pour vérifier les tables de la base de données
"""
import sqlite3

DATABASE = 'feelflix.db'

def show_tables():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    
    # Récupérer toutes les tables
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    
    print("\n" + "="*70)
    print("📊 TABLES DE LA BASE DE DONNÉES FEELFLIX")
    print("="*70)
    
    for table_name in tables:
        table = table_name[0]
        c.execute(f"PRAGMA table_info({table})")
        columns = c.fetchall()
        
        print(f"\n✓ Table: {table.upper()}")
        print("-" * 70)
        
        # Afficher les colonnes
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            constraint = "NOT NULL" if col[3] else "NULL"
            print(f"  • {col_name:<25} {col_type:<15} {constraint}")
        
        # Compter les lignes
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"\n  📈 Lignes: {count}")
    
    conn.close()
    print("\n" + "="*70 + "\n")

if __name__ == '__main__':
    try:
        show_tables()
    except Exception as e:
        print(f"❌ Erreur: {e}")
