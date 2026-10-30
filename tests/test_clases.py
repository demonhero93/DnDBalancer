"""Registro de clases: apply_class (equivalencia con los apply sueltos)."""
from __future__ import annotations

import pytest

from dnd_sim import Abilities, Attack, PlayerCharacter, apply_class
from dnd_sim.rules.classes import (
    CLASSES,
    ClassDef,
    apply_barbarian,
    register_class,
)
from dnd_sim.rules.classes.barbarian.subclasses import (
    apply_ancestral_guardian,
    apply_battlerager,
)


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Thor", max_hp=80, ac=12, level=5, abilities=_abilities(),
        attacks=[Attack("Hacha de batalla", "1d12", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def test_apply_class_battlerager_equivalente_a_los_apply_suelto():
    a = _pj()
    b = _pj()
    apply_class(a, "barbarian", "battlerager")
    apply_barbarian(b)
    apply_battlerager(b)
    assert _firmas(a) == _firmas(b)


def test_apply_class_ancestral_equivalente_a_los_apply_suelto():
    a = _pj()
    b = _pj()
    apply_class(a, "barbarian", "ancestral-guardian")
    apply_barbarian(b)
    apply_ancestral_guardian(b)
    assert _firmas(a) == _firmas(b)


def test_apply_class_sin_subclase_equivalente_a_apply_barbarian():
    a = _pj()
    b = _pj()
    apply_class(a, "barbarian")
    apply_barbarian(b)
    assert _firmas(a) == _firmas(b)


def test_apply_class_normaliza_el_nombre():
    a = _pj()
    apply_class(a, "Barbarian", "Ancestral Guardian")
    nombres = [type(t).__name__ for t in a.traits]
    assert "AncestralGuardianFeatures" in nombres


def test_clase_inexistente_da_value_error():
    with pytest.raises(ValueError, match="Clase desconocida"):
        apply_class(_pj(), "guerrero")


def test_subclase_inexistente_da_value_error():
    with pytest.raises(ValueError, match="no es una subclase"):
        apply_class(_pj(), "barbarian", "no-existe")


def test_subclase_de_otra_clase_da_value_error():
    """Una subclase registrada no vale para otra clase."""
    register_class(ClassDef(name="claseficticia",
                            apply=lambda pj, **kw: None))
    try:
        with pytest.raises(ValueError, match="no es una subclase"):
            apply_class(_pj(), "claseficticia", "battlerager")
    finally:
        CLASSES.pop("claseficticia", None)


def test_nivel_insuficiente_da_value_error():
    with pytest.raises(ValueError, match="nivel >= 3"):
        apply_class(_pj(level=2), "barbarian", "battlerager")


def test_apply_subclase_sin_clase_previa_sigue_fallando():
    from dnd_sim.rules.classes.barbarian.subclasses import (
        apply_ancestral_guardian as apply_sub,
    )
    with pytest.raises(ValueError, match="apply_barbarian"):
        apply_sub(_pj())


def test_apply_class_reenvia_kwargs_a_la_clase():
    pj = _pj()
    apply_class(pj, "barbarian", "battlerager",
                skills=("athletics", "intimidation"), level=5)
    assert {"athletics", "intimidation"} <= pj.skill_proficiencies
    assert pj.level == 5
