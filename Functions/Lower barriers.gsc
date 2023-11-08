// Credits to DoktorSAS

/*
 place this in onPlayerConnect()
 level thread doLowerbarriers();
 only needs to call once
*/

doLowerbarriers()
{
	dksas = 0;
	switch (getDvar("mapname"))
	{
	case "mp_bridge":
		dksas = 1300;
		break;
	case "mp_concert":
		dksas = 200;
		break;
	case "mp_express":
	case "mp_dig":
	case "mp_nightclub":
		dksas = 250;
		break;
	case "mp_uplink":
	case "mp_slums":
		dksas = 350;
		break;
	case "mp_magma":
	case "mp_hijacked":
	case "mp_takeoff":
	case "mp_carrier":
	case "mp_meltdown":
		dksas = 100;
		break;
	case "mp_raid":
		dksas = 120;
		break;
	case "mp_studio":
		dksas = 20;
		break;
	case "mp_socotra":
	case "mp_downhill":
		dksas = 620;
		break;
	case "mp_vertigo":
		dksas = 1000;
		break;
	case "mp_hydro":
		dksas = 1200;
		level thread customHydroBarrier();
		break;
	case "mp_nuketown_2020":
		dksas = 200;
		break;
	}
	lowerBarrier(dksas);
	removeHighBarrier();
}

customHydroBarrier()
{
	level endon("game_ended");
	for (;;)
	{
		wait 0.05;
		foreach (player in level.players)
		{
			if (player.origin[2] < 1100 && player.origin[2] > 900)
			{
				player suicide();
			}
		}
	}
}

lowerBarrier(dksas)
{
	hurt_triggers = getentarray("trigger_hurt", "classname");
	foreach (barrier in hurt_triggers)
		if (barrier.origin[2] <= 0)
			barrier.origin -= (0, 0, dksas);
	// else barrier.origin += (0, 0, 99999);
}

removeHighBarrier()
{
	hurt_triggers = getentarray("trigger_hurt", "classname");
	foreach (barrier in hurt_triggers)
		if (isDefined(barrier.origin[2]) && barrier.origin[2] >= 70)
			barrier.origin += (0, 0, 99999);
}