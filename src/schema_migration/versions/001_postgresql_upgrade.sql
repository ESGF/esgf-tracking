create schema esgf_subscription ;
create table esgf_subscription.subscribers (email varchar(256), key varchar(64), value varchar(256)); 
create table esgf_subscription.keys (key varchar(64), project varchar(64));
insert into esgf_subscription.keys values ('experiment', 'default');
insert into esgf_subscription.keys values ('variable', 'default');


