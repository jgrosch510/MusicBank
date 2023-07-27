BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `setlists` (
	`rec_num`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`rec_id`	TEXT,
	`band`	TEXT,
	`artist_key`	TEXT,
	`show_key`	TEXT,
	`show_date`	TEXT,
	`venue`	TEXT,
	`city`	TEXT,
	`state_abbr`	TEXT,
	`set_1`	TEXT,
	`set_2`	TEXT,
	`set_3`	TEXT,
	`comment`	TEXT,
	`last_update`	TEXT,
	`show_year`	TEXT,
	`show_user_id`	TEXT
);
CREATE INDEX IF NOT EXISTS `show_key` ON `setlists` (
	`show_key`
);
CREATE INDEX IF NOT EXISTS `rec_id` ON `setlists` (
	`rec_id`
);
COMMIT;
