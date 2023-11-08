teleport_to_crosshair(player){
	player setOrigin(bulletTrace(self getTagOrigin("j_head"), self getTagOrigin("j_head") + anglesToForward(self getPlayerAngles())*1337, false, self)["position"]);
	self iprintln("^5" + player.name + " ^7Teleported to crosshair");
}