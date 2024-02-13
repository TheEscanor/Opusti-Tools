void main()
{
    vector spawnLocation = "2207.89 42.5511 1604.76"; // ตำแหน่งเริ่มต้นที่ตัวละครจะเกิด
    Entity playerEnt = GetGame().CreatePlayer(NULL, "SurvivorM_Mirek", spawnLocation, 0, "NONE");
    PlayerBase player = (PlayerBase) playerEnt;

	TStringArray tops = {"USMCJacket_Woodland"};
	TStringArray pants = {"USMCPants_Woodland"};
	TStringArray shoes = {"CombatBoots_Green","CombatBoots_Black"};
		
	EntityAI item = player.GetInventory().CreateInInventory(tops.GetRandomElement());
	EntityAI item2 = player.GetInventory().CreateInInventory(pants.GetRandomElement());
	EntityAI item3 = player.GetInventory().CreateInInventory(shoes.GetRandomElement());
	
	EntityAI itemEnt;
	EntityAI itemIn;
	ItemBase itemBs;
	int rndQnt;
	
	itemEnt = player.GetInventory().CreateInInventory("Rag");
	itemBs = ItemBase.Cast(itemEnt);
	itemBs.SetQuantity(4);

	itemEnt = player.GetInventory().CreateInInventory("Flashlight");
	if (itemEnt.GetType() == "Flashlight")
	{
		EntityAI battery9V = itemEnt.GetInventory().CreateAttachment("Battery9V");
	}

	itemEnt = player.GetInventory().CreateInInventory("Aug");
	ItemBase aug = ItemBase.Cast(itemEnt);
	player.SetQuickBarEntityShortcut(itemEnt, 0);
	itemIn = itemEnt.GetInventory().CreateAttachment("M4_Suppressor");
	itemIn = itemEnt.GetInventory().CreateAttachment("Mag_Aug_30Rnd");	
	itemIn = itemEnt.GetInventory().CreateAttachment("ReflexOptic");
	itemIn.GetInventory().CreateAttachment("Battery9V");
	itemIn = itemEnt.GetInventory().CreateAttachment("UniversalLight");
	itemIn.GetInventory().CreateAttachment("Battery9V");

	GetGame().SelectPlayer(NULL, player);
}
