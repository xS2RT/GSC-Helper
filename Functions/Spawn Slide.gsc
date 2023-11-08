manageSlides()
{
    self endon("death");
    self endon("disconnect");

    start = self getTagOrigin("tag_eye");
    end = anglestoforward(self getPlayerAngles()) * 1000000;
    slidePos = BulletTrace(start, end, true, self)["position"] + (0,0,15);
    slideAng = self getPlayerAngles();

    if(!isDefined(self.slide))
    {
        self.slide = spawn("script_model", slidePos);
        self.slide.angles = (0, slideAng[1] - 90, 70);
        self.slide setModel("t6_wpn_supply_drop_trap");
    }
    else
    {
        self.slide RotateTo((0, slideAng[1] - 90, 70), 0.1, 0, 0 );
        self.slide MoveTo(slidePos, 0.1, 0, 0 );
        self.slide notify("restartSlideThink"); // Killing thread so it doesn't duplicate
    }

    self.slide thread slideThink(slidePos,slideAng);
}

slideThink(origin, angles)
{
    self endon("restartSlideThink");

    for(;;)
    {
        foreach(player in level.players)
        {
            if( distance(player.origin, origin) < 100 && player meleeButtonPressed() && player isMeleeing() && length(anglesXY(player getPlayerAngles() - angles)) < 90)
            {
                vec = anglesToForward(player.angles);
                for(i = 0; i < 10; i++)
                {
                    player setVelocity(player getVelocity() + ( vec[0]*(100) , vec[1]*(100), 200 ));
                    wait .01;
                }
            }
        }
        wait .1;
    }
}

anglesXY(angles)
{
    return (angles[0], angles[1], 0);
}