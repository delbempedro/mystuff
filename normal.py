#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

def main():
    # Entrada dos valores
    x = float(input("Digite o valor da média (x): "))
    y = float(input("Digite o valor do desvio padrão (y): "))
    z = float(input("Digite o valor do ponto a marcar (z): "))

    # Geração dos dados
    x_vals = np.linspace(x - 4*y, x + 4*y, 1000)
    y_vals = norm.pdf(x_vals, loc=x, scale=y)
    z_height = norm.pdf(z, loc=x, scale=y)

    # Criação da figura sem exibir
    plt.figure(figsize=(8, 5))
    plt.plot(x_vals, y_vals, label=f'N({x}, {y}²)', color='blue')
    plt.axvline(z, color='red', linestyle='--', label=f'z = {z}')
    plt.scatter([z], [z_height], color='red', zorder=5)
    plt.title('Distribuição Normal')
    plt.xlabel('Valor')
    plt.ylabel('Densidade de Probabilidade')
    plt.legend()
    plt.grid(True)

    # Salvando o gráfico
    plt.savefig("curva-de-notas.png")
    plt.close()

    print("Gráfico salvo como 'curva-de-notas.png'.")

if __name__ == "__main__":
    main()

