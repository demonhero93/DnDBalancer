"""Subclase Arcane Archer (Arquero Arcano, XGE): registro, Lore y tablas."""
from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import arcane_shot_options_known, arcane_shot_uses
from dnd_sim.core.enums import AttackRange, parse_damage_type
from dnd_sim.core.proficiency import proficiency_bonus
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    ARCANE_SHOTS,
    ArcaneArcherFeatures,
    apply_arcane_archer,
)
from dnd_sim.rules.classes.fighter.subclasses.arcane_archer import (
    ARCANE_SHOTS_SIN_TIRADA,
    CurvingShotAction,
)
from dnd_sim.rules.conditions import Condition
from dnd_sim.rules.traits.base import AtaqueSustituido
from dnd_sim.model.actions import TurnResources


def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Legolas", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Arco corto", "1d6", ability="dex", range_type="ranged")],
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


def _trait(pj) -> ArcaneArcherFeatures:
    for trait in pj.traits:
        if isinstance(trait, ArcaneArcherFeatures):
            return trait
    raise AssertionError("falta ArcaneArcherFeatures")


# --- Registro y equivalencia --------------------------------------------------

def test_registro_arcane_archer_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    # Cambio esperado con Cavalier (2026-11-10, explicado en PASOS).
    # Cambio esperado con Champion (2026-11-11, explicado en PASOS):
    # la clave "champion" se añade al registro.
    # Cambio esperado con Psi Warrior (2026-11-12, explicado en PASOS):
    # la clave "psi_warrior" se añade al registro.
    # Cambio esperado con Rune Knight (2026-11-13, explicado en PASOS):
    # la clave "rune_knight" se añade al registro.
    # Cambio esperado con Samurai (2026-11-15, explicado en PASOS):
    # la clave "samurai" se añade al registro.
    # Cambio esperado con Eldritch Knight (2026-11-17, explicado en PASOS):
    # la clave "eldritch_knight" se añade al registro.
    assert set(subclases) == {"arcane_archer", "battle_master",
                              "cavalier", "champion", "eldritch_knight",
                              "psi_warrior", "rune_knight", "samurai"}
    sub = subclases["arcane_archer"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_arcane_archer(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    a = _pj()
    b = _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(aa_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "arcane_archer", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(aa_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b)
    apply_arcane_archer(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert _trait(a).opciones_conocidas == _trait(b).opciones_conocidas


def test_apply_arcane_archer_exige_la_clase_fighter():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_arcane_archer(_pj())


def test_arcane_archer_requiere_nivel_3():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "arcane_archer")


# --- Tablas -------------------------------------------------------------------

def test_tabla_de_opciones_conocidas_por_nivel():
    esperado = {1: 0, 2: 0, 3: 2, 6: 2, 7: 3, 9: 3, 10: 4, 14: 4,
                15: 5, 17: 5, 18: 6, 20: 6}
    assert {lvl: arcane_shot_options_known(lvl) for lvl in esperado} == esperado


def test_tabla_de_usos_de_arcane_shot_por_nivel():
    esperado = {1: 0, 2: 0, 3: 2, 14: 2, 15: 3, 20: 3}
    assert {lvl: arcane_shot_uses(lvl) for lvl in esperado} == esperado


# --- Opciones conocidas -------------------------------------------------------

def test_opciones_conocidas_segun_nivel():
    casos = {3: 2, 10: 4, 18: 6}
    for nivel, cuenta in casos.items():
        pj = _pj(level=nivel)
        apply_fighter(pj, level=nivel)
        trait = apply_arcane_archer(pj, level=nivel)
        assert len(trait.opciones_conocidas) == cuenta
        assert len(set(trait.opciones_conocidas)) == cuenta
        assert set(trait.opciones_conocidas) <= set(ARCANE_SHOTS)


def test_kwarg_de_opciones_explicitas_valido():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    elegidas = ("Grasping Arrow", "Shadow Arrow")
    trait = apply_arcane_archer(pj, level=3, arcane_shots=elegidas)
    assert trait.opciones_conocidas == list(elegidas)


def test_kwarg_de_opciones_invalidas_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="no es una opción de Arcane Shot"):
        apply_arcane_archer(pj, level=3,
                            arcane_shots=("Flecha inventada",
                                          "Grasping Arrow"))


def test_kwarg_con_recuento_equivocado_da_value_error():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    with pytest.raises(ValueError, match="se esperaban 2 opciones"):
        apply_arcane_archer(pj, level=3, arcane_shots=("Grasping Arrow",))


# --- Arcane Archer Lore -------------------------------------------------------

def test_arcane_archer_lore_da_competencia():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    trait = apply_arcane_archer(pj, level=3)
    assert trait.competencia in ("arcana", "nature")
    assert trait.competencia in pj.skill_proficiencies


def test_arcane_archer_lore_guarda_el_truco_como_dato():
    pj = _pj(level=3)
    apply_fighter(pj, level=3)
    trait = apply_arcane_archer(pj, level=3)
    assert trait.truco in ("Prestidigitación", "Druidismo")


# --- Arcane Shot: usos y decisión ---------------------------------------------

class _RngSi:
    """randrange siempre el último elemento («si» / última opción)."""

    def randrange(self, n: int) -> int:
        return n - 1

    def random(self) -> float:
        return 1.0

    def randint(self, a: int, b: int) -> int:
        return b


class _RngNo:
    """randrange siempre 0 («no»)."""

    def randrange(self, n: int) -> int:
        return 0


class _RngExplota:
    """Cualquier acceso a RNG hace fallar el test."""

    def __getattr__(self, name: str):
        raise AssertionError(f"RNG no debería usarse: {name}")


class _RngFalla:
    """«si» a la decisión, última opción conocida y d20 siempre 1."""

    def randrange(self, n: int) -> int:
        return n - 1

    def random(self) -> float:
        return 1.0

    def randint(self, a: int, b: int) -> int:
        return a


def _arquero(level: int = 5, **kwargs):
    pj = _pj(level=level)
    apply_fighter(pj, level=level)
    trait = apply_arcane_archer(pj, level=level, **kwargs)
    return pj, trait


def _disparo(trait, rng, rango=AttackRange.RANGED, target=None, ctx=None):
    if target is None:
        # Las opciones tiran salvaciones: hace falta un combatiente real.
        target = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    # Decisión única antes de la tirada (paso 2b del motor).
    sustituido = trait.sustituir_ataque(
        trait.owner, target, atk, rango, ctx=ctx, rng=rng)
    if sustituido is not None:
        return sustituido  # Piercing/Seeking: sin daño en el hook
    return trait.extra_attack_damage(
        trait.owner, target, rango, ctx=ctx, rng=rng, atk=atk,
    )


def test_arcane_shot_crea_usos_por_nivel():
    assert _arquero(level=3)[1].arcane_shot_usage.uses_max == 2
    assert _arquero(level=15)[1].arcane_shot_usage.uses_max == 3


def test_arcane_shot_se_gasta_un_uso_al_aplicar():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    daño = _disparo(trait, _RngSi())
    assert daño > 0
    assert trait.arcane_shot_usage.uses_left == 1
    assert trait.shot_used_this_turn is True


def test_arcane_shot_se_aplica_una_sola_vez_por_turno():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    assert _disparo(trait, _RngSi()) > 0
    assert _disparo(trait, _RngSi()) == 0  # ya usado este turno
    assert trait.arcane_shot_usage.uses_left == 1  # solo un gasto


def test_arcane_shot_se_reinicia_en_on_turn_start():
    _, trait = _arquero(level=3)
    trait.shot_used_this_turn = True
    trait.on_turn_start(trait.owner)
    assert trait.shot_used_this_turn is False


def test_arcane_shot_sin_usos_cero_rng():
    _, trait = _arquero(level=3)
    trait.arcane_shot_usage.uses_left = 0
    assert _disparo(trait, _RngExplota()) == 0


def test_ataque_cuerpo_a_cuerpo_cero_rng():
    _, trait = _arquero(level=3)
    assert _disparo(trait, _RngExplota(), rango=AttackRange.MELEE) == 0


def test_arcane_shot_sin_rng_no_actua():
    _, trait = _arquero(level=3)
    assert _disparo(trait, None) == 0


def test_decision_no_no_gasta_uso():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    assert _disparo(trait, _RngNo()) == 0
    assert trait.arcane_shot_usage.uses_left == 2
    assert trait.shot_used_this_turn is False


def test_daño_de_arcane_shot_es_2d6_antes_del_18(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    vistas: list[str] = []

    def _dado(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return 12

    monkeypatch.setattr(aa_mod, "roll_dice", _dado)
    _, trait = _arquero(level=5, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    assert _disparo(trait, _RngSi()) == 12
    assert vistas == ["2d6"]


def test_daño_de_arcane_shot_es_4d6_desde_el_18(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    vistas: list[str] = []

    def _dado(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return 24

    monkeypatch.setattr(aa_mod, "roll_dice", _dado)
    # Pool de 6 opciones SOLO de impacto (RngSi elegiría la última del
    # pool completo, que ahora puede ser Piercing/Seeking).
    _, trait = _arquero(
        level=18,
        arcane_shots=("Banishing Arrow", "Beguiling Arrow", "Bursting Arrow",
                      "Enfeebling Arrow", "Grasping Arrow", "Shadow Arrow"),
    )
    assert _disparo(trait, _RngSi()) == 24
    assert vistas == ["4d6"]


def test_reset_restaura_los_usos_de_arcane_shot():
    _, trait = _arquero(level=3)
    trait.arcane_shot_usage.spend()
    trait.shot_used_this_turn = True
    trait.reset()
    assert trait.arcane_shot_usage.uses_left == 2
    assert trait.shot_used_this_turn is False


def test_ever_ready_shot_no_cambia_los_usos_al_empezar_un_combate():
    """Ever-Ready (10): cada combate empieza con los usos completos.

    Como el sim hace un combate por descanso, la ventaja (iniciativa
    con los usos ya llenos) es inalcanzable por diseño: se congela aquí
    y se reabre solo si hay más de un combate por descanso.
    """
    _, trait = _arquero(10)
    trait.arcane_shot_usage.spend()
    trait.arcane_shot_usage.spend()
    trait.reset()  # un combate nuevo = un día descansado
    assert (trait.arcane_shot_usage.uses_left
            == trait.arcane_shot_usage.uses_max)


# --- Decisión única antes de la tirada ---------------------------------------

def test_piercing_y_seeking_estan_en_el_pool():
    assert len(ARCANE_SHOTS) == 8
    assert "Piercing Arrow" in ARCANE_SHOTS
    assert "Seeking Arrow" in ARCANE_SHOTS
    assert set(ARCANE_SHOTS_SIN_TIRADA) == {"Piercing Arrow",
                                            "Seeking Arrow"}


def test_todas_las_opciones_del_pool_son_elegibles():
    """Con RngSi (última opción) cada una del pool puede salir elegida."""
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    for opcion in ARCANE_SHOTS:
        shots = tuple([x for x in ARCANE_SHOTS if x != opcion][:5]) + (opcion,)
        _, trait = _arquero(18, arcane_shots=shots)
        ctx = SimpleNamespace(combatants=[trait.owner, objetivo], round=1)
        res = trait.sustituir_ataque(
            trait.owner, objetivo, atk, AttackRange.RANGED,
            ctx=ctx, rng=_RngSi())
        if opcion in ARCANE_SHOTS_SIN_TIRADA:
            assert isinstance(res, AtaqueSustituido), opcion
            assert res.motivo == opcion
        else:
            assert res is None, opcion
            assert trait.opcion_pendiente == opcion


def test_decision_de_impacto_no_gasta_el_uso_hasta_impactar():
    _, trait = _arquero(3, arcane_shots=("Grasping Arrow", "Shadow Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner, objetivo], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    res = trait.sustituir_ataque(
        trait.owner, objetivo, atk, AttackRange.RANGED, ctx=ctx, rng=_RngSi())
    assert res is None
    assert trait.opcion_pendiente == "Shadow Arrow"
    assert trait.arcane_shot_usage.uses_left == 2  # sin gastar aún
    assert trait.shot_used_this_turn is False


def test_piercing_gasta_el_uso_al_sustituir():
    _, trait = _arquero(3, arcane_shots=("Grasping Arrow", "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner, objetivo], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    res = trait.sustituir_ataque(
        trait.owner, objetivo, atk, AttackRange.RANGED, ctx=ctx, rng=_RngSi())
    assert isinstance(res, AtaqueSustituido)
    assert res.motivo == "Piercing Arrow"
    assert trait.arcane_shot_usage.uses_left == 1
    assert trait.shot_used_this_turn is True
    assert trait.opcion_pendiente is None


def test_sustitucion_sin_elegibles_no_actua_para_piercing():
    """Pool solo P/S y sin enemigos: None SIN RNG y sin gastar uso."""
    _, trait = _arquero(3, arcane_shots=("Piercing Arrow", "Seeking Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    res = trait.sustituir_ataque(
        trait.owner, objetivo, atk, AttackRange.RANGED,
        ctx=ctx, rng=_RngExplota())
    assert res is None
    assert trait.arcane_shot_usage.uses_left == 2


def test_sustitucion_hace_un_solo_par_de_picks():
    class _Cuenta:
        def __init__(self):
            self.n = 0

        def randrange(self, n: int) -> int:
            self.n += 1
            return n - 1

    _, trait = _arquero(3, arcane_shots=("Grasping Arrow", "Shadow Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner, objetivo], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    rng = _Cuenta()
    res = trait.sustituir_ataque(
        trait.owner, objetivo, atk, AttackRange.RANGED, ctx=ctx, rng=rng)
    assert res is None
    assert trait.opcion_pendiente == "Shadow Arrow"
    assert rng.n == 2  # «si» + opción: un solo par de picks


def test_sustitucion_sin_usos_o_melee_cero_rng():
    _, trait = _arquero(3, arcane_shots=("Grasping Arrow", "Shadow Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner, objetivo], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    trait.arcane_shot_usage.uses_left = 0
    assert trait.sustituir_ataque(
        trait.owner, objetivo, atk, AttackRange.RANGED,
        ctx=ctx, rng=_RngExplota()) is None
    trait.arcane_shot_usage.uses_left = 2
    assert trait.sustituir_ataque(
        trait.owner, objetivo, atk, AttackRange.MELEE,
        ctx=ctx, rng=_RngExplota()) is None


# --- Piercing Arrow (sin tirada de ataque) -----------------------------------

def test_piercing_falla_la_salvacion_y_dana_arma_mas_1d6():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    res = _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx)
    assert isinstance(res, AtaqueSustituido)
    assert res.motivo == "Piercing Arrow"
    # Arma: 1d6(mín)=1 + mod DES(14)=2 → 3; extra 1d6(mín)=1 → 4.
    assert objetivo.hp == objetivo.max_hp - 4
    assert trait.arcane_shot_usage.uses_left == 1
    assert trait.shot_used_this_turn is True


def test_piercing_salvacion_exitosa_da_la_mitad():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    # d20 = 20: mitad de la arma ((6+2)//2=4) y del extra (6//2=3).
    _disparo(trait, _RngSi(), target=objetivo, ctx=ctx)
    assert objetivo.hp == objetivo.max_hp - 7


def test_piercing_los_dados_extra_se_tiran_una_sola_vez(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    vistas: list[str] = []

    def _dado(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return 12

    monkeypatch.setattr(aa_mod, "roll_dice", _dado)
    # Nivel 18 (6 opciones) con Piercing la última (RngSi la elige).
    pj, trait = _arquero(
        18, arcane_shots=("Banishing Arrow", "Beguiling Arrow",
                          "Bursting Arrow", "Enfeebling Arrow",
                          "Grasping Arrow", "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    vecino = Monster("Vecino", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo, vecino], round=1)
    res = _disparo(trait, _RngSi(), target=objetivo, ctx=ctx)
    assert isinstance(res, AtaqueSustituido)
    # Una sola tirada de extra compartida; la del arma va por engine.
    assert vistas == ["2d6"]


def test_piercing_k_uniforme_y_atacante_nunca_es_objetivo():
    class _RngK1:
        """«si» y última opción (n=2→1), k=1 (n=3→0 → elemento 1)."""

        def randrange(self, n: int) -> int:
            return 1 if n == 2 else 0

        def randint(self, a: int, b: int) -> int:
            return a

        def random(self) -> float:
            return 1.0

    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Piercing Arrow"))
    enemigos = [Monster(f"E{i}", max_hp=50, ac=15, abilities=_abilities())
                for i in range(3)]
    ctx = SimpleNamespace(combatants=[pj, *enemigos], round=1)
    _disparo(trait, _RngK1(), target=enemigos[0], ctx=ctx)
    danados = [c for c in enemigos if c.hp < c.max_hp]
    assert len(danados) == 1
    assert pj.hp == pj.max_hp  # el atacante nunca es objetivo


def test_piercing_k_se_limita_a_los_elegibles():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Piercing Arrow"))
    enemigos = [Monster(f"E{i}", max_hp=50, ac=15, abilities=_abilities())
                for i in range(2)]
    ctx = SimpleNamespace(combatants=[pj, *enemigos], round=1)
    # RngFalla pide k = 3 (último elemento de (1,2,3)): solo hay 2.
    _disparo(trait, _RngFalla(), target=enemigos[0], ctx=ctx)
    danados = [c for c in enemigos if c.hp < c.max_hp]
    assert len(danados) == 2


def test_piercing_sin_elegibles_no_gasta_uso():
    _, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                         "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    hecho = trait._ejecutar_piercing(
        objetivo, atk, AttackRange.RANGED, ctx, _RngExplota())
    assert hecho is False
    assert trait.arcane_shot_usage.uses_left == 2
    assert trait.shot_used_this_turn is False


def test_las_salvaciones_de_piercing_no_suman_cobertura(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    capturas = []
    original = aa_mod.apply_save_damage

    def _espia(source, target, effect, rolled_damage, ctx, on_resolved=None):
        salida = original(source, target, effect, rolled_damage, ctx,
                          on_resolved)
        capturas.append(salida)
        return salida

    monkeypatch.setattr(aa_mod, "apply_save_damage", _espia)
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx)
    assert len(capturas) == 1
    sr = capturas[0].save
    # Solo el mod de DES: sin cobertura, sin ventaja (una tirada).
    assert sr.bonus == objetivo.abilities.mod("dex")
    assert len(sr.rolls) == 1


def test_piercing_respeta_la_resistencia_al_perforante():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Piercing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    objetivo.resistances = {parse_damage_type("piercing")}
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged",
                 damage_type="piercing")
    trait.sustituir_ataque(
        pj, objetivo, atk, AttackRange.RANGED, ctx=ctx, rng=_RngFalla())
    # Arma 3 → resistencia → 1; extra 1 → resistencia → 0.
    assert objetivo.hp == objetivo.max_hp - 1


# --- Seeking Arrow (sin tirada de ataque) ------------------------------------

def test_seeking_falla_la_salvacion_y_dana_arma_mas_1d6():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Seeking Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    res = _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx)
    assert isinstance(res, AtaqueSustituido)
    assert res.motivo == "Seeking Arrow"
    assert objetivo.hp == objetivo.max_hp - 4
    assert trait.arcane_shot_usage.uses_left == 1


def test_seeking_salvacion_exitosa_da_la_mitad():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Seeking Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    _disparo(trait, _RngSi(), target=objetivo, ctx=ctx)
    # d20 = 20: mitad de la arma ((6+2)//2=4) y del extra (6//2=3).
    assert objetivo.hp == objetivo.max_hp - 7


def test_seeking_2d6_de_extra_desde_el_18(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    vistas: list[str] = []

    def _dado(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return 12

    monkeypatch.setattr(aa_mod, "roll_dice", _dado)
    pj, trait = _arquero(
        18, arcane_shots=("Banishing Arrow", "Beguiling Arrow",
                          "Bursting Arrow", "Enfeebling Arrow",
                          "Grasping Arrow", "Seeking Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    res = _disparo(trait, _RngSi(), target=objetivo, ctx=ctx)
    assert isinstance(res, AtaqueSustituido)
    assert vistas == ["2d6"]


def test_seeking_respeta_la_resistencia_a_la_fuerza():
    pj, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                          "Seeking Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    objetivo.resistances = {parse_damage_type("force")}
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=1)
    _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx)
    # Arma (corte, sin resistencia) 3 completa; extra de fuerza 1 → 0.
    assert objetivo.hp == objetivo.max_hp - 3


def test_seeking_sin_elegibles_no_gasta_uso():
    _, trait = _arquero(3, arcane_shots=("Grasping Arrow",
                                         "Seeking Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[trait.owner], round=1)
    atk = Attack("Arco corto", "1d6", ability="dex", range_type="ranged")
    hecho = trait._ejecutar_seeking(
        objetivo, atk, AttackRange.RANGED, ctx, _RngExplota())
    assert hecho is False
    assert trait.arcane_shot_usage.uses_left == 2
    assert trait.shot_used_this_turn is False


# --- Efectos de las opciones (salvaciones y condiciones) ----------------------

def test_cd_de_arcane_shot_es_8_mas_pb_mas_int():
    _, trait = _arquero(level=3)
    assert trait._cd() == (8 + proficiency_bonus(3)
                            + trait.owner.abilities.mod("int"))


def test_banishing_arrow_falla_la_salvacion_y_deja_incapacitado():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Banishing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    assert _disparo(trait, _RngFalla(), target=objetivo) > 0
    assert objetivo.conditions.has(Condition.INCAPACITATED)
    assert trait.arcane_shot_usage.uses_left == 1


def test_banishing_arrow_salvacion_exitosa_no_aplica_condicion():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Banishing Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    assert _disparo(trait, _RngSi(), target=objetivo) > 0  # d20 = 20
    assert not objetivo.conditions.has(Condition.INCAPACITATED)
    assert trait.arcane_shot_usage.uses_left == 1


def test_beguiling_arrow_hechiza_y_termina_si_el_aliado_ataca():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Beguiling Arrow"))
    aliado = _pj(name="Arwen")
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, aliado, objetivo], round=1)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    assert objetivo.conditions.has(Condition.CHARMED)
    assert trait.beguiling.get(objetivo.name) is aliado
    # El aliado ataca a la víctima: el hechizo termina y la marca cae.
    mods = SimpleNamespace(advantage_sources=[], disadvantage_sources=[])
    trait.grant_attack_modifiers(mods, aliado, objetivo,
                                 AttackRange.RANGED, ctx=ctx)
    assert not objetivo.conditions.has(Condition.CHARMED)
    assert trait.beguiling == {}


def test_beguiling_sin_aliados_no_tira_salvacion(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Beguiling Arrow"))
    enemigo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, enemigo], round=1)

    def _no_debe_llamarse(*args, **kwargs):
        raise AssertionError("sin aliados no se tira salvación")

    monkeypatch.setattr(aa_mod, "saving_throw", _no_debe_llamarse)
    assert _disparo(trait, _RngSi(), target=enemigo, ctx=ctx) > 0
    assert enemigo.conditions.instances == []
    assert trait.arcane_shot_usage.uses_left == 1  # el daño sí se aplicó


def test_enfeebling_arrow_marca_el_dano_mitigado():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Enfeebling Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=3)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    assert objetivo.state.enfeeble_hasta_ronda == {pj.name: 4}


def test_enfeebling_salvacion_exitosa_no_marca():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Enfeebling Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, objetivo], round=3)
    assert _disparo(trait, _RngSi(), target=objetivo, ctx=ctx) > 0
    assert objetivo.state.enfeeble_hasta_ronda == {}


def test_shadow_arrow_solo_tira_salvacion_sin_condicion():
    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Shadow Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    assert _disparo(trait, _RngFalla(), target=objetivo) > 0
    assert objetivo.conditions.instances == []
    assert trait.arcane_shot_usage.uses_left == 1


def test_bursting_arrow_dana_a_los_vecinos_sin_salvacion():
    pj, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                                "Bursting Arrow"))
    aliado = _pj(name="Arwen")
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    vecino = Monster("Vecino", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[pj, aliado, objetivo, vecino],
                          round=1)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    # 2d6 con el RNG del test (siempre 1s) = 2 de fuerza al vecino.
    assert vecino.hp == vecino.max_hp - 2
    # Sin salvación ni condición; el aliado no recibe nada.
    assert objetivo.conditions.instances == []
    assert vecino.conditions.instances == []
    assert aliado.hp == aliado.max_hp
    assert trait.arcane_shot_usage.uses_left == 1


def test_bursting_sin_vecinos_no_tira_dados_extra(monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.arcane_archer as aa_mod

    _, trait = _arquero(level=3, arcane_shots=("Grasping Arrow",
                                               "Bursting Arrow"))
    objetivo = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    ctx = SimpleNamespace(combatants=[_pj(), objetivo], round=1)
    vistas: list[str] = []
    original = aa_mod.roll_dice

    def _espia(expr, rng, *args, **kwargs):
        vistas.append(expr)
        return original(expr, rng, *args, **kwargs)

    monkeypatch.setattr(aa_mod, "roll_dice", _espia)
    assert _disparo(trait, _RngFalla(), target=objetivo, ctx=ctx) > 0
    # Solo el daño base del shot: sin vecinos no hay tirada de 2d6 extra.
    assert vistas == ["2d6"]


def test_reset_borra_las_marcas_de_beguiling():
    _, trait = _arquero(level=3)
    trait.beguiling["Blanco"] = object()
    trait.reset()
    assert trait.beguiling == {}


def test_la_marca_de_enfeebling_mitiga_por_ronda():
    from dnd_sim.core.combat_state import CombatState

    estado = CombatState()
    assert estado.enfeeble_mitiga(1) is False
    estado.enfeeble_hasta_ronda["Legolas"] = 4
    assert estado.enfeeble_mitiga(3) is True
    assert estado.enfeeble_mitiga(4) is True
    assert estado.enfeeble_mitiga(5) is False
    assert estado.enfeeble_mitiga(None) is False


def test_el_motor_mitiga_el_dano_con_la_marca_de_enfeebling(monkeypatch):
    import random

    from dnd_sim.core.dice import D20Result, RollMode
    from dnd_sim.engine.combat import attack as atk_mod

    atk = Attack("Hacha de batalla", "1d12", ability="str")
    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=15, rolls=[15],
                                    mode=RollMode.NORMAL))
    monkeypatch.setattr(atk_mod, "roll_dice", lambda *a, **k: 10)

    pj = _pj()
    sin_marca = Monster("Muñeco", max_hp=100, ac=10, abilities=_abilities(),
                        attacks=[])
    atk_mod.attack_roll(pj, sin_marca, atk, random.Random(1),
                        ctx=SimpleNamespace(round=1,
                                            combatants=[pj, sin_marca]))
    pj.state.enfeeble_hasta_ronda["Arquero"] = 99
    con_marca = Monster("Muñeco", max_hp=100, ac=10, abilities=_abilities(),
                        attacks=[])
    atk_mod.attack_roll(pj, con_marca, atk, random.Random(1),
                        ctx=SimpleNamespace(round=1,
                                            combatants=[pj, con_marca]))

    esperado = 10 + pj.abilities.mod("str")  # dado fijo + mod FUE
    assert sin_marca.hp == sin_marca.max_hp - esperado
    assert con_marca.hp == con_marca.max_hp - esperado // 2


# --- Magic Arrow y Curving Shot (7) ------------------------------------------

def _arco(magical: bool = False, name: str = "Arco corto") -> Attack:
    atk = Attack(name, "1d6", ability="dex",
                 range_type=AttackRange.RANGED)
    atk.magical = magical
    return atk


def _curving(pj) -> CurvingShotAction:
    for accion in pj.actions:
        if isinstance(accion, CurvingShotAction):
            return accion
    raise AssertionError("falta CurvingShotAction")


def _ctx_curving(pj, rng, enemigos) -> SimpleNamespace:
    return SimpleNamespace(actor=pj, rng=rng,
                           combatants=[pj, *enemigos], log=None)


def test_magic_arrow_vuelve_magico_el_arco_desde_el_nivel_7():
    pj, _ = _arquero(7)
    assert pj.attacks and all(atk.magical for atk in pj.attacks)


def test_magic_arrow_no_toca_armas_que_no_sean_arcos():
    pj = _pj(level=7,
             attacks=[Attack("Hacha de batalla", "1d12", ability="str")])
    apply_fighter(pj, level=7)
    apply_arcane_archer(pj, level=7)
    assert not pj.attacks[0].magical


def test_magic_arrow_solo_desde_el_7_y_acepta_nombres_en_ingles():
    pj5, _ = _arquero(6)
    assert not any(atk.magical for atk in pj5.attacks)
    pj = _pj(level=7, attacks=[
        Attack("Longbow", "1d8", ability="dex",
               range_type=AttackRange.RANGED)])
    apply_fighter(pj, level=7)
    apply_arcane_archer(pj, level=7)
    assert pj.attacks[0].magical


def test_curving_marca_el_fallo_con_arco_magico():
    pj, trait = _arquero(7)
    atk = _arco(magical=True)
    blanco = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    trait.after_attack_roll(pj, blanco, atk, False)
    assert trait.curving_atk is atk
    assert trait.curving_contra == "Blanco"


def test_curving_no_marca_acierto_melee_sin_magia_o_antes_del_7():
    pj, trait = _arquero(7)
    blanco = Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())
    trait.after_attack_roll(pj, blanco, _arco(magical=True), True)
    assert trait.curving_atk is None
    trait.after_attack_roll(pj, blanco, _arco(magical=False), False)
    assert trait.curving_atk is None
    melee = Attack("Daga", "1d4", ability="str")
    melee.magical = True
    trait.after_attack_roll(pj, blanco, melee, False)
    assert trait.curving_atk is None
    pj5, trait5 = _arquero(6)
    trait5.after_attack_roll(pj5, blanco, _arco(magical=True), False)
    assert trait5.curving_atk is None


def test_accion_curving_se_anade_desde_el_nivel_7():
    pj5, _ = _arquero(5)
    assert not any(isinstance(a, CurvingShotAction) for a in pj5.actions)
    pj7, _ = _arquero(7)
    assert any(isinstance(a, CurvingShotAction) for a in pj7.actions)


def test_curving_can_use_requiere_bonus_libre():
    pj, trait = _arquero(7)
    trait.curving_atk = _arco(magical=True)
    trait.curving_contra = "Blanco"
    enemigos = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities()),
                Monster("Otro", max_hp=50, ac=15, abilities=_abilities())]
    recursos = TurnResources(bonus_action_used=True)
    assert not _curving(pj).can_use(
        recursos, _ctx_curving(pj, _RngExplota(), enemigos))


def test_curving_sin_otro_enemigo_cero_rng():
    pj, trait = _arquero(7)
    trait.curving_atk = _arco(magical=True)
    trait.curving_contra = "Blanco"
    solo = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())]
    assert not _curving(pj).can_use(
        TurnResources(), _ctx_curving(pj, _RngExplota(), solo))


def test_curving_sin_marca_cero_rng():
    pj, _ = _arquero(7)
    enemigos = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities()),
                Monster("Otro", max_hp=50, ac=15, abilities=_abilities())]
    assert not _curving(pj).can_use(
        TurnResources(), _ctx_curving(pj, _RngExplota(), enemigos))


def test_curving_decision_no_no_re_tira():
    pj, trait = _arquero(7)
    trait.curving_atk = _arco(magical=True)
    trait.curving_contra = "Blanco"
    enemigos = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities()),
                Monster("Otro", max_hp=50, ac=15, abilities=_abilities())]
    assert not _curving(pj).can_use(
        TurnResources(), _ctx_curving(pj, _RngNo(), enemigos))


