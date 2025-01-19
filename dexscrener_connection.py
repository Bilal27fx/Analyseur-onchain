import requests

def get_token_data(token_address):
    """Récupère les données d'un token depuis l'API Dexscreener."""
    url = f"https://api.dexscreener.com/latest/dex/tokens/{token_address}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Erreur : {response.status_code}"}
    except Exception as e:
        return {"error": f"Une erreur s'est produite : {str(e)}"}

def get_specific_data_from_api(token_address):
    """Récupère des données spécifiques d'un token."""
    data = get_token_data(token_address)
    
    if "error" in data:
        return data["error"]  # Retourne l'erreur si présente

    try:
        # Extraire les informations nécessaires
        base_token_name = data['pairs'][0]['baseToken']['name']
        quote_token_symbol = data['pairs'][0]['quoteToken']['symbol']
        price_in_usd = data['pairs'][0]['priceUsd']
        market_cap = data['pairs'][0]['marketCap']
        website = data['pairs'][0]['info']['websites'][0]['url']
        twitter = data['pairs'][0]['info']['socials'][0]['url']
        variation_24h = data['pairs'][0]['priceChange']['h24']
        
        return (base_token_name, quote_token_symbol, price_in_usd, market_cap, website, twitter, variation_24h)
    
    except (KeyError, IndexError):
        return "Erreur : Impossible de trouver les informations demandées dans la réponse de l'API."
