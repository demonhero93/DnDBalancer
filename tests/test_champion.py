"""Tests de tablas y registro de Champion (Campeón, PHB 2024).

Las tablas viven en A1; el registro y ``apply_champion`` en A2; el
rango crítico ampliado en A3; Remarkable Athlete en A4; Additional
Fighting Style en A5 y Heroic Rally en A6. Los rasgos sin modelo
(Heroic Warrior, Defy Death, movimiento tras crítico) se congelan como
dato sin efecto.
"""

from __future__ import annotations

import random
from types import SimpleNamespace

import pytest

from dnd_sim import Abilities, Attack, Monster, PlayerCharacter, apply_class
from dnd_sim.core.classes import (
    FIGHTER_STYLES,
    champion_crit_threshold,
    heroic_rally_amount,
)
from dnd_sim.core.enums import AttackRange
from dnd_sim.rules.classes import CLASSES, apply_fighter
from dnd_sim.rules.classes.fighter import (
    ChampionFeatures,
    FighterFeatures,
    apply_cavalier,
    apply_champion,
)

# --- A1: tablas --------------------------------------------------------------


def test_el_rango_critico_de_champion_es_20_19_o_18_segun_el_nivel():
    assert champion_crit_threshold(1) == 20
    assert champion_crit_threshold(2) == 20
    assert champion_crit_threshold(3) == 19
    assert champion_crit_threshold(14) == 19
    assert champion_crit_threshold(15) == 18
    assert champion_crit_threshold(18) == 18
    assert champion_crit_threshold(20) == 18


def test_la_cura_de_heroic_rally_es_5_mas_el_mod_de_con_sin_bajar_de_cero():
    assert heroic_rally_amount(5) == 10
    assert heroic_rally_amount(3) == 8
    assert heroic_rally_amount(0) == 5
    assert heroic_rally_amount(-5) == 0
    assert heroic_rally_amount(-9) == 0


# --- A2: esqueleto, registro y datos sin efecto ------------------------------

def _abilities(**kwargs) -> Abilities:
    base = dict(str=16, dex=14, con=16, int=10, wis=12, cha=10)
    base.update(kwargs)
    return Abilities(**base)


def _pj(**kwargs) -> PlayerCharacter:
    defaults = dict(
        name="Camila", max_hp=70, ac=15, level=5, abilities=_abilities(),
        attacks=[Attack("Espada larga", "1d8", ability="str")],
    )
    defaults.update(kwargs)
    return PlayerCharacter(**defaults)


def _trait(pj) -> ChampionFeatures:
    for trait in pj.traits:
        if isinstance(trait, ChampionFeatures):
            return trait
    raise AssertionError("falta ChampionFeatures")


def _champion(level: int = 5, fighting_style: str | None = None,
              **kwargs) -> tuple:
    pj = _pj(level=level)
    apply_fighter(pj, level=level, fighting_style=fighting_style)
    trait = apply_champion(pj, level=level, **kwargs)
    return pj, trait


def _firmas(pj) -> tuple:
    """(rasgos, acciones, salvaciones, habilidades, CA) para comparar."""
    return (
        [type(t).__name__ for t in pj.traits],
        [type(a).__name__ for a in pj.actions],
        set(pj.save_proficiencies),
        set(pj.skill_proficiencies),
        pj.ac,
    )


def test_registro_champion_bajo_fighter():
    subclases = CLASSES["fighter"].subclasses
    assert "champion" in subclases
    sub = subclases["champion"]
    assert sub.class_name == "fighter"
    assert sub.min_level == 3


def test_apply_class_equivalente_a_apply_champion(monkeypatch):
    """Misma semilla en los dos RNG de creación: resultados idénticos."""
    import dnd_sim.rules.classes.fighter.features as fighter_mod
    import dnd_sim.rules.classes.fighter.subclasses.champion as champ_mod

    a, b = _pj(), _pj()
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(champ_mod, "_RNG_CREACION", random.Random(0))
    apply_class(a, "fighter", "champion", level=5)
    monkeypatch.setattr(fighter_mod, "_RNG_CREACION", random.Random(0))
    monkeypatch.setattr(champ_mod, "_RNG_CREACION", random.Random(0))
    apply_fighter(b)
    apply_champion(b, level=5)
    assert _firmas(a) == _firmas(b)
    assert isinstance(_trait(a), ChampionFeatures)
    assert isinstance(_trait(b), ChampionFeatures)