def test_curving_can_use_si_con_la_decision_si():
    pj, trait = _arquero(7)
    trait.curving_atk = _arco(magical=True)
    trait.curving_contra = "Blanco"
    enemigos = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities()),
                Monster("Otro", max_hp=50, ac=15, abilities=_abilities())]
    assert _curving(pj).can_use(
        TurnResources(), _ctx_curving(pj, _RngSi(), enemigos))


def test_curving_re_tira_contra_otro_enemigo(monkeypatch):
    pj, trait = _arquero(7)
    atk = _arco(magical=True)
    trait.curving_atk = atk
    trait.curving_contra = "Blanco"
    enemigos = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities()),
                Monster("Otro", max_hp=50, ac=15, abilities=_abilities())]
    registrados = []
    monkeypatch.setattr(
        "dnd_sim.engine.combat.attack_roll",
        lambda a, t, k, r, log=None, ctx=None: registrados.append((a, t, k)),
    )
    _curving(pj).execute(_ctx_curving(pj, random.Random(1), enemigos))
    assert len(registrados) == 1
    assert registrados[0][0] is pj
    assert registrados[0][1].name == "Otro"
    assert registrados[0][2] is atk
    assert trait.curving_atk is None
    assert trait.curving_contra is None


def test_curving_execute_sin_otro_enemigo_no_llama_nada(monkeypatch):
    pj, trait = _arquero(7)
    trait.curving_atk = _arco(magical=True)
    trait.curving_contra = "Blanco"
    solo = [Monster("Blanco", max_hp=50, ac=15, abilities=_abilities())]

    def _no_llamar(*args, **kwargs):
        raise AssertionError("no debería re-tirar sin otro enemigo")

    monkeypatch.setattr("dnd_sim.engine.combat.attack_roll", _no_llamar)
    _curving(pj).execute(_ctx_curving(pj, _RngExplota(), solo))
    assert trait.curving_atk is not None  # la marca se conserva


