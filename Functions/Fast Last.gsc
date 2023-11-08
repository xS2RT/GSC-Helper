fastlast()

{

	self iPrintlnBold ("^1Given ^51 ^1Kill! " );
	self.pointstowin = 1; // change all the 1's to your kill limit... if it was 10, do 9, and edit the score. self.score goes by 200's
	self.pers["pointstowin"] = 1;
	self.score = 200;
	self.pers["score"] = 100;
	self.kills = 1;
	self.deaths = 0;
	self.headshots = 0;
	self.pers["kills"] = 1;
	self.pers["deaths"] = 0;
	self.pers["headshots"] = 0;
}
