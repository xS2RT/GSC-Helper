isentityabot()
{
	return (isDefined(self.pers["isBot"]) && self.pers["isBot"]);
}

/*
example usage to count number of bots in game:

countBots()
{
	bots = 0;
	foreach (player in level.players)
	{
		if (player isentityabot())
		{
			bots++;
		}
	}
	return bots;
}
*/
