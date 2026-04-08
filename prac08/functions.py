CREATE OR REPLACE FUNCTION find_contacts(ptrn TEXT)
RETURNS TABLE (res_name TEXT, res_phone TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone FROM phonebook
    WHERE name ILIKE '%' || ptrn || '%' OR phone LIKE '%' || ptrn || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_paged(p_limit INT, p_offset INT)
RETURNS TABLE (res_name TEXT, res_phone TEXT) AS $$
BEGIN
    RETURN QUERY 
    SELECT name, phone FROM phonebook
    ORDER BY name 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;