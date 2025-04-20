declare
	p_item JSON;
	p_name text;
	p_last_name text;
	p_phone text;
	contact_id int;
	invalid_list TEXT[] = '{}';
begin
	for p_item in select * from json_array_elements(fromjsondata)
	loop
		p_name := p_item->>'имя';
		p_last_name := p_item->>'фамилия';
		p_phone := p_item->>'номер';

		if p_phone ~ '^\+7\d{10}$' then
			insert into contacts(first_name,last_name) values(p_name,p_last_name)
			RETURNING id INTO contact_id;

            INSERT INTO phone_numbers(contact_id, phone_number)
            VALUES (contact_id, p_phone);
		else
			invalid_phones := array_append(invalid_list, p_phone);
		end if;
	end loop;
	invalid_phones := invalid_list;
end;