file = io.open ("factorio_015_items.csv", "w")

data = {}
data["extend"] = function (data, t)
    for n, recipe in ipairs(t) do
        for i, component in ipairs(recipe["ingredients"]) do
            cname = component[1] or component["name"]
            camt = component[2] or component["amount"]
            file:write('"' .. recipe["name"] .. '","' .. cname .. '",' .. camt .. "\n")
            print('"' .. recipe["name"] .. '","' .. cname .. '",' .. camt)
        end
    end
end

files = {
    "ammo",
    "capsule",
    "demo-furnace-recipe",
    "demo-recipe",
    "demo-turret",
    "equipment",
    "fluid-recipe",
    "furnace-recipe",
    "inserter",
    "module",
    "recipe",
    "turret",
}

for i, f in ipairs(files) do
    dofile("./recipes/" .. f .. ".lua")
end
