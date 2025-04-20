begin
	if exists(select 1 from contacts where first_name = p_first_name and last_name = p_last_name) then
		delete from contacts where first_name = p_first_name and last_name = p_last_name;
		results := 'чел удален';
	else
		results := 'не существует чела';
	end if;
end;