MaxAmmo()
{
	Primary = self getCurrentWeapon();
	Lethal = self getCurrentOffHand();
	self giveMaxAmmo(Primary);
	self giveMaxAmmo(Lethal);
}