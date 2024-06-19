def create_ticker(name):
    name = name.replace('City', '')
    name = name.replace('New York', 'NYC')
    name = name.replace('Los Angeles', 'LAX')
    name = name.replace('Atlanta', 'ATL')
    name = name.replace('Las Vegas', 'LAS')
    name = name.replace('San Diego', 'SAN')
    name = name.replace('Boston', 'BOS')
    name = name.replace('Miami Beach', 'MIABCH')
    name = name.replace('San Francisco', 'SFO')
    name = name.replace('Denver', 'DEN')
    name = name.replace('Chicago', 'CHI')
    name = name.replace('Washington, DC', 'DC')
    name = name.replace('Washington', 'DC')
    name = name.replace('Austin', 'ATX')
    name = name.replace('United States Of America', 'USA')
    name = name.replace('Kings County', 'BRKLYN')
    name = name.replace('Miami', 'MIA')
    return name

def format_names(nme):
    nme = nme.replace('United States Of America', 'USA')
    nme = nme.replace('Kings County', 'Brooklyn, NY')
    nme = nme.replace('Washington City', 'Washington, DC')
    return nme

def format_cs_10_names(nme):
    nme = nme.replace('Denver-Aurora-Lakewood, Co', 'Denver')
    nme = nme.replace('Boston-Cambridge-Newton, Ma-Nh', 'Boston')
    nme = nme.replace('Las Vegas-Henderson-Paradise, Nv', 'Las Vegas')
    nme = nme.replace('San Francisco-Oakland-Berkeley, Ca', 'San Francisco')
    nme = nme.replace('Chicago-Naperville-Elgin, Il-In-Wi', 'Chicago')
    nme = nme.replace('Los Angeles-Long Beach-Anaheim, Ca', 'Los Angeles')
    nme = nme.replace('San Diego-Chula Vista-Carlsbad, Ca', 'San Diego')
    nme = nme.replace('Washington-Arlington-Alexandria, Dc-Va-Md-Wv', 'Washington, DC')
    nme = nme.replace('Miami-Fort Lauderdale-Pompano Beach, Fl', 'Miami')
    nme = nme.replace('New York-Newark-Jersey City, Ny-Nj-Pa', 'New York')
    return nme