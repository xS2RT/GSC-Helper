#include maps\mp\_utility;
#include common_scripts\utility;
#include maps\mp\gametypes\_hud_util;
#include maps\mp\gametypes\_hud_message;
#include maps\mp\gametypes\_globallogic;

init()
{
    level thread onPlayerConnect();
}

onPlayerConnect()
{
    for(;;)
    {
        level waittill("connecting", player);

        player thread onPlayerSpawned();
        if(player isHost())
            player.Status = "Host";
        else player.status = "User";
    }
}

onPlayerSpawned()
{
    self endon("disconnect");
    level endon("game_ended");
    self.MenuInit = false;
    self.MenuTitle = "GSC Helper";
	self.txt = "Controls:\n  [{+actionslot 1}] - Scroll Up\n  [{+actionslot 2}] - Scroll Down\n  [{+usereload}] - Select\n  [{+melee}] - Go Back\n\nMade with: ^3GSC Helper^7\nBy ^6S2RT";
    self.TitleColor = (1, 1, 1);
    self.TitleGlow = (1, 0, 1);
    self.ScrollerColor = (0, 1, 0);
    self.Line1Color = (0, 1, 0);
    self.Line2Color = (0, 1, 0);
    self.Line3Color = (0, 1, 0);
    self.Line4Color = (0, 1, 0);
    for(;;)
    {
        self waittill("spawned_player");

        self freezeControls(false);
        if (!self.MenuInit)
        {
            self.MenuInit = true;
            self thread MenuInit();
            self thread closeMenuOnDeath();
        }
        self iPrintlnBold("Crouch and [{+actionslot 3}] to Access Menu");
    }
}

CreateMenu()
{
    self add_menu("Main Menu", undefined, "User");
}

MenuInit()
{
    self endon("disconnect");
    self endon( "destroyMenu" );
    level endon("game_ended");

    self.menu = spawnstruct();
    self.toggles = spawnstruct();
    self.menu.open = false;
    self StoreShaders();
    self CreateMenu();
    for(;;)
    {
        if(self getStance() == "crouch" && self actionSlotThreeButtonPressed() && !self.menu.open) // Open.
        {
            openMenu();
        }
        else if(self.menu.open)
        {
            if(self meleebuttonpressed())
            {
                if(isDefined(self.menu.previousmenu[self.menu.currentmenu]))
                {
                    self submenu(self.menu.previousmenu[self.menu.currentmenu], self.MenuTitle);
                }
                else
                {
                    closeMenu();
                }
                wait 0.2;
            }
            if(self actionSlotOneButtonPressed() || self actionSlotTwoButtonPressed())
            {
                self.menu.curs[self.menu.currentmenu] += (Iif(self actionSlotTwoButtonPressed(), 1, -1));
                self.menu.curs[self.menu.currentmenu] = (Iif(self.menu.curs[self.menu.currentmenu] < 0, self.menu.menuopt[self.menu.currentmenu].size-1, Iif(self.menu.curs[self.menu.currentmenu] > self.menu.menuopt[self.menu.currentmenu].size-1, 0, self.menu.curs[self.menu.currentmenu])));

                self updateScrollbar();
            }
            if(self UseButtonPressed())
            {
                self thread [[self.menu.menufunc[self.menu.currentmenu][self.menu.curs[self.menu.currentmenu]]]](self.menu.menuinput[self.menu.currentmenu][self.menu.curs[self.menu.currentmenu]], self.menu.menuinput1[self.menu.currentmenu][self.menu.curs[self.menu.currentmenu]]);
                wait 0.2;
            }
        }
        wait 0.05;
    }
}

