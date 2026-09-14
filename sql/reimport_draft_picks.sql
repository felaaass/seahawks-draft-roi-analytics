USE seahawks_draft_analytics;

DROP TABLE IF EXISTS draft_picks;

CREATE TABLE draft_picks (
    season INT,
    `round` INT,
    pick INT,
    team VARCHAR(10),
    pfr_player_id VARCHAR(20),
    pfr_player_name VARCHAR(100),
    position VARCHAR(10),
    age INT,
    `to` INT,
    allpro INT,
    probowls INT,
    seasons_started INT,
    w_av DECIMAL(6,1),
    dr_av DECIMAL(6,1),
    games INT,
    college VARCHAR(100),
    pfr_id VARCHAR(20),
    player_name VARCHAR(100),
    pos VARCHAR(10),
    school VARCHAR(100),
    ht DECIMAL(5,1),
    wt DECIMAL(6,1),
    forty DECIMAL(5,2),
    bench INT,
    vertical DECIMAL(5,1),
    broad_jump DECIMAL(6,1),
    cone DECIMAL(5,2),
    shuttle DECIMAL(5,2),
    known_outcome VARCHAR(10),
    round_median_wav DECIMAL(6,1),
    draft_status VARCHAR(20),
    hit INT,
    is_seahawks INT,
    hit_probability DECIMAL(8,6)
);

LOAD DATA LOCAL INFILE 'C:/temp/nfl_draft_scored_1999_2025.csv'
INTO TABLE draft_picks
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

SELECT COUNT(*) FROM draft_picks;