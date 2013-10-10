create table octorsync_status (
    distro_name     text primary key not null,
    lasy_rsync_time date,
    rsync_status    text
);
