function slant_range = geo(es_lat_deg, es_long_deg, st_long_deg)
    earth_radius_km = earthRadius('km');
    gso_semi_major_axis_km = (398600000000000*(86400*(365.25/366.25)/(2*pi))^2)^(1/3)/1000;
    earth_central_angle = 57.29578 * acosd(cosd(abs(es_lat_deg)/57.29578)*cosd(abs(es_long_deg-st_long_deg)/57.29578));
    slant_range = sqrt(gso_semi_major_axis_km^2 + earth_radius_km^2 - 2*gso_semi_major_axis_km*earth_radius_km*cosd(earth_central_angle/57.29578));
end