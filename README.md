🧵 Suavização do Movimento da Extrusora 3D com Splines

Este projeto simula e analisa o movimento de uma extrusora de impressora 3D utilizando splines cúbicas para suavizar a trajetória e evitar movimentos bruscos. 
Ele considera jerk e massa da extrusora para estimar o risco de ghosting (vibrações que afetam a qualidade da impressão).


🎯 Objetivo
- Modelar o movimento da extrusora em 2D de forma suave.
- Avaliar o comportamento de velocidade, aceleração, jerk e força do jerk ao longo do tempo.
- Estimar o risco de ghosting com base em limites definidos para jerk e força.
- Ajudar na compreensão de como parâmetros físicos influenciam a qualidade da impressão 3D.


⚙️ Parâmetros Configuráveis
Você pode modificar os seguintes parâmetros no início do código:
| Parâmetro           | Descrição                                   | Exemplo           |
| ------------------- | ------------------------------------------- | ----------------- |
| `massa`             | Massa da extrusora (em kg)                  | `0.5`             |
| `tempo_total`       | Duração da simulação (em segundos)          | `5.0`             |
| `num_pontos`        | Número de pontos de controle                | `6`               |
| `jerk_limite`       | Limite de jerk (mm/s³)                      | `10`              |
| `forca_jerk_limite` | Limite de força de jerk (Newtons)           | `5`               |
| `x`, `y`            | Posição dos pontos de controle (trajetória) | `np.array([...])` |


📈 Saídas do Código
O código gera 5 gráficos:
1. Trajetória 2D da extrusora (X vs Y)
2. Velocidade
3. Aceleração
4. Jerk efetivo vs limite
5. Força do jerk vs limite

E também imprime:
- % do tempo com jerk acima do limite
- % do tempo com força do jerk acima do limite


📦 Requisitos
- Python 3.x
- numpy
- matplotlib
- scipy


🧠 Como o Jerk e a Massa Afetam a Impressão?
- Jerk alto pode causar ghosting (ondas ou vibrações em peças).
- Massa maior → mais força necessária para mudar a velocidade → maior risco de vibração.
- Esse modelo ajuda a encontrar o equilíbrio entre rapidez e qualidade.

🧪 Exemplo de Uso
Execute o script com:  python extrusora_spline.py

🧰 Autoria: 
Este projeto foi desenvolvido como parte de um trabalho de Matemática Computacional, com o objetivo de aplicar conceitos de cálculo, física e computação para resolver um problema real no contexto de impressão 3D. Alunos: Maria Eduarda de Carvalho e Tiago Godart

