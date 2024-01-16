function()
    local result = ""
    local totalFreeSlots = 0

    for bag = BACKPACK_CONTAINER, NUM_TOTAL_EQUIPPED_BAG_SLOTS do
        local numSlots = C_Container.GetContainerNumSlots(bag)
        local slotsLeft = 0

        for slot = 1, numSlots do
            local itemLink = C_Container.GetContainerItemLink(bag, slot)
            if not itemLink then
                slotsLeft = slotsLeft + 1
                totalFreeSlots = totalFreeSlots + 1
            else
                local itemName, _, itemRarity, _, _, _, _, _, _, itemTexture = GetItemInfo(itemLink)
                local itemID = tonumber(string.match(itemLink, "item:(%d+)"))

                result = result .. "\n" .. "Bag: " .. bag .. " | Slot: " .. slot .. " | ItemID: " .. itemID .. " | Name: " .. itemName .. " | Rarity: " .. itemRarity .. " | Texture: " .. itemTexture
            end
        end

        result = result .. "\n" .. "Bag: " .. bag .. " | Slots Left: " .. slotsLeft .. "\n"
    end

    result = "Total Free Slots: " .. totalFreeSlots .. "\n" .. result
    return result
end
