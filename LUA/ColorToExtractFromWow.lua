function(progress, r1, g1, b1, a1, r2, g2, b2, a2)
    posX=0
    posY=0
    facing=0
    
    if IsInInstance() then
        
    else
        local map = C_Map.GetBestMapForUnit("player");
        local pos = C_Map.GetPlayerMapPosition(map,"player");
        local posX,posY = pos:GetXY()
        local facing = GetPlayerFacing() / (2*3.1418)
    end
    
    return posX,posY,facing,1
end

