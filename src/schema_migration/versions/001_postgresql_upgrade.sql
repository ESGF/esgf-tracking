create schema esgf_subscription ;

create table esgf_subscription.subscribers (id serial primary key,  user_id integer 
	, period integer) ;

create table esgf_subscription.terms (id serial primary key, subscribers_id integer, keyname varchar(64), valuename varchar(64), 
FOREIGN KEY (subscribers_id)
REFERENCES esgf_subscription.subscribers(id)
ON DELETE CASCADE
) ;

create index terms1 on esgf_subscription.terms (keyname, valuename);
create index terms2 on esgf_subscription.terms (subscribers_id) ;



