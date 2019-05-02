create schema esgf_subscription ;
create table esgf_subscription.subscribers (id serial primary key, email varchar(256), period integer) ;
create table esgf_subscription.terms (id serial primary key, subscribers_id integer, keyname varchar(64), valuename varchar(64)) ;

create index terms1 on esgf_subscription.terms (keyname, valuename);
create index terms2 on esgf_subscription.terms (subscribers_id) ;



