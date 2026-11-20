"""Métricas de riesgo y percentiles de engine.stats (post-proceso puro)."""
from dnd_sim import Abilities, Attack, PlayerCharacter
from dnd_sim.engine.stats import _percentil, simulate


def _duelo():
    return [
        PlayerCharacter(name="A", max_hp=12, ac=11, abilities=Abilities(str=12),
                        attacks=[Attack("Golpe", "1d6", ability="str")]),
        PlayerCharacter(name="B", max_hp=12, ac=11, abilities=Abilities(str=12),
                        attacks=[Attack("Golpe", "1d6", ability="str")]),
    ]


def test_percentil_es_rango_mas_cercano():
    assert _percentil([], 50) == 0
    assert _percentil([7], 50) == 7
    # ceil(0.5 * 4) = 2 → segunda posición de la lista ordenada.
    assert _percentil([1, 2, 3, 4], 50) == 2
    assert _percentil([1, 2, 3, 4], 100) == 4
    assert _percentil([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 10) == 1


def test_metricas_de_riesgo_y_percentiles_son_coherentes():
    stats = simulate(_duelo(), n=50, seed=11)
    assert stats["rounds_std"] >= 0
    assert 0.0 <= stats["multi_pj_downed_rate"] <= stats["any_pj_downed_rate"] <= 1.0
    assert set(stats["pj_downed_rate"]) == {"A", "B"}
    assert (stats["hp_min_frac_p5"]
            <= stats["hp_min_frac_p10"]
            <= stats["hp_min_frac_p25"])
    assert 0.0 <= stats["hp_min_frac_p10_by_name"]["A"] <= 1.0
    assert (stats["rounds_p10"] <= stats["rounds_p50"]
            <= stats["rounds_p90"] <= stats["rounds_p99"])
    assert stats["rounds_p99"] <= stats["rounds_max"]
