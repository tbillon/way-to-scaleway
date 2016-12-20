CREATE EXTENSION "uuid-ossp";


CREATE TABLE task (
       uuid UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
       sub_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       upd_date TIMESTAMP DEFAULT NULL,
       status INTEGER DEFAULT 0, -- 0 pending, 1 started, 2 finished, 3 error
       dst_url VARCHAR(2083) DEFAULT NULL,
       src_url VARCHAR(2083) NOT NULL
);


CREATE OR REPLACE FUNCTION task_update_upd_date()
RETURNS trigger AS $$
BEGIN
	NEW.upd_date = CURRENT_TIMESTAMP;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER trigger_task_update_upd_date BEFORE UPDATE ON task FOR EACH ROW
       WHEN (NEW.status <> OLD.status) EXECUTE PROCEDURE  task_update_upd_date();
