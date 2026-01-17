FUNNELS = {
    "financas": {
        "cold": "conteudo_educativo",
        "warm": "prova_social",
        "hot": "oferta"
    }
}

def get_funnel(niche, stage):
    return FUNNELS.get(niche, {}).get(stage)
