toggleCamo()
{
	randy = RandomIntRange( 1, 46 );
 	weaps = self getcurrentweapon();
 	self takeWeapon( weaps );
 	self giveWeapon( weaps, 0, randy);
 	self switchToWeapon( weaps );
}