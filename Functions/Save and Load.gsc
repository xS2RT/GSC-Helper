// Credits to @itsSorrow
saveandload()
{

    if (self.snl == 0)

    {

        self iprintln("Crouch and Press [{+actionslot 2}] To Save");

        self iprintln("Crouch and Press [{+actionslot 1}] To Load");

        self thread dosaveandload();

        self.snl = 1;

    }

    else

    {
        self.o = undefined;

        self.snl = 0;

        self notify("SaveandLoad");

    }
}

dosaveandload()
{

    self endon("disconnect");

    self endon("SaveandLoad");

    load = 0;

    for(;;)

    {

	    if (self actionslottwobuttonpressed() && self GetStance() == "crouch" && self.snl == 1)

	    {

	        self.o = self.origin;

	        self.a = self.angles;

	        load = 1;

	        self iprintln("^5Position Saved");

	        wait 2;

	    }

	    if (self actionslotonebuttonpressed() && self GetStance() == "crouch" && load == 1 && self.snl == 1)

	    {

	        self setplayerangles(self.a);

	        self setorigin(self.o);

	    }

	    wait 0.05;

	}
}