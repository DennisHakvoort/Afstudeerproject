t-- !!! WARNING: THIS DESTROYS THE DATABASE, APPROACH WITH CAUTION !!!

-- We drop the database tables, triggers, functions, etc., start with a clean slate and such.
DROP TRIGGER IF EXISTS trigger_delete_outdated_distances ON documents;
DROP FUNCTION IF EXISTS delete_outdated_distances;
DROP TABLE IF EXISTS document_distance;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS last_update;

CREATE TABLE last_update
(
    last_update timestamp NOT NULL,
    CONSTRAINT pk_last_update
        PRIMARY KEY (last_update)
);

CREATE TABLE documents
(
    id                 VARCHAR      NOT NULL,
    body_raw           TEXT         NOT NULL,
    body_preprocessed  TEXT         NOT NULL,
    title_raw          TEXT         NOT NULL,
    title_preprocessed TEXT         NOT NULL,
    space              VARCHAR(255) NOT NULL,
    CONSTRAINT pk_document_id
        PRIMARY KEY (id)
);

CREATE TABLE document_distance
(
    document_id_1 VARCHAR NOT NULL,
    document_id_2 VARCHAR NOT NULL,
    distance      REAL    NOT NULL,
    CONSTRAINT pk_document_distance
        PRIMARY KEY (document_id_1, document_id_2),
    CONSTRAINT fk_document_distance_1
        FOREIGN KEY (document_id_1)
            REFERENCES documents (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE,
    CONSTRAINT fk_document_distance_2
        FOREIGN KEY (document_id_2)
            REFERENCES documents (id)
            ON DELETE CASCADE
            ON UPDATE CASCADE
);

INSERT INTO last_update (last_update)
    VALUES (to_timestamp(0));

CREATE FUNCTION delete_outdated_distances()
    RETURNS TRIGGER AS
$delete_outdated_distances$
BEGIN
    IF NEW.id IS NOT NULL THEN
        DELETE
        FROM document_distance
        WHERE document_id_1 = NEW.id
           OR document_id_2 = NEW.id;
    END IF;

    RETURN NEW;
END;
$delete_outdated_distances$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_delete_outdated_distances
    AFTER INSERT OR UPDATE
    ON documents
    FOR EACH ROW -- executes once of every row, so for every inserted row, the function is called once.
EXECUTE FUNCTION delete_outdated_distances()

