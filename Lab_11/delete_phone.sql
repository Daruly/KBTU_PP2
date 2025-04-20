begin
	if exists(select 1 from phone_numbers where phone_number = p_phone_number) then
		delete from phone_numbers where phone_number = p_phone_number;
		results := 'номер удален';
	else
		results := 'номера нет';
	end if;
end;