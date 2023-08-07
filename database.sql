create table if not exists urls (
  id serial primary key,
  name varchar(255) not null unique,
  created_at date not null default current_date
);
create table if not exists url_checks (
  id serial primary key,
  url_id INT references urls (id) on delete cascade,
  status_code INT,
  h1 varchar(255),
  title varchar(255),
  description text, 
  created_at date not null default current_date
);
