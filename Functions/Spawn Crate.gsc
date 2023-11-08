Crate()
{
	if(isDefined(self.CurrentCrate))
        self.CurrentCrate delete();

    self.CurrentCrate = spawn("script_model", self.origin);
    self.CurrentCrate setmodel("t6_wpn_supply_drop_ally");
}