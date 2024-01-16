function()
    
    local player ="player"
    local target ="target"
    local dico = {    }
    
    
    
    
    
    local totalItemLevel = 0
    local totalItems = 0
    local description ="D"
    
    for i = 1, 18 do  -- Iterate through equipment slots
        local itemInfo= GetInventoryItemLink(player, i)
        if itemInfo then
            local itemName, itemLink, itemRarity, itemLevel, itemMinLevel, itemType, itemSubType, itemStackCount, itemEquipLoc, itemIcon, itemSellPrice, itemClassID, itemSubClassID, bindType, expacID, itemSetID, isCraftingReagent = GetItemInfo(itemInfo)
            
            if itemLevel then
                totalItemLevel = totalItemLevel + itemLevel
                totalItems = totalItems + 1
            end
            
            
            
            
            if itemLevel then
                local line = string.format("Name: %s, Link: %s, Rarity: %d, Level: %d, Type: %s, SubType: %s, Stack Count: %d, Equip Loc: %s, Icon: %s, Sell Price: %d\n",
                itemName, itemLink, itemRarity, itemLevel, itemType, itemSubType, itemStackCount, itemEquipLoc, itemIcon, itemSellPrice)
                
                description= description..line
            else
                
            end
            
            
        end
    end
    dico.a_description = description
    dico.a_averageItemLevel = totalItemLevel / totalItems
    
    
    
    
    local timeTick =10
    local result = ""
    result = "Armor:"..(math.floor( GetTime() / timeTick )) .. "\n"
    result = result.."Time:"..GetTime().."\n"
    local keys = {}
    
    for key, _ in pairs(dico) do
        table.insert(keys, key)
    end
    
    -- Sort keys
    table.sort(keys)
    
    -- Iterate over sorted keys
    for _, key in ipairs(keys) do
        local value = dico[key]
        
        -- Check if the value is nil
        if value == nil then
            value = "nil"
        elseif type(value) == "boolean" then
            -- Convert boolean to string
            value = value and "True" or "False"
        end
        
        result = result .. key .. ":" .. value .. "\n"
    end
    
    return result
    
end









