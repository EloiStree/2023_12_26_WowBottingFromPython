function(progress, r1, g1, b1, a1, r2, g2, b2, a2)
    posX=0
    posY=0
    facing=0
    
    if IsInInstance() then
        posX = 0
        posY = 0
        facing=0
    else
        local map = C_Map.GetBestMapForUnit("player");
        if not map==nil then
            
            local pos = C_Map.GetPlayerMapPosition(map,"player");
            if not pos==nil then
                
                local posX,posY = pos:GetXY()
                local facing = GetPlayerFacing() / (2*3.1418)
            end
        end
    end
    
    
    return posX,posY,facing,1
end