submenu(input, title)
{
    if (verificationToNum(self.status) >= verificationToNum(self.menu.status[input]))
    {
        self.menu.options destroy();
        if (input == "Main Menu")
        {
            self thread StoreText(input, "Main Menu");
            self updateScrollbar();
        }
        else
        {
            self thread StoreText(input, title);
            self updateScrollbar();
        }

        self.CurMenu = input;

        self.menu.title destroy();
        self.menu.title = drawText(title, "objective", 2, 0, 20, self.TitleColor, 0, self.TitleGlow, 1, 3);
        self.menu.title FadeOverTime(0.3);
        self.menu.title.alpha = 1;

        self.menu.scrollerpos[self.CurMenu] = self.menu.curs[self.CurMenu];
        self.menu.curs[input] = self.menu.scrollerpos[input];
        self updateScrollbar();

        if (!self.menu.closeondeath)
        {
           self updateScrollbar();
        }
    }
    else
    {
        self iPrintln("Only Players With ^6" + self.menu.status[input] + " ^7Can Access This");
    }
}

add_menu_alt(Menu, prevmenu)
{
    self.menu.getmenu[Menu] = Menu;
    self.menu.menucount[Menu] = 0;
    self.menu.previousmenu[Menu] = prevmenu;
}

add_menu(Menu, prevmenu, status)
{
    self.menu.status[Menu] = status;
    self.menu.getmenu[Menu] = Menu;
    self.menu.scrollerpos[Menu] = 0;
    self.menu.curs[Menu] = 0;
    self.menu.menucount[Menu] = 0;
    self.menu.previousmenu[Menu] = prevmenu;
}

add_option(Menu, Text, Func, arg1, arg2)
{
    Menu = self.menu.getmenu[Menu];
    Num = self.menu.menucount[Menu];
    self.menu.menuopt[Menu][Num] = Text;
    self.menu.menufunc[Menu][Num] = Func;
    self.menu.menuinput[Menu][Num] = arg1;
    self.menu.menuinput1[Menu][Num] = arg2;
    self.menu.menucount[Menu] += 1;
}


elemMoveY(time, input)
{
    self moveOverTime(time);
    self.y = 69 + input;
}


updateScrollbar()
{
    self.menu.scroller fadeOverTime(0.3);
    self.menu.scroller.alpha = 0.75;
    self.menu.scroller moveOverTime(0.15);
    self.menu.scroller.y = 49 + (self.menu.curs[self.menu.currentmenu] * 20.36);
}

openMenu()
{
    self freezeControls(false);
    self StoreText("Main Menu", "Main Menu");

    self.menu.title destroy();
    self.menu.title = drawText(self.MenuTitle, "objective", 2, 0, 20, self.TitleColor, 0, self.TitleGlow, 1, 3);
    self.menu.title FadeOverTime(0.3);
    self.menu.title.alpha = 1;

    self.menu.control = drawText(self.txt, "objective", 1.4, -130, 70, (1, 1, 1), 0, (0, 0, 0), 0, 3);
    self.menu.control FadeOverTime(0.3);
    self.menu.control.alpha = 1;

    self.menu.background FadeOverTime(0.3);
    self.menu.background.alpha = .75;

    self.menu.line1 FadeOverTime(0.3);
    self.menu.line1.alpha = .75;
    self.menu.line2 FadeOverTime(0.3);
    self.menu.line2.alpha = .75;
    self.menu.line3 FadeOverTime(0.3);
    self.menu.line3.alpha = .75;
    self.menu.line4 FadeOverTime(0.3);
    self.menu.line4.alpha = .75;

    self updateScrollbar();
    self.menu.open = true;
}

closeMenu()
{
    self.menu.title destroy();

    self.menu.options FadeOverTime(0.3);
    self.menu.options.alpha = 0;

    self.menu.background FadeOverTime(0.3);
    self.menu.background.alpha = 0;

    self.menu.control FadeOverTime(0.3);
    self.menu.control.alpha = 0;
    self.menu.control destroy();

    self.menu.line1 FadeOverTime(0.3);
    self.menu.line1.alpha = 0;
    self.menu.line2 FadeOverTime(0.3);
    self.menu.line2.alpha = 0;
    self.menu.line3 FadeOverTime(0.3);
    self.menu.line3.alpha = 0;
    self.menu.line4 FadeOverTime(0.3);
    self.menu.line4.alpha = 0;

    self.menu.title FadeOverTime(0.3);
    self.menu.title.alpha = 0;

    self.menu.scroller FadeOverTime(0.3);
    self.menu.scroller.alpha = 0;
    self.menu.open = false;
}