def test_apply_champion_sin_clase_guerrero_da_value_error():
    with pytest.raises(ValueError, match="Primero aplica la clase guerrero"):
        apply_champion(_pj(), level=5)


def test_apply_champion_por_debajo_del_nivel_3_da_value_error():
    with pytest.raises(ValueError, match=">= 3"):
        apply_class(_pj(level=2), "fighter", "champion")


def test_heroic_warrior_es_dato_sin_efecto():
    """Sin Inspiración Heroica en el modelo: solo el dato congelado."""
    pj, trait = _champion(level=10)
    assert trait.heroic_warrior is True
    # Ni salvaciones, habilidades ni CA cambian; no hay inspiración.
    assert not hasattr(pj, "inspiration")


def test_defy_death_es_dato_sin_efecto():
    """Sin salvaciones de muerte en el modelo: solo el dato congelado."""
    pj, trait = _champion(level=18)
    assert trait.defy_death is True
    # Un PJ a 0 PG muere o queda fuera: no existe el atributo.
    assert not hasattr(pj, "death_saves")


def test_sin_subclase_no_hay_rasgo_ni_datos_de_champion():
    pj = _pj()
    apply_fighter(pj, level=5)
    assert not any(isinstance(t, ChampionFeatures) for t in pj.traits)
    # Cero consulta: sin el rasgo nadie lleva los datos congelados.
    assert not any(hasattr(t, "heroic_warrior") for t in pj.traits)
    assert not any(hasattr(t, "defy_death") for t in pj.traits)


# --- A3: rango crítico ampliado ------------------------------------------------

def _parchea_d20(monkeypatch, valor: int) -> None:
    from dnd_sim.core.dice import D20Result
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(
        atk_mod, "roll_d20",
        lambda rng, mode: D20Result(value=valor, rolls=[valor], mode=mode))


def test_el_critico_con_19_impacta_aunque_no_alcance_la_ca(monkeypatch):
    _parchea_d20(monkeypatch, 19)
    pj, _ = _champion(level=5)
    enemigo = Monster("Toloso", max_hp=60, ac=40, abilities=_abilities())
    atk = Attack("Espada larga", "1d8", ability="str")
    from dnd_sim.engine.combat import attack as atk_mod

    log: list[str] = []
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), log=log)
    assert any("CRÍTICO" in line for line in log)
    assert enemigo.hp < enemigo.max_hp


def test_un_no_champion_con_19_falla_contra_la_misma_ca(monkeypatch):
    _parchea_d20(monkeypatch, 19)
    pj = _pj()
    apply_fighter(pj, level=5)
    enemigo = Monster("Toloso", max_hp=60, ac=40, abilities=_abilities())
    atk = Attack("Espada larga", "1d8", ability="str")
    from dnd_sim.engine.combat import attack as atk_mod

    log: list[str] = []
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), log=log)
    assert any("falla" in line for line in log)
    assert not any("CRÍTICO" in line for line in log)
    assert enemigo.hp == enemigo.max_hp


def test_el_rango_ampliado_a_18_solo_funciona_desde_el_nivel_15(monkeypatch):
    _parchea_d20(monkeypatch, 18)
    from dnd_sim.engine.combat import attack as atk_mod

    pj15, _ = _champion(level=15)
    alto = Monster("Alto", max_hp=60, ac=40, abilities=_abilities())
    log15: list[str] = []
    atk_mod.attack_roll(pj15, alto, Attack("Espada", "1d8", ability="str"),
                        random.Random(1), log=log15)
    assert any("CRÍTICO" in line for line in log15)

    pj3, _ = _champion(level=3)
    bajo = Monster("Bajo", max_hp=60, ac=40, abilities=_abilities())
    log3: list[str] = []
    atk_mod.attack_roll(pj3, bajo, Attack("Espada", "1d8", ability="str"),
                        random.Random(1), log=log3)
    assert any("falla" in line for line in log3)


