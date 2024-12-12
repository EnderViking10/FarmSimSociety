-- Lightweight FarmersOnly Mod

local modDirectory = g_currentModDirectory
local modName = g_currentModName

local clubhouse = {}

local function loadJsonFile(filePath)
    local file = io.open(filePath, "r")
    if file then
        local content = file:read("*all")
        file:close()
        return json.decode(content)
    else
        return nil
    end
end

local function handleCommand(command)
    print("Handling command: " .. command.type .. ":" .. command.action)
    -- Implement command handling logic here based on command.type and command.action
    -- Example:
    if command.type == "money" and command.action == "add" then
        local farmName = command.farmName
        local amount = command.amount
        -- Add money to the specified farm
    end
end

local function processCommands()
    local filePath = getUserProfileAppPath() .. "modSettings/FarmSimSociety/commands.json"
    local commands = loadJsonFile(filePath)
    if commands then
        for _, command in ipairs(commands) do
            handleCommand(command)
        end
    end
end

local function onMoneyChanged(farmId)
    if farmId > 0 then
        local farm = g_farmManager:getFarmById(farmId)
        print("Money changed for farm: " .. farm.name .. ", current balance: " .. farm.money)
        processCommands()
    end
end

local function subscribeToEvents()
    if g_currentMission and g_currentMission.messageCenter then
        -- Check if messageCenter exists
        g_currentMission.messageCenter:subscribe(MessageType.MONEY_CHANGED, onMoneyChanged)
        print("Subscribed to MONEY_CHANGED event.")  -- Confirmation message
    else
        print("Error: Could not subscribe to events. messageCenter is nil.")  -- Error message
    end
end

local function init()
    g_currentMission.clubhouse = clubhouse
    subscribeToEvents()  -- Call the subscription function
end

local function unload()
    if g_currentMission and g_currentMission.messageCenter then
        -- Check during unload too.
        g_currentMission.messageCenter:unsubscribeAll(clubhouse)
        print("Unsubscribed from events.") -- Confirmation
    end
    g_currentMission.clubhouse = nil
end


-- Use Mission00.loadMission00Finished instead of Mission00.load
Mission00.loadMission00Finished = Utils.appendedFunction(Mission00.loadMission00Finished, function(mission, superFunc, callback)
    superFunc(mission, callback) -- Call original function first
    init() -- Initialize after the original load function is finished.
end)

FSBaseMission.delete = Utils.appendedFunction(FSBaseMission.delete, unload)


-- Example commands.json file:
-- [
--     {"type": "money", "action": "add", "farmName": "My Farm", "amount": 10000},
--     {"type": "money", "action": "subtract", "farmName": "Other Farm", "amount": 5000}
-- ]
