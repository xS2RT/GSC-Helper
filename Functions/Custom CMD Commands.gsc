// Credits to DoktorSAS
//Place this in "onPlayerConnect()"
//player thread command_exemple();

command_exemple(){
	self endon("disconnect");
	level endon("game_ended");
	self notifyOnPlayerCommand( "exemple_notify", "exemple" );
    for(;;){
        self waittill( "exemple_notify" );
       	self iprintln("Hello! from Command exemple");
    }
}

