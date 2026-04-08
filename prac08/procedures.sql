CREATE OR REPLACE PROCEDURE upsert_contact(p_name TEXT, p_phone TEXT)
AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
    ELSE
        INSERT INTO phonebook (name, phone) VALUES (p_name, p_phone);
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_many(p_names TEXT[], p_phones TEXT[])
AS $$
DECLARE i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        IF length(p_phones[i]) >= 5 THEN
            CALL upsert_contact(p_names[i], p_phones[i]);
        ELSE
            RAISE NOTICE 'Skipping: invalid phone for user %', p_names[i];
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE delete_contact(p_val TEXT)
AS $$
BEGIN
    DELETE FROM phonebook WHERE name = p_val OR phone = p_val;
END;
$$ LANGUAGE plpgsql;