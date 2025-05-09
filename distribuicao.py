#!/usr/bin/env python3
#!/usr/bin/env python3
import numpy as np
from scipy.stats import beta
from scipy.optimize import minimize

# Parâmetros desejados
mu_target = 3.65
sigma_target = 1.63
a, b = 0, 10
N_total = 1277  # total de pontos discretos

# Reescalar momentos para intervalo [0, 1]
mu_std = mu_target / (b - a)
var_std = (sigma_target / (b - a))**2

# Função objetivo para ajustar alpha e beta
# Novo objetivo: adiciona erro no percentil 6
def objective(params):
    alpha, beta_param = params
    if alpha <= 0 or beta_param <= 0:
        return np.inf
    mean_beta = alpha / (alpha + beta_param)
    var_beta = (alpha * beta_param) / ((alpha + beta_param)**2 * (alpha + beta_param + 1))
    cdf_6 = beta.cdf((6 - a) / (b - a), alpha, beta_param)
    return ((mean_beta - mu_std)**2 +
            (var_beta - var_std)**2 +
            (cdf_6 - 0.9106)**2)  # penalidade pelo desvio no percentil


# Ajuste dos parâmetros alpha e beta
res = minimize(objective, [2, 2], bounds=[(1e-5, None), (1e-5, None)])
alpha_fit, beta_fit = res.x

# Criar pontos discretos: 0.00, 0.25, ..., 10.00
x_vals = np.arange(a, b + 0.25, 0.25)

# Calcular densidade da Beta reparametrizada nesses pontos
dx = 0.25
cdf_left = beta.cdf((x_vals - dx/2 - a) / (b - a), alpha_fit, beta_fit)
cdf_right = beta.cdf((x_vals + dx/2 - a) / (b - a), alpha_fit, beta_fit)
probs = cdf_right - cdf_left

# Estimar número de pontos em cada valor
counts = np.round(probs * N_total).astype(int)

# Gravar resultado formatado
with open("distribuicao.dat", "w") as f:
    f.write(f"{'Participantes':>15} | {'Nota':^6} | {'Acertos':^8}\n")
    f.write("-"*35+"\n")
    for x_i, count_i in zip(x_vals, counts):
        acertos = int(round(x_i * 4))
        f.write(f"{count_i:15d} | {x_i:6.2f} | {acertos:^8d}\n")
