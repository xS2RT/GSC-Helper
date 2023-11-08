ToggleplayerUAV()
{
	if(self.someuav==true)
	{
		self iprintln("Toggle Constant UAV: ^2ON^7");
		self setclientuivisibilityflag("g_compassShowEnemies",1);
		self.someuav=false;
	}
	else
	{
		self iprintln("Toggle Constant UAV: ^1OFF^7");
		self setclientuivisibilityflag("g_compassShowEnemies",0);
		self.someuav=true;
	}
}