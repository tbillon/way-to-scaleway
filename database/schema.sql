CREATE EXTENSION "uuid-ossp";


CREATE TABLE task (
       uuid UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
       sub_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       upd_date TIMESTAMP DEFAULT NULL,
       status INTEGER DEFAULT 0, -- 0 pending, 1 started, 2 finished, 3 error
       dst_url VARCHAR(2083) DEFAULT NULL,
       src_url VARCHAR(2083) NOT NULL
);
