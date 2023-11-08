// Credits to DoktorSAS
giveCustomClass( weap1, weap2, classnameP, equip1, equip2){ //Made By DoktorSAS
   self takeallweapons();
   self.classnamePlayerP = classnameP;
   self iprintln("Class ^2Choosed");
   self giveweapon("knife_mp",0,true(0,0,0,0,0));
   self giveweapon(weap1,0,true(0,0,0,0,0));
   self givemaxammo(weap1);
   self giveweapon(weap2,0,true(0,0,0,0,0));
   self givemaxammo(weap2);
   self giveweapon(equip1);
   self setWeaponAmmoStock(equip1,1);
   self giveweapon(equip2);
   self setWeaponAmmoStock(equip2,1);
    self switchtoweapon(weap1);
   self baseperk();
}
baseperk(){
   self clearperks();
   self setperk("specialty_additionalprimaryweapon");
   self setperk("specialty_fastequipmentuse");
   self setperk("specialty_fastladderclimb");
   self setperk("specialty_fastmantle");
   self setperk("specialty_bulletpenetration");
   self setperk("specialty_fastads");
   self setperk("specialty_longersprint");
   self setperk("specialty_fastweaponswitch");
   self setperk("specialty_fallheight");
}
exemple(){
   giveCustomClass("dsr50_mp+steadyaim+fmj+extclip", "ksg_mp", "DSRKSG", "sticky_grenade_mp", "proximity_grenade_mp" );
}

