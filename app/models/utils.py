import json
import requests

price = {}

def set_crypto_prices():
  price['ETH'] = float(json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/ethereum') \
      .text)[0]['price_usd'])
  price['DAI'] = float(json.loads(requests.get('https://api.coinmarketcap.com/v1/ticker/dai') \
      .text)[0]['price_usd'])

def address_to_contract_name(address):
  names = {
    '080bf510fcbf18b91105470639e9561022937712': '0x',
    'c02aaa39b223fe8d0a0e5c4f27ead9083c756cc2': '0x',
    '12459c951127e0c374ff9105dda097662a027093': '0x',
    'b1dd690cc9af7bb1a906a9b5a94f94191cc553ce': 'Argent',
    '514910771af9ca656af840dff83e8264ecf986ca': 'ChainLink',
    '3d9819210a31b4961b30ef54be2aed79b9c9cd3b': 'Compound',
    '4ddc2d193948926d02f9b1fe9e1daa0718270ed5': 'Compound',
    '3fda67f7583380e67ef93072294a7fac882fd7e7': 'Compound',
    'f5dce57282a584d2746faf1593d3121fcac444dc': 'Compound',
    '06012c8cf97bead5deae237070f9587f8e7a266d': 'CryptoKitties',
    '89d24a6b4ccb1b6faa2625fe562bdd9a23260359': 'Dai',
    '8ef1351941d0cd8da09d5a4c74f2d64503031a18': 'Dharma',
    '4e0f2b97307ad60b741f993c052733acc1ea5811': 'Dharma',
    'f7b3fc555c458c46d288ffd049ddbfb09f706df7': 'Dharma',
    '1e0447b19bb6ecfdae1e4ae1694b0c3659614e4e': 'dYdX',
    'fec6f679e32d45e22736ad09dfdf6e3368704e31': 'Edgeware',
    '1b75b90e60070d37cfa9d87affd124bb345bf70a': 'Edgeware',
    'b3775fb83f7d12a36e0475abdd1fca35c091efbe': 'Fomo3D',
    '6e95c8e8557abc08b46f3c347ba06f8dc012763f': 'Gnosis',
    'ff1a8eda5eacdb6aaf729905492bdc6376dbe2dd': 'Gnosis',
    '2a0c0dbecc7e4d658f48e01e3fa353f44050c208': 'IDEX',
    '498b3bfabe9f73db90d252bcd4fa9548cd0fd981': 'InstaDApp',
    '3a306a399085f3460bbcb5b77015ab33806a10d5': 'InstaDApp',
    '498b3bfabe9f73db90d252bcd4fa9548cd0fd981': 'InstaDApp',
    '63825c174ab367968ec60f061753d3bbd36a0d8f': 'Kyber',
    '8573f2f5a3bd960eee3d998473e50c75cdbe6828': 'Livepeer',
    '448a5065aebb8e423f0896e6c5d525c040f59af3': 'MakerDAO',
    '9f8f72aa9304c8b593d555f12ef6589cc3a579a2': 'MakerDAO',
    'bda109309f9fafa6dd6a9cb9f1df4085b27ee8ef': 'MakerDAO',
    '9b0f70df76165442ca6092939132bbaea77f2d7a': 'MakerDAO',
    'f53ad2c6851052a81b42133467480961b2321c09': 'MakerDAO',
    'ba23485a04b897c957918fde2dabd4867838140b': 'Market Protocol',
    '6217d5392f6b7b6b3a9b2512a2b0ec4cbb14c448': 'Market Protocol',
    '94772cc6e33b186bfdd0719a287f12d3ca816657': 'Market Protocol',
    '3457905deea11ddc085bc7bfaa8813aab26b2ded': 'Market Protocol',
    '0d580ae50b58fe08514deab4e38c0dfdb0d30adc': 'Melonport',
    'ec67005c4e498ec7f55e092bd1d35cbc47c91892': 'Melonport',
    '1fd169a4f5c59acf79d0fd5d91d1201ef1bce9f1': 'MolochDAO',
    '08c3a887865684f30351a0ba6d683aa9b539829a': 'Nexus Mutual',
    '802275979b020f0ec871c5ec1db6e412b72ff20b': 'Nuo Network',
    'd26114cd6ee289accf82350c8d8487fedb8a0c07': 'OmiseGO',
    '4aa42145aa6ebf72e164c9bbc74fbd3788045016': 'POA Network',
    'e1579debdd2df16ebdb9db8694391fa74eea201e': 'POA Network',
    '5b67871c3a857de81a1ca0f9f7945e5670d986dc': 'Set Protocol',
    'f55186cc537e7067ea616f2aae007b4427a120c8': 'Set Protocol',
    '882d80d3a191859d64477eb78cca46599307ec1c': 'Set Protocol',
    'c011a72400e58ecd99ee497cf89e3775d4bd732f': 'Synthetix',
    '94a1b5cdb22c43faab4abeb5c74999895464ddaf': 'Tornado Mixer',
    'cd2053679de3bcf2b7e2c2efb6b499c57701222c': 'Totle',
    'c0a47dfe034b400b47bdad5fecda2621de6c4d95': 'Uniswap',
    '2c4bd064b998838076fa341a83d007fc2fa50957': 'Uniswap',
    '09cabec1ead1c0ba254b09efb3ee13841712be14': 'Uniswap',
    '22d8432cc7aa4f8712a655fc4cdfb1baec29fca9': 'Uniswap',
    'f173214c720f58e03e194085b1db28b50acdeead': 'Uniswap'
  }
  return names[address.lower()] if address.lower() in names else 'Other'
