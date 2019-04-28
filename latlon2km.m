function [ d ] = latlon2km( lat1, lon1, lat2, lon2 )

    r = 6372.8;
    dlat = deg2rad(lat2-lat1);
    dlon = deg2rad(lon2-lon1);
    lat1 = deg2rad(lat1);
    lat2 = deg2rad(lat2);
    
    a = (sin(dlat./2)).^2 + cos(lat1) .* cos(lat2) .* (sin(dlon./2)).^2;
    c = 2 .* asin(sqrt(a));
    d = r.*c;
    %arrayfun(@(x) printf("distance: %.4f km\n",6372.8 * x), c);

end

