doTeleport()
{
	self.weapon = self getCurrentWeapon();
	self giveWeapon( "killstreak_remote_turret_mp" );
	self switchToWeapon( "killstreak_remote_turret_mp" );
	self beginLocationSelection( "map_mortar_selector" );
	self.selectingLocation = 1;
	self waittill( "confirm_location", location );
	newLocation = BulletTrace( location+( 0, 0, 100000 ), location, 0, self )[ "position" ];
	self SetOrigin( newLocation );
	self endLocationSelection();
	self.selectingLocation = undefined;
	self iprintln("Teleported!");
	self takeWeapon("killstreak_remote_turret_mp");
}