def test_el_un_natural_sigue_fallen_do_para_un_champion(monkeypatch):
    _parchea_d20(monkeypatch, 1)
    pj, _ = _champion(level=15)
    enemigo = Monster("Cerdo", max_hp=60, ac=10, abilities=_abilities())
    atk = Attack("Espada larga", "1d8", ability="str")
    from dnd_sim.engine.combat import attack as atk_mod

    log: list[str] = []
    atk_mod.attack_roll(pj, enemigo, atk, random.Random(1), log=log)
    assert any("falla" in line for line in log)
    assert not any("CRÍTICO" in line for line in log)
    assert enemigo.hp == enemigo.max_hp


def test_los_dados_del_critico_se_doblan_con_el_rango_ampliado(monkeypatch):
    from dnd_sim.engine.combat import attack as atk_mod

    _parchea_d20(monkeypatch, 19)
    criticos: list[bool] = []
    original = atk_mod.roll_dice

    def espia(expr, rng, crit=False, **kw):
        criticos.append(bool(crit))
        return original(expr, rng, crit=crit, **kw)

    monkeypatch.setattr(atk_mod, "roll_dice", espia)
    pj, _ = _champion(level=3, fighting_style="Archery")
    enemigo = Monster("Blanco", max_hp=60, ac=40, abilities=_abilities())
    atk_mod.attack_roll(pj, enemigo, Attack("Espada", "1d8", ability="str"),
                        random.Random(1), log=[])
    assert criticos, "el daño no pasó por roll_dice"
    assert all(criticos)


def test_ataque_de_hechizo_no_usa_el_umbral_de_champion(monkeypatch):
    _parchea_d20(monkeypatch, 19)
    pj, _ = _champion(level=15)
    destello = Attack("Destello", "1d8", ability="int",
                      spell_attack=True)
    enemigo = Monster("Toloso", max_hp=60, ac=40, abilities=_abilities())
    from dnd_sim.engine.combat import attack as atk_mod

    log: list[str] = []
    atk_mod.attack_roll(pj, enemigo, destello, random.Random(1), log=log)
    assert any("falla" in line for line in log)
    assert not any("CRÍTICO" in line for line in log)


def test_warding_no_convierte_en_fallo_un_critico_por_rango_ampliado(
        monkeypatch):
    import dnd_sim.rules.classes.fighter.subclasses.cavalier as cav_mod
    from dnd_sim.engine.combat import attack as atk_mod

    monkeypatch.setattr(cav_mod, "pick", lambda rng, seq: seq[-1])
    monkeypatch.setattr(cav_mod, "roll_dice",
                        lambda expr, rng, crit=False: 8)
    monkeypatch.setattr(atk_mod, "roll_dice",
                        lambda expr, rng, crit=False: 3)
    _parchea_d20(monkeypatch, 19)
    atacante, _ = _champion(fighting_style="Archery")
    # Defensor Cavalier 7 con CA 40: sin rango ampliado el 19 no
    # entraría jamás; con él, crítico → Warding no lo convierte en fallo.
    defensor = _pj(name="Doris", max_hp=70)
    apply_fighter(defensor, level=7)
    apply_cavalier(defensor, level=7)
    defensor.ac = 40
    ctx = SimpleNamespace(round=1, actor=atacante, rng=random.Random(1),
                           combatants=[atacante, defensor], log=None)
    log: list[str] = []
    atk_mod.attack_roll(atacante, defensor,
                        Attack("Golpe", "1d6", ability="str"),
                        random.Random(1), log=log, ctx=ctx,
                        allow_friendly=True)
    assert any("CRÍTICO" in line for line in log)
    assert defensor.hp < defensor.max_hp


def test_sin_subclase_el_umbral_de_critico_es_20_sin_rng():
    from dnd_sim.rules.roll_modifiers import evaluar_d20, umbral_critico

    pj = _pj()
    apply_fighter(pj, level=5)
    atk = Attack("Espada larga", "1d8", ability="str")
    assert umbral_critico(pj, atk) == 20
    assert evaluar_d20(19, pj, atk) == (False, False)
    assert evaluar_d20(20, pj, atk) == (True, False)
    assert evaluar_d20(1, pj, atk) == (False, True)


