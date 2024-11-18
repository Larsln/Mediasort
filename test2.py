import countries

cc = countries.CountryChecker('world-administrative-boundaries.shp')
print (cc.getCountry(countries.Point(49.7821, 3.5708)).iso)