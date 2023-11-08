dropCurrentWeapon()
{
	weap = self getcurrentweapon();
	self dropitem(weap);
	if (isDefined(weap))
	{
		self dropitem(weap);
		self iprintln("Current weapon ^5dropped");
	}
	else
		self iprintln("No weapon to ^1drop");
}