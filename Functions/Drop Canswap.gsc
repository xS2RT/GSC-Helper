randomGun() // Credits to @MatrixMods
{
	self endon("disconnect");
	level endon("game_ended");
	self.gun = "";
	while (self.gun == "")
	{
		id = random(level.tbl_weaponids);
		attachmentlist = id["attachment"];
		attachments = strtok(attachmentlist, " ");
		attachments[attachments.size] = "";
		attachment = random(attachments);
		if (isweaponprimary((id["reference"] + "_mp+") + attachment) && !checkGun(id["reference"] + "_mp+" + attachment))
			self.gun = (id["reference"] + "_mp+") + attachment;
	}
	return self.gun;
}

checkGun(weap)
{
	self.allWeaps = [];
	self.allWeaps = self getWeaponsList();
	foreach (weapon in self.allWeaps)
	{
		if (isSubStr(weapon, weap))
			return 1;
	}
	return 0;
}

DropCan()
{
	weap = randomGun();
	self giveWeapon(weap);
	wait 0.1;
	self dropItem(weap);
}