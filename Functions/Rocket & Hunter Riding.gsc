toggleriding()
{
	if( !(IsDefined( self.rocketride )) )
	{
		self.rocketride = 1;
		self thread rocketride();
		self iprintln("Rocket & Hunter Riding: ^2ON^7");
	}
	else
	{
		self.rocketride = undefined;
		self iprintln("Rocket & Hunter Riding: ^1OFF^7");
		self notify( "stopRocketz" );
	}

}

rocketride()
{
	self endon( "stopRocketz" );
	self endon( "disconnect" );
	for(;;)
	{
	if( !(IsDefined( self.isridingrocket )) )
	{
		self waittill( "missile_fire", weapon, weapname );
		if( weapname == "missile_drone_projectile_mp" || weapname == "usrpg_mp" )
		{
			self.isridingrocket = 1;
			self.rocketlinker = modelspawner( weapon.origin + ( 0, 0, 5 ), "tag_origin" );
			self.rocketlinker linkto( weapon );
			self playerlinkto( self.rocketlinker );
			self thread jumpoffrocket( weapon );
		}
	}
	waitframe();
	}

}

jumpoffrocket( rocket )
{
	self endon( "stopRocketz" );
	while( IsDefined( rocket ) )
	{
		if( self jumpbuttonpressed() )
		{
			break;
		}
		waitframe();
	}
	self unlink();
	if( IsDefined( self.rocketlinker ) )
	{
		self.rocketlinker delete();
	}
	self.isridingrocket = undefined;

}

modelspawner( origin, model, angles, time )
{
	if( IsDefined( time ) )
	{
		wait time;
	}
	obj = spawn( "script_model", origin );
	obj setmodel( model );
	if( IsDefined( angles ) )
	{
		obj.angles = angles;
	}
	return obj;

}