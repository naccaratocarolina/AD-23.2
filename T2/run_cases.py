from mm1_epidemy import mm1_epidemy
from analisys import run_analisys

### Simulações Infinitas Não Deterministicas ###
# Caso 1: 
infinita_caso1 = mm1_epidemy(
  num_sims=20,
  tx_chegada=1,
  tx_saida=2,
  name='caso1',
  infinita=True,
)

# Caso 2:
infinita_caso2 = mm1_epidemy(
  num_sims=20,
  tx_chegada=2,
  tx_saida=4,
  name='caso2',
  infinita=True,
)

# Caso 3:
infinita_caso3 = mm1_epidemy(
  num_sims=20,
  tx_chegada=1.05,
  tx_saida=1,
  name='caso3',
  infinita=True,
)

# Caso 4:
infinita_caso4 = mm1_epidemy(
  num_sims=20,
  tx_chegada=1.10,
  tx_saida=1,
  name='caso4',
  infinita=True,
)

### Simulações Infinitas Deterministicas ###
# Caso 1: 
infinita_det_caso1 = mm1_epidemy(
  num_sims=20,
  tx_chegada=1,
  tx_saida=2,
  name='caso1',
  infinita=True,
  deterministico=True,
)

# Caso 2:
infinita_det_caso2 = mm1_epidemy(
  num_sims=20,
  tx_chegada=2,
  tx_saida=4,
  name='caso2',
  infinita=True,
  deterministico=True,
)

# Caso 3:
infinita_det_caso3 = mm1_epidemy(
  num_sims=20,
  tx_chegada=1.05,
  tx_saida=1,
  name='caso3',
  infinita=True,
  deterministico=True,
)

# Caso 4:
infinita_det_caso4 = mm1_epidemy(
  num_sims=20,
  tx_chegada=1.10,
  tx_saida=1,
  name='caso4',
  infinita=True,
  deterministico=True,
)

### Simulações Finitas Não Deterministicas ###
# Caso 1: 
finita_caso1 = mm1_epidemy(
  num_sims=100,
  tx_chegada=1,
  tx_saida=2,
  name='caso1',
)

# Caso 2:
finita_caso2 = mm1_epidemy(
  num_sims=100,
  tx_chegada=2,
  tx_saida=4,
  name='caso2',
)

# Caso 3:
finita_caso3 = mm1_epidemy(
  num_sims=100,
  tx_chegada=1.05,
  tx_saida=1,
  name='caso3',
)

# Caso 4:
finita_caso4 = mm1_epidemy(
  num_sims=100,
  tx_chegada=1.10,
  tx_saida=1,
  name='caso4',
)

### Simulações Finitas Deterministicas ###
# Caso 1: 
finita_det_caso1 = mm1_epidemy(
  num_sims=100,
  tx_chegada=1,
  tx_saida=2,
  name='caso1',
  deterministico=True,
)

# Caso 2:
finita_det_caso2 = mm1_epidemy(
  num_sims=100,
  tx_chegada=2,
  tx_saida=4,
  name='caso2',
  deterministico=True,
)

# Caso 3:
finita_det_caso3 = mm1_epidemy(
  num_sims=100,
  tx_chegada=1.05,
  tx_saida=1,
  name='caso3',
  deterministico=True,
)

# Caso 4:
finita_det_caso4 = mm1_epidemy(
  num_sims=100,
  tx_chegada=1.10,
  tx_saida=1,
  name='caso4',
  deterministico=True,
)

# Roda as simulacoes

infinita_caso1.run_mm1_epid()
infinita_caso2.run_mm1_epid()
infinita_caso3.run_mm1_epid()
infinita_caso4.run_mm1_epid()

infinita_det_caso1.run_mm1_epid()
infinita_det_caso2.run_mm1_epid()
infinita_det_caso3.run_mm1_epid()
infinita_det_caso4.run_mm1_epid()

# finita_caso1.run_mm1_epid()
# finita_caso2.run_mm1_epid()
# finita_caso3.run_mm1_epid()
# finita_caso4.run_mm1_epid()

# finita_det_caso1.run_mm1_epid()
# finita_det_caso2.run_mm1_epid()
# finita_det_caso3.run_mm1_epid()
# finita_det_caso4.run_mm1_epid()

run_analisys()
