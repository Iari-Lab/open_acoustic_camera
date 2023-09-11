e = 0.5;
radius = 0.3/2;
color ("gray") {
    for(j=[0:9]) 
        {
        for (i = [0:9]){
            translate([i*e,j*e,radius]) {
                sphere(r = radius, $fn=10, center=true);
                }
       }
    }
}

color ("black") {
    translate([-0.5,-0.5,0.21]) {        
        cube( [5.5,5.5,0.4] );
    }
}
