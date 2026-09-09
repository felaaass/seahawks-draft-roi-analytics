# Seattle Seahawks Draft ROI Analytics

Análise de eficiência do Seattle Seahawks nas escolhas de draft (1999–2025), comparando o capital investido (posição do pick) com o retorno real de carreira dos jogadores, usando um modelo preditivo de hit/bust treinado com dados da liga inteira.

## Stack

- **Python** — extração via `nflreadpy`, tratamento de dados, modelo `xgboost`
- **SQL (MySQL)** — banco relacional com Views, CTEs e Window Functions
- **Excel** — validação via Power Query/ODBC
- **Power BI** — dashboard com Star Schema e DAX

## Metodologia

- Dados de draft (1999–2025) via `nflreadpy.load_draft_picks()`, combinados com dados de combine (`load_combine()`)
- Métrica de sucesso: **Weighted Approximate Value (w_av)**, comparada à mediana da própria rodada (round) — evita comparar picks de 1ª rodada com picks de 7ª injustamente
- Picks de 2021–2025 marcados como `em_avaliacao` (carreira ainda em andamento, sem rótulo definitivo de hit/bust)
- Modelo de classificação treinado com picks de **toda a liga** (1999–2020) para maior robustez estatística, depois aplicado à análise do Seahawks

## Nota técnica

Durante a extração, identificamos que o campo `career_av` (Career Approximate Value) estava retornando nulo para 100% dos registros — tanto na biblioteca `nfl_data_py` (descontinuada) quanto na `nflreadpy` (sucessora oficial), indicando uma falha upstream no pipeline de dados da nflverse/PFR. Pivotamos para o campo `w_av` (Weighted Approximate Value), que estava íntegro e é inclusive a métrica preferida por analistas de draft por ponderar produção por temporada em vez de valor bruto acumulado.

## Estrutura

```
01_extracao_tratamento_draft.py   # extração + tratamento (liga + Seahawks)
02_modelo_xgboost_draft.py        # modelo preditivo hit/bust (em construção)
requirements.txt
```

## Status

- [x] Etapa 1 — Extração e tratamento
- [ ] Etapa 2 — Modelo XGBoost
- [ ] Etapa 3 — Banco de dados MySQL
- [ ] Etapa 4 — Validação em Excel
- [ ] Etapa 5 — Dashboard Power BI