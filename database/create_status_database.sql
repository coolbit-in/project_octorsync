CREATE TABLE "octorsync_status" (
    "id" integer NOT NULL PRIMARY KEY,
    "distro_name" text NOT NULL UNIQUE,
    "last_rsync_time" text,
    "rsync_status" text NOT NULL
)
;