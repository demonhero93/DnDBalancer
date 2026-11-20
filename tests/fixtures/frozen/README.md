# Snapshots congelados

Fichas congeladas para tests con valores exactos (regresiones con semilla
fija): `test_damage.py` (ogre, owlbear) y `test_hechizos_pj.py` (lich).

**No regenerar ni migrar**: cambiar estos JSON desajusta las aserciones
exactas (`abs=1e-9`, supervivientes, usos de acción). Si la API 2024 cambia,
regenerar exige recalcular los valores esperados a mano.
