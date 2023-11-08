toggleUFO()
{
	if(self.UFO == "On")
	{
		self.UFO = "Off";
		self notify("StopUFO");
		self unlink();
	}
	else
	{
		self.UFO = "On";
		self thread doUFO();
	}
}

doUFO()
{
	self endon("StopUFO");
	self endon("death");
	if(isDefined(self.UFO)) self.UFO destroy();
	self.UFO = spawn("script_model",self.origin);
	self playerLinkTo(self.UFO);
	self closeMenu();
	self iPrintln("Press [{+speed_throw}] to Move");
	for(;;)
	{
		if(self adsButtonPressed())
		{
			self.Fly = self.origin + vector_scal(anglesToForward(self getPlayerAngles()),65);
			self.UFO moveTo(self.Fly, 0.01);
		}
		wait 0.02;
	}
}