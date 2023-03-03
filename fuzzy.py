import numpy as np
import skfuzzy as fuzz


# import matplotlib.pyplot as plt


def get_reliability(distance, std_pct):
    x_dist = np.arange(0, 17500, 1)
    x_std = np.arange(0, 101, 1)
    x_rel = np.arange(0, 101, 1)

    # Genero le funzioni appartenenza fuzzy
    dist_lo = fuzz.trimf(x_dist, [0, 0, 6000])
    dist_md = fuzz.trimf(x_dist, [0, 6000, 12000])
    dist_hi = fuzz.trapmf(x_dist, [6000, 12000, 17500, 17500])
    std_lo = fuzz.trimf(x_std, [0, 0, 50])
    std_md = fuzz.trimf(x_std, [0, 50, 100])
    std_hi = fuzz.trimf(x_std, [50, 100, 100])
    rel_sl = fuzz.trimf(x_rel, [0, 0, 25])
    rel_lo = fuzz.trimf(x_rel, [0, 25, 50])
    rel_md = fuzz.trimf(x_rel, [25, 50, 75])
    rel_hi = fuzz.trimf(x_rel, [50, 75, 100])
    rel_sh = fuzz.trimf(x_rel, [75, 100, 100])

    """
    # Visualizzo gli universi e le funzioni di appartenenza
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))

    ax0.plot(x_dist, dist_lo, 'b', linewidth=2, label='Breve')
    ax0.plot(x_dist, dist_md, 'y', linewidth=2, label='Media')
    ax0.plot(x_dist, dist_hi, 'r', linewidth=2, label='Lunga')
    ax0.set_title('Distanza (m)')
    ax0.legend()

    ax1.plot(x_std, std_lo, 'b', linewidth=2, label='Bassa')
    ax1.plot(x_std, std_md, 'y', linewidth=2, label='Media')
    ax1.plot(x_std, std_hi, 'r', linewidth=2, label='Alta')
    ax1.set_title('Deviazione standard (%)')
    ax1.legend()

    ax2.plot(x_rel, rel_sl, 'b', linewidth=2, label='Molto '
                                                    'bassa')
    ax2.plot(x_rel, rel_lo, 'g', linewidth=2, label='Bassa')
    ax2.plot(x_rel, rel_md, 'y', linewidth=2, label='Media')
    ax2.plot(x_rel, rel_hi, 'm', linewidth=2, label='Alta')
    ax2.plot(x_rel, rel_sh, 'r', linewidth=2, label='Molto alta')
    ax2.set_title('Affidabilità (%)')
    ax2.legend()

    # Disabilito assi superiore e destro
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    """

    # Abbiamo bisogno dell'attivazione delle nostre funzioni di appartenenza fuzzy a questi valori
    dist_level_lo = fuzz.interp_membership(x_dist, dist_lo, distance)
    dist_level_md = fuzz.interp_membership(x_dist, dist_md, distance)
    dist_level_hi = fuzz.interp_membership(x_dist, dist_hi, distance)

    std_pct_level_lo = fuzz.interp_membership(x_std, std_lo, std_pct)
    std_pct_level_md = fuzz.interp_membership(x_std, std_md, std_pct)
    std_pct_level_hi = fuzz.interp_membership(x_std, std_hi, std_pct)

    """
    R1: Se la distanza è lunga e la percentuale di deviazione standard è alta, 
        allora l'affidabilità del percorso sarà molto bassa
    R2: Se la distanza è media e la percentuale di deviazione standard è alta 
        oppure se la distanza è lunga e la percentuale di deviazione standard 
        è media, allora l'affidabilità del percorso sarà bassa
    R3: Se la distanza è media e la percentuale di deviazione standard è media,
        allora l'affidabilità del percorso sarà media
    R4: Se la distanza è media e la percentuale di deviazione standard è
        bassa oppure se la distanza è breve e la percentuale di deviazione
        standard è media, allora l'affidabilità del percorso sarà alta
    R5: Se la distanza è breve o la percentuale di deviazione standard è
    bassa, allora l'affidabilità del percorso sarà molto alta
    """

    # R1
    active_rule1 = np.fmin(dist_level_hi, std_pct_level_hi)
    rel_activation_sl = np.fmin(np.resize(active_rule1, 101), rel_sl)

    # R2
    active_rule2 = np.fmax(np.fmin(dist_level_md, std_pct_level_hi), np.fmin(dist_level_hi, std_pct_level_md))
    rel_activation_lo = np.fmin(np.resize(active_rule2, 101), rel_lo)

    # R3
    active_rule3 = np.fmin(dist_level_md, std_pct_level_md)
    rel_activation_md = np.fmin(np.resize(active_rule3, 101), rel_md)

    # R4
    active_rule4 = np.fmax(np.fmin(dist_level_md, std_pct_level_lo), np.fmin(dist_level_lo, std_pct_level_md))
    rel_activation_hi = np.fmin(np.resize(active_rule4, 101), rel_hi)

    # R5
    active_rule5 = np.fmax(dist_level_lo, std_pct_level_lo)
    rel_activation_sh = np.fmin(np.resize(active_rule5, 101), rel_sh)

    rel0 = np.zeros_like(x_rel)

    """
    # Visualizzo il grado di attivazione
    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.fill_between(x_rel, rel0, rel_activation_sh, facecolor='b', alpha=0.7)
    ax0.plot(x_rel, rel_sh, 'b', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_rel, rel0, rel_activation_lo, facecolor='g', alpha=0.7)
    ax0.plot(x_rel, rel_lo, 'g', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_rel, rel0, rel_activation_md, facecolor='y', alpha=0.7)
    ax0.plot(x_rel, rel_md, 'y', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_rel, rel0, rel_activation_hi, facecolor='m', alpha=0.7)
    ax0.plot(x_rel, rel_hi, 'm', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_rel, rel0, rel_activation_sh, facecolor='r', alpha=0.7)
    ax0.plot(x_rel, rel_sh, 'r', linewidth=0.5, linestyle='--')
    ax0.set_title('Output funzione di appartenenza')

    # Disabilito assi superiore e destro
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    """

    # Aggrego tutte le cinque funzioni di appartnenza di output insieme
    aggregated = np.fmax(rel_activation_sl,
                         np.fmax(rel_activation_lo,
                                 np.fmax(rel_activation_md,
                                         np.fmax(rel_activation_hi,
                                                 rel_activation_sh))))

    # Calcolo il risultato defuzzificato
    rel_pct = fuzz.defuzz(x_rel, aggregated, 'centroid')
    rel_activation = fuzz.interp_membership(x_rel, aggregated, rel_pct)  # for plot

    """
    # Visualizzo il risultato defuzzificato
    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.plot(x_rel, rel_sl, 'b', linewidth=0.5, linestyle='--')
    ax0.plot(x_rel, rel_lo, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(x_rel, rel_md, 'y', linewidth=0.5, linestyle='--')
    ax0.plot(x_rel, rel_hi, 'm', linewidth=0.5, linestyle='--')
    ax0.plot(x_rel, rel_sh, 'r', linewidth=0.5, linestyle='--')
    ax0.fill_between(x_rel, rel0, aggregated, facecolor='Orange', alpha=0.7)
    ax0.plot([rel_pct, rel_pct], [0, rel_activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Appartenenza aggregata e risultato (linea)')

    # Disabilito assi superiore e destro
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.show()
    """

    return rel_pct
