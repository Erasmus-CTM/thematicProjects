-- Seitentitel je Sprache.
-- Im Profil "english" ersetzt `title-en:` (und `subtitle-en:`, `description-en:`)
-- aus dem Seitenkopf den deutschen Wert. Im Profil "deutsch" werden die -en-Felder
-- nur entfernt. So bleibt pro Seite eine einzige .qmd-Datei für beide Sprachen.
local profile = os.getenv("QUARTO_PROFILE") or ""

local function isEnglish()
  for p in profile:gmatch("[^,%s]+") do
    if p == "english" then return true end
  end
  return false
end

local felder = { "title", "subtitle", "description" }

function Meta(meta)
  local englisch = isEnglish()
  for _, feld in ipairs(felder) do
    local en = meta[feld .. "-en"]
    if englisch and en ~= nil then
      meta[feld] = en
    end
    meta[feld .. "-en"] = nil
  end
  return meta
end
