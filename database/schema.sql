CREATE EXTENSION "uuid-ossp";


CREATE TABLE task (
       uuid UUID PRIMARY KEY DEFAULT uuid_generate_v1mc(),
       sub_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
       dst_url VARCHAR(2083) DEFAULT NULL,
       src_url VARCHAR(2083) NOT NULL,
       title VARCHAR(100) DEFAULT NULL
);
