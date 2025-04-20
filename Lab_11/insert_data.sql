DECLARE
    user_id INT;
BEGIN
	SELECT id into user_id from contacts c where c.first_name = p_first_name and c.last_name = p_last_name;

	If found then
		update phone_numbers set phone_number = p_phone_number where contact_id = user_id;
	else
		insert into contacts (first_name, last_name) values(p_first_name, p_last_name) returning id into user_id;
		insert into phone_numbers (phone_number, contact_id) values(p_phone_number, user_id);
	END if;
		
END;