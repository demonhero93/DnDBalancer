"""Simulaciones repetidas y estadísticas."""
import math
import random
import statistics

from .combat import run_combat
from ..model.combatant import Combatant


def _percentil(valores: list, p: float) -> int | float:
    """Percentil por rango más cercano (p entre 0 y 100)."""
    if not valores:
        return 0
    ordenados = sorted(valores)
    posicion = max(1, math.ceil(p / 100 * len(ordenados)))
    return ordenados[posicion - 1]


def simulate(combatants: list[Combatant], n: int = 1000, seed: int | None = None) -> dict:
    rng = random.Random(seed)
    results = [run_combat(combatants, rng) for _ in range(n)]
    teams = {c.team for c in combatants}
    rounds = [r.rounds for r in results]
    hp_max = {c.name: c.max_hp for c in combatants}
    # Usos por acción (sumados en todos los combates) y objetivos por área.
    action_uses: dict[str, int] = {}
    area_hits: list[int] = []
    for r in results:
        for name, count in (getattr(r, "action_uses", None) or {}).items():
            action_uses[name] = action_uses.get(name, 0) + int(count)
        area_hits.extend(getattr(r, "area_targets_hit", None) or [])
    # Límite de uso de las acciones con uso limitado (vive en la acción).
    action_limits: dict[str, dict] = {}
    for c in combatants:
        for action in getattr(c, "actions", []) or []:
            usage = getattr(action, "usage", None)
            if usage is None:
                continue
            name = getattr(action, "name", "") or ""
            action_limits.setdefault(name, {
                "kind": getattr(usage.kind, "value", str(usage.kind)),
                "uses_max": usage.uses_max,
                "recharge_dice": usage.recharge_dice,
                "recharge_min": usage.recharge_min,
            })
    # Daño medio de combate por combatiente.
    damage_dealt_avg = {
        c.name: statistics.mean(r.damage_dealt.get(c.name, 0) for r in results)
        for c in combatants
    }
    damage_received_avg = {
        c.name: statistics.mean(r.damage_received.get(c.name, 0) for r in results)
        for c in combatants
    }
    # Condiciones: veces aplicada cada una y turnos perdidos por incapacitación.
    conditions_applied: dict[str, int] = {}
    turns_lost: dict[str, int] = {}
    escape_attempts: dict[str, int] = {}
    escape_successes: dict[str, int] = {}
    attacks_at_range = 0
    # Leyenda: acciones legendarias usadas, puntos gastados y resistencias.
    legendary_actions: dict[str, int] = {}
    legendary_points = 0
    legendary_resistances = 0
    for r in results:
        for name, count in (getattr(r, "conditions_applied", None) or {}).items():
            conditions_applied[name] = conditions_applied.get(name, 0) + int(count)
        for name, count in (getattr(r, "turns_lost_incapacitated", None) or {}).items():
            turns_lost[name] = turns_lost.get(name, 0) + int(count)
        for name, count in (getattr(r, "escape_attempts", None) or {}).items():
            escape_attempts[name] = escape_attempts.get(name, 0) + int(count)
        for name, count in (getattr(r, "escape_successes", None) or {}).items():
            escape_successes[name] = escape_successes.get(name, 0) + int(count)
        attacks_at_range += int(getattr(r, "attacks_vs_at_range", 0) or 0)
        for name, count in (getattr(r, "legendary_actions_used", None) or {}).items():
            legendary_actions[name] = legendary_actions.get(name, 0) + int(count)
        legendary_points += int(getattr(r, "legendary_points_spent", 0) or 0)
        legendary_resistances += int(getattr(r, "legendary_resistances_used", 0) or 0)
    # Riesgo real y cola de distribución: PV mínimos por combate (los
    # registra el daño en rules.damage) y percentiles de rondas.
    pj_names = [c.name for c in combatants if c.team == "PJ"]
    min_frac: dict[str, list[float]] = {c.name: [] for c in combatants}
    grupo_frac: list[float] = []
    bajos_pj: dict[str, int] = {name: 0 for name in pj_names}
    any_downed = 0
    multi_downed = 0
    for r in results:
        mins = getattr(r, "min_hp", None) or {}
        fracs: dict[str, tuple[int, float]] = {}
        for c in combatants:
            valor = int(mins.get(c.name, r.survivors.get(c.name, 0)))
            frac = (valor / c.max_hp) if c.max_hp else 1.0
            min_frac[c.name].append(frac)
            fracs[c.name] = (valor, frac)
        if pj_names:
            grupo_frac.append(min(fracs[name][1] for name in pj_names))
            con_cero = sum(1 for name in pj_names if fracs[name][0] <= 0)
            any_downed += con_cero >= 1
            multi_downed += con_cero >= 2
            for name in pj_names:
                bajos_pj[name] += fracs[name][0] <= 0
    return {
        "n": n,
        "win_rate": {t: sum(r.winner == t for r in results) / n for t in teams},
        "draw_rate": sum(r.winner == "Empate" for r in results) / n,
        "rounds_avg": statistics.mean(rounds),
        "rounds_median": statistics.median(rounds),
        "rounds_max": max(rounds),
        "hp_left_avg": {c.name: statistics.mean(r.survivors[c.name] for r in results)
                        for c in combatants},
        "hp_max": hp_max,
        "hp_left_pct_avg": {
            c.name: (statistics.mean(r.survivors[c.name] for r in results)
                     / c.max_hp * 100) if c.max_hp else 0.0
            for c in combatants
        },
        # Estadísticas de uso de acciones y de áreas.
        "action_uses_avg": {name: total / n for name, total in action_uses.items()},
        "action_uses_total": action_uses,
        "action_limits": action_limits,
        "area_uses_total": len(area_hits),
        "area_targets_avg": statistics.mean(area_hits) if area_hits else 0.0,
        # Daño medio de combate (infligido y recibido) por combatiente.
        "damage_dealt_avg": damage_dealt_avg,
        "damage_received_avg": damage_received_avg,
        "teams": {c.name: c.team for c in combatants},
        # Condiciones (media de aplicaciones por combate) y turnos perdidos.
        "conditions_applied_avg": {name: total / n for name, total in conditions_applied.items()},
        "turns_lost_incapacitated_avg": {name: total / n for name, total in turns_lost.items()},
        # Escapes (intentos y aciertos por combate) y ataques a distancia.
        "escape_attempts_avg": {name: total / n for name, total in escape_attempts.items()},
        "escape_successes_avg": {name: total / n for name, total in escape_successes.items()},
        "attacks_vs_at_range_avg": attacks_at_range / n,
        # Leyenda (medias por combate).
        "legendary_actions_used_avg": {
            name: total / n for name, total in legendary_actions.items()
        },
        "legendary_actions_used_total": legendary_actions,
        "legendary_points_spent_avg": legendary_points / n,
        "legendary_resistances_used_avg": legendary_resistances / n,
        # Riesgo: PJ a 0 PV en algún momento del combate (por nombre y
        # combates con 1+ o 2+ PJ a la vez).
        "any_pj_downed_rate": any_downed / n,
        "multi_pj_downed_rate": multi_downed / n,
        "pj_downed_rate": {name: total / n for name, total in bajos_pj.items()},
        # Cola de PV mínimos (fracción del máximo): percentiles de grupo
        # (mínimo entre los PJ de cada combate) y P10 por combatiente.
        "hp_min_frac_p5": _percentil(grupo_frac, 5),
        "hp_min_frac_p10": _percentil(grupo_frac, 10),
        "hp_min_frac_p25": _percentil(grupo_frac, 25),
        "hp_min_frac_p10_by_name": {
            name: _percentil(fracs, 10) for name, fracs in min_frac.items()
        },
        # Variabilidad de rondas: desviación típica y percentiles.
        "rounds_std": statistics.pstdev(rounds),
        "rounds_p10": _percentil(rounds, 10),
        "rounds_p50": _percentil(rounds, 50),
        "rounds_p90": _percentil(rounds, 90),
        "rounds_p99": _percentil(rounds, 99),
    }