def test_reset_borra_la_marca_de_curving():
    _, trait = _arquero(7)
    trait.curving_atk = _arco(magical=True)
    trait.curving_contra = "Blanco"
    trait.reset()
    assert trait.curving_atk is None
    assert trait.curving_contra is None


# --- Integración ---------------------------------------------------------------

def test_run_combat_con_arquero_es_reproducible():
    from dnd_sim.engine.combat import run_combat

    def _duelo():
        pj, _ = _arquero(7)
        enemigo = Monster(name="Muñeco", max_hp=150, ac=10,
                          abilities=_abilities(), attacks=[])
        return pj, enemigo

    pj1, enemigo1 = _duelo()
    res1 = run_combat([pj1, enemigo1], random.Random(4), verbose=True,
                      max_rounds=5)
    pj2, enemigo2 = _duelo()
    res2 = run_combat([pj2, enemigo2], random.Random(4), verbose=True,
                      max_rounds=5)
    assert res1.log == res2.log
    assert res1.action_uses == res2.action_uses
    assert enemigo1.hp == enemigo2.hp
    assert enemigo1.hp < enemigo1.max_hp  # el arquero sí ataca


def test_sin_subclase_no_se_ejecuta_codigo_de_arcane_archer(monkeypatch):
    from dnd_sim.engine.combat import run_combat
    from dnd_sim.rules.classes.fighter.subclasses import (
        arcane_archer as aa_mod,
    )

    def _revienta(*args, **kwargs):
        raise AssertionError(
            "Arcane Archer no debe ejecutarse sin la subclase")

    monkeypatch.setattr(aa_mod.ArcaneArcherFeatures,
                        "extra_attack_damage", _revienta)
    monkeypatch.setattr(aa_mod.ArcaneArcherFeatures,
                        "sustituir_ataque", _revienta)
    monkeypatch.setattr(aa_mod.ArcaneArcherFeatures,
                        "after_attack_roll", _revienta)
    monkeypatch.setattr(aa_mod.ArcaneArcherFeatures,
                        "grant_attack_modifiers", _revienta)
    pj = _pj(level=7)
    apply_fighter(pj, level=7)  # SIN subclase: los hooks no existen
    assert not any(isinstance(a, aa_mod.CurvingShotAction)
                   for a in pj.actions)
    enemigo = Monster(name="Muñeco", max_hp=150, ac=10,
                      abilities=_abilities(), attacks=[])
    run_combat([pj, enemigo], random.Random(1), max_rounds=3)
