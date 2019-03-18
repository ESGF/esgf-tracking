create schema esgf_subscription ;
create table esgf_subscription.subscribers (id integer primary key, email varchar(256), keyname varchar(64), valuename varchar(256)); 
create table esgf_subscription.keys (keyname varchar(64) primary key, project varchar(64));
insert into esgf_subscription.keys values ('experiment', 'default');
insert into esgf_subscription.keys values ('variable', 'default');