def print_report(stats: dict) -> None:
    print(f"\n=== {stats['n']} simulaciones ===")
    for team, rate in stats["win_rate"].items():
        print(f"Victorias {team}: {rate:.1%}")
    print(f"Empates: {stats['draw_rate']:.1%}")
    print(f"Rondas: media {stats['rounds_avg']:.1f} | mediana {stats['rounds_median']} "
          f"| máx {stats['rounds_max']}")
    for name, hp in stats["hp_left_avg"].items():
        max_hp = (stats.get("hp_max") or {}).get(name, 0)
        pct = (hp / max_hp * 100) if max_hp else 0.0
        print(f"HP medio restante de {name}: {hp:.1f} ({pct:.1f}% de {max_hp})")

    # Daño medio de combate, separado en PJ y monstruos.
    equipos = stats.get("teams") or {}
    print("\nDaño medio de combate:")
    for team, etiqueta in (("PJ", "PJ"), ("NPC", "Monstruos")):
        miembros = [name for name, equipo in equipos.items() if equipo == team]
        if not miembros:
            continue
        print(f"  {etiqueta}:")
        for name in miembros:
            infligido = (stats.get("damage_dealt_avg") or {}).get(name, 0.0)
            recibido = (stats.get("damage_received_avg") or {}).get(name, 0.0)
            print(f"    {name}: {infligido:.1f} infligido | {recibido:.1f} recibido")

    if stats.get("area_uses_total"):
        print(f"Áreas por combate: {stats['area_uses_total'] / stats['n']:.2f} "
              f"| objetivos medios por área: {stats['area_targets_avg']:.2f}")

    condiciones = stats.get("conditions_applied_avg") or {}
    if condiciones:
        print("Condiciones (media de aplicaciones por combate):")
        for name, avg in sorted(condiciones.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {name}: {avg:.2f}")
    perdidos = stats.get("turns_lost_incapacitated_avg") or {}
    if perdidos:
        print("Turnos perdidos por incapacitación (media):")
        for name, avg in sorted(perdidos.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f"  {name}: {avg:.2f}")

    intentos = stats.get("escape_attempts_avg") or {}
    if intentos:
        print("Intentos de escape (media por combate):")
        for name, avg in sorted(intentos.items(), key=lambda kv: (-kv[1], kv[0])):
            exitos = (stats.get("escape_successes_avg") or {}).get(name, 0.0)
            print(f"  {name}: {avg:.2f} intentos | {exitos:.2f} exitos")
    if stats.get("attacks_vs_at_range_avg"):
        print(f"Ataques contra objetivos a distancia: {stats['attacks_vs_at_range_avg']:.2f} por combate")

    acciones_legendarias = stats.get("legendary_actions_used_avg") or {}
    if acciones_legendarias:
        print("Acciones legendarias (media de usos por combate):")
        for name, avg in sorted(acciones_legendarias.items(),
                                key=lambda kv: (-kv[1], kv[0])):
            print(f"  {name}: {avg:.2f}")
        print(f"Puntos legendarios gastados: {stats.get('legendary_points_spent_avg', 0.0):.2f} "
              f"por combate")
        print(f"Resistencias legendarias gastadas: "
              f"{stats.get('legendary_resistances_used_avg', 0.0):.2f} por combate")

    # Métricas clave de dificultad: riesgo, cola de PV mínimos y rondas.
    pj = [name for name, equipo in equipos.items() if equipo == "PJ"]
    if pj:
        print(f"\n=== Dificultad: métricas clave (n={stats['n']}) ===")
        print("Riesgo")
        desglose = " | ".join(
            f"{name} {(stats.get('pj_downed_rate') or {}).get(name, 0.0) * 100:.1f} %"
            for name in pj)
        print(f"  {'Algún PJ a 0 PV:':<27}"
              f"{stats.get('any_pj_downed_rate', 0.0) * 100:.1f} %   ({desglose})")
        print(f"  {'2+ PJ a 0 PV:':<27}"
              f"{stats.get('multi_pj_downed_rate', 0.0) * 100:.1f} %")
        print("PV mínimos (fracción del máximo)")
        print(f"  {'Grupo  P5 / P10 / P25:':<27}"
              f"{stats.get('hp_min_frac_p5', 0.0):.2f} / "
              f"{stats.get('hp_min_frac_p10', 0.0):.2f} / "
              f"{stats.get('hp_min_frac_p25', 0.0):.2f}")
        por_nombre = stats.get("hp_min_frac_p10_by_name") or {}
        for name in pj:
            print(f"  {name + ' P10:':<27}{por_nombre.get(name, 0.0):.2f}")
        print("Rondas")
        print(f"  {'media / std:':<27}{stats['rounds_avg']:.1f} / "
              f"{stats.get('rounds_std', 0.0):.1f}")
        print(f"  {'P10 / P50 / P90 / P99:':<27}{stats.get('rounds_p10', 0)} / "
              f"{stats.get('rounds_p50', 0)} / {stats.get('rounds_p90', 0)} / "
              f"{stats.get('rounds_p99', 0)}")