def test_el_umbral_del_rasgo_es_19_o_18_y_20_para_hechizos():
    from dnd_sim.rules.roll_modifiers import umbral_critico

    pj3, _ = _champion(level=3)
    pj15, _ = _champion(level=15)
    atk = Attack("Espada larga", "1d8", ability="str")
    destello = Attack("Destello", "1d8", ability="int",
                      spell_attack=True)
    assert umbral_critico(pj3, atk) == 19
    assert umbral_critico(pj15, atk) == 18
    assert umbral_critico(pj15, destello) == 20


# --- A4: Remarkable Athlete ---------------------------------------------------

def test_la_iniciativa_tira_dos_d20_y_toma_el_mayor_solo_para_el_champion(
        monkeypatch):
    from dnd_sim.core.dice import RollMode
    from dnd_sim.engine.combat import encounter as enc_mod

    modos: list = []
    original = enc_mod.roll_d20

    def espia(rng, mode):
        modos.append(mode)
        return original(rng, mode)

    monkeypatch.setattr(enc_mod, "roll_d20", espia)
    pj, _ = _champion()
    enc_mod.roll_initiative([pj], random.Random(0))
    assert modos == [RollMode.ADVANTAGE]
    assert pj.initiative is not None


def test_sin_champion_la_iniciativa_consume_un_d20_por_combatiente(monkeypatch):
    from dnd_sim.engine.combat import encounter as enc_mod

    tiradas: list = []
    monkeypatch.setattr(enc_mod, "d20",
                        lambda rng: (tiradas.append(1), 10)[1])
    monkeypatch.setattr(
        enc_mod, "roll_d20",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("sin la subclase no se pide ventaja")))
    a, b = _pj(name="A"), _pj(name="B")
    enc_mod.roll_initiative([a, b], random.Random(0))
    assert len(tiradas) == 2  # un d20 por combatiente: RNG exacto


def test_ventaja_y_desventaja_de_iniciativa_se_anulan(monkeypatch):
    from dnd_sim.engine.combat import encounter as enc_mod

    class _Ambas:
        def ventaja_iniciativa(self):
            return True

        def desventaja_iniciativa(self):
            return True

    tiradas: list = []
    monkeypatch.setattr(enc_mod, "d20",
                        lambda rng: (tiradas.append(1), 10)[1])
    monkeypatch.setattr(
        enc_mod, "roll_d20",
        lambda *a, **k: (_ for _ in ()).throw(
            AssertionError("con ambas fuentes se tira normal")))
    pj, _ = _champion()
    pj.traits.append(_Ambas())
    enc_mod.roll_initiative([pj], random.Random(0))
    assert len(tiradas) == 1


def test_la_desventaja_de_iniciativa_tira_dos_d20_y_toma_el_menor(
        monkeypatch):
    from dnd_sim.core.dice import RollMode
    from dnd_sim.engine.combat import encounter as enc_mod

    class _Desventaja:
        def ventaja_iniciativa(self):
            return False

        def desventaja_iniciativa(self):
            return True

    modos: list = []
    original = enc_mod.roll_d20

    def espia(rng, mode):
        modos.append(mode)
        return original(rng, mode)

    monkeypatch.setattr(enc_mod, "roll_d20", espia)
    pj = _pj()
    pj.traits.append(_Desventaja())
    enc_mod.roll_initiative([pj], random.Random(0))
    assert modos == [RollMode.DISADVANTAGE]


def test_atletismo_recibe_ventaja_para_el_champion():
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.checks import skill_check

    pj, _ = _champion()
    res = skill_check(pj, "athletics", 15, random.Random(0))
    assert res.mode == RollMode.ADVANTAGE
    assert len(res.rolls) == 2


def test_las_demas_habilidades_no_reciben_ventaja_del_champion():
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.checks import skill_check

    pj, _ = _champion()
    res = skill_check(pj, "stealth", 15, random.Random(0))
    assert res.mode == RollMode.NORMAL
    assert len(res.rolls) == 1


def test_la_ventaja_de_atletismo_se_anula_con_desventaja():
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.checks import skill_check
    from dnd_sim.rules.conditions import Condition, apply_condition

    pj, _ = _champion()
    ctx = SimpleNamespace(round=1, combatants=[pj], rng=random.Random(1),
                           log=None)
    apply_condition(pj, Condition.POISONED, ctx)  # desventaja en pruebas
    res = skill_check(pj, "athletics", 15, random.Random(0))
    assert res.mode == RollMode.NORMAL
    assert len(res.rolls) == 1