destroyMenu(player)
{
    player.MenuInit = false;
    closeMenu();
    wait 0.3;

    player.menu.options destroy();
    player.menu.background destroy();
    player.menu.scroller destroy();
    player.menu.line destroy();
    player.menu.title destroy();
    player notify("destroyMenu");
}

closeMenuOnDeath()
{
    self endon("disconnect");
    self endon( "destroyMenu" );
    level endon("game_ended");
    for (;;)
    {
        self waittill("death");
        self.menu.closeondeath = true;
        self submenu("Main Menu", self.MenuTitle);
        closeMenu();
        self.menu.closeondeath = false;
        self.menu.title destroy();
    }
}

StoreShaders()
{
    self.menu.background = self drawShader("white", 0, 0, 450,  250, (0, 0, 0), 0, 0);
    self.menu.scroller = self drawShader("white", 100, -500, 200, 17, self.ScrollerColor, 255, 0);
    self.menu.line1 = self drawShader("white", 0, 0, 450, 2, self.Line1Color, 0, 0);
    self.menu.line2 = self drawShader("white", 0, 250, 450, 2, self.Line2Color, 0, 0);
    self.menu.line3 = self drawShader("white", -225, 2, 2, 250, self.Line3Color, 0, 0);
    self.menu.line4 = self drawShader("white", 225, 0, 2, 250, self.Line4Color, 0, 0);
    self.menu.control = drawText(self.txt, "objective", 1.4, -130, 70, (1, 1, 1), 0, (0, 0, 0), 0, 3);
}

StoreText(menu, title)
{
    self.menu.currentmenu = menu;
    self.menu.title destroy();
    string = "";
    self.menu.title = drawText(title, "objective", 2, 0, 20, self.TitleColor, 0, self.TitleGlow, 1, 3);
    self.menu.title FadeOverTime(0.3);
    self.menu.title.alpha = 1;

    for(i = 0; i < self.menu.menuopt[menu].size; i++)
    { string += self.menu.menuopt[menu][i]+ "\n"; }

    self.menu.options destroy();
    self.menu.options = drawText(string, "objective", 1.7, 100, 48, (1, 1, 1), 0, (0, 0, 0), 0, 4);
    self.menu.options FadeOverTime(0.3);
    self.menu.options.alpha = 1;
}

getPlayerName(player)
{
    playerName = getSubStr(player.name, 0, player.name.size);
    for(i=0; i < playerName.size; i++)
    {
        if(playerName[i] == "]")
            break;
    }
    if(playerName.size != i)
        playerName = getSubStr(playerName, i + 1, playerName.size);
    return playerName;
}

Iif(bool, rTrue, rFalse)
{
    if(bool)
        return rTrue;
    else
        return rFalse;
}

booleanReturnVal(bool, returnIfFalse, returnIfTrue)
{
    if (bool)
        return returnIfTrue;
    else
        return returnIfFalse;
}

booleanOpposite(bool)
{
    if(!isDefined(bool))
        return true;
    if (bool)
        return false;
    else
        return true;
}

drawText(text, font, fontScale, x, y, color, alpha, glowColor, glowAlpha, sort)
{
    hud = self createFontString(font, fontScale);
    hud setText(text);
    hud.x = x;
    hud.y = y;
    hud.color = color;
    hud.alpha = alpha;
    hud.glowColor = glowColor;
    hud.glowAlpha = glowAlpha;
    hud.sort = sort;
    hud.alpha = alpha;
    return hud;
}

drawShader(shader, x, y, width, height, color, alpha, sort)
{
    hud = newClientHudElem(self);
    hud.elemtype = "icon";
    hud.color = color;
    hud.alpha = alpha;
    hud.sort = sort;
    hud.children = [];
    hud setParent(level.uiParent);
    hud setShader(shader, width, height);
    hud.x = x;
    hud.y = y;
    return hud;
}

verificationToNum(status)
{
    if (status == "Host")
        return 2;
    if (status == "User")
        return 1;
    else
        return 0;
}

vector_scal(vec, scale)
{
    vec = (vec[0] * scale, vec[1] * scale, vec[2] * scale);
    return vec;
}