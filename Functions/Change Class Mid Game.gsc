// Credits to @VariationModz7s
//place this in init()
// game["strings"]["change_class"] = undefined; // Removes the class text if changing class midgame

//Place this in "onplayerspawned()"
//self thread monitorClass();

MonitorClass()
{

   self endon("disconnect");

    for(;;)
    {
        self waittill("changed_class");
        self maps\mp\gametypes\_class::giveloadout( self.team, self.class );
        wait .5;
    }

}