def test_remarkable_athlete_no_concede_competencia_en_atletismo():
    pj = _pj()
    apply_fighter(pj, level=5)
    antes = set(pj.skill_proficiencies)
    apply_champion(pj, level=5)
    assert set(pj.skill_proficiencies) == antes


def test_sin_subclase_atletismo_tira_normal_sin_ventaja_ni_rng_extra():
    from dnd_sim.core.dice import RollMode
    from dnd_sim.rules.checks import skill_check

    pj = _pj()
    apply_fighter(pj, level=5)
    res = skill_check(pj, "athletics", 15, random.Random(0))
    assert res.mode == RollMode.NORMAL
    assert len(res.rolls) == 1


def test_moverse_tras_un_critico_es_dato_sin_efecto():
    # El modelo no tiene campo de velocidad: no hay nada que mover.
    pj, _ = _champion()
    assert not hasattr(pj, "speed")


# --- A5: Additional Fighting Style --------------------------------------------

def _fighter(pj) -> FighterFeatures:
    for trait in pj.traits:
        if isinstance(trait, FighterFeatures):
            return trait
    raise AssertionError("falta FighterFeatures")


def test_el_segundo_estilo_difiere_del_primero_y_esta_en_el_pool():
    pj, _ = _champion(level=7)
    f = _fighter(pj)
    assert f.estilos_extra
    segundo = f.estilos_extra[0]
    assert segundo != f.estilo
    assert segundo in FIGHTER_STYLES
    assert set(f.estilos) == {f.estilo, segundo}


def test_kwarg_explicito_de_estilo_adicional_valido():
    pj, _ = _champion(level=7, fighting_style="Archery",
                      additional_fighting_style="Defense")
    assert _fighter(pj).estilos_extra == ["Defense"]


def test_kwarg_que_repite_el_primero_da_value_error():
    with pytest.raises(ValueError, match="repite"):
        _champion(level=7, fighting_style="Archery",
                  additional_fighting_style="Archery")


def test_kwarg_estilo_inventado_da_value_error():
    with pytest.raises(ValueError, match="no es un Estilo"):
        _champion(level=7, additional_fighting_style="Silly Style")


def test_los_dos_estilos_funcionan_a_la_ves():
    pj, _ = _champion(level=7, fighting_style="Dueling",
                      additional_fighting_style="Defense")
    f = _fighter(pj)
    # Defense: +1 CA al aplicarse el segundo estilo.
    assert pj.ac == 16
    # Dueling: +2 a daño cuerpo a cuerpo a una mano.
    objetivo = Monster("Bobo", max_hp=60, ac=10, abilities=_abilities())
    daño = f.extra_attack_damage(
        pj, objetivo, AttackRange.MELEE,
        atk=Attack("Espada", "1d8", ability="str"))
    assert daño == 2


def test_defense_como_primero_no_duplica_la_ca():
    pj, _ = _champion(level=7, fighting_style="Defense")
    f = _fighter(pj)
    assert pj.ac == 16  # +1 una sola vez: el segundo nunca es Defense
    assert f.estilos_extra[0] != "Defense"


def test_por_debajo_del_nivel_7_no_concede_estilo_adicional():
    pj, _ = _champion(level=6, fighting_style="Archery",
                      additional_fighting_style="Defense")
    f = _fighter(pj)
    assert f.estilos_extra == []
    assert pj.ac == 15


def test_misma_semilla_elige_el_mismo_segundo_estilo():
    a, _ = _champion(level=7, fighting_style="Archery",
                     rng=random.Random(0))
    b, _ = _champion(level=7, fighting_style="Archery",
                     rng=random.Random(0))
    assert _fighter(a).estilos_extra == _fighter(b).estilos_extra


def test_sin_subclase_no_hay_estilos_extra():
    pj = _pj()
    apply_fighter(pj, level=7, fighting_style="Archery")
    f = _fighter(pj)
    assert f.estilos_extra == []
    assert f.estilos == ("Archery",)
