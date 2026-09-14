
CREATE DATABASE IF NOT EXISTS seahawks_draft_analytics;
USE seahawks_draft_analytics;

CREATE OR REPLACE VIEW team_round_efficiency AS
SELECT
    team,
    `round`,
    COUNT(*) AS total_picks,
    SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) AS hits,
    ROUND(SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS hit_rate_pct,
    ROUND(AVG(w_av), 1) AS avg_w_av
FROM draft_picks
WHERE draft_status IN ('hit', 'bust')
GROUP BY team, `round`;

WITH team_hit_rate AS (
    SELECT
        team,
        COUNT(*) AS total_picks,
        SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) AS hits,
        ROUND(SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS hit_rate_pct
    FROM draft_picks
    WHERE draft_status IN ('hit', 'bust')
    GROUP BY team
    HAVING COUNT(*) >= 50
)
SELECT
    team,
    total_picks,
    hits,
    hit_rate_pct,
    RANK() OVER (ORDER BY hit_rate_pct DESC) AS league_rank
FROM team_hit_rate
ORDER BY league_rank;

SELECT
    season,
    `round`,
    pick,
    pfr_player_name,
    w_av,
    ROUND(AVG(w_av) OVER (ORDER BY season ROWS BETWEEN 4 PRECEDING AND CURRENT ROW), 1) AS media_movel_5anos,
    ROUND(AVG(w_av) OVER (PARTITION BY `round`), 1) AS media_do_round
FROM draft_picks
WHERE team = 'SEA'
ORDER BY season, `round`;

CREATE OR REPLACE VIEW seahawks_vs_league_by_round AS
SELECT
    l.`round`,
    l.hit_rate_pct AS liga_hit_rate_pct,
    s.hit_rate_pct AS seahawks_hit_rate_pct,
    ROUND(s.hit_rate_pct - l.hit_rate_pct, 1) AS diferenca_pct
FROM
    (SELECT `round`, ROUND(SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS hit_rate_pct
     FROM draft_picks WHERE draft_status IN ('hit', 'bust') GROUP BY `round`) l
JOIN
    (SELECT `round`, ROUND(SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) / COUNT(*) * 100, 1) AS hit_rate_pct
     FROM draft_picks WHERE draft_status IN ('hit', 'bust') AND team = 'SEA' GROUP BY `round`) s
ON l.`round` = s.`round`
ORDER BY l.`round`;


SELECT
    CASE WHEN season < 2010 THEN 'Pre-Schneider (1999-2009)' ELSE 'Era Schneider (2010-2025)' END AS era,
    COUNT(*) AS total_picks,
    ROUND(SUM(CASE WHEN draft_status = 'hit' THEN 1 ELSE 0 END) /
          NULLIF(SUM(CASE WHEN draft_status IN ('hit', 'bust') THEN 1 ELSE 0 END), 0) * 100, 1) AS hit_rate_pct,
    ROUND(AVG(w_av), 1) AS avg_w_av
FROM draft_picks
WHERE team = 'SEA'
GROUP BY era;