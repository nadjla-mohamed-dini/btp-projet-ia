from app import map_value_to_mood

cases = [
    (0, 'très triste'),
    (15, 'peur'),
    (40, 'énervé'),
    (50, 'neutre'),
    (60, 'heureux'),
    (80, 'joyeux'),
    (95, 'amoureux')
]

for val, expected in cases:
    res = map_value_to_mood(val)
    assert res == expected, f"Value {val}: expected {expected}, got {res}"

print('All mapping tests passed')