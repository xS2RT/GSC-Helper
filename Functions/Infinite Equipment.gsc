infiniteEquipment()
{
    self endon("disconnect");
    if(!isDefined(self.infAmmo))
    {
        self.infAmmo = true;
        self thread infAmmo();
        self iprintln("Infinite equipments: ^2ON^7");
    }
    else
    {
        self.infAmmo = undefined;
        self iprintln("Infinite equipments: ^1OFF^7");
    }
}

infAmmo()
{
    self endon("disconnect");

    while(isDefined(self.infAmmo))
    {
        off = self getCurrentOffHand();
        if(off != "none")
            self giveMaxAmmo(off);
        wait .05;
    }
}