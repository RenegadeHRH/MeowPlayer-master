create table if not exists musics
(
    ID         char(16)     not null,
    music_name varchar(128) null,
    aritists   varchar(512) null,
    refer_List varchar(128) not null,
    primary key (ID, refer_List)
);

create table if not exists playlists
(
    ID   char(16)     not null
        primary key,
    name varchar(128) null
);


