module raspi(){
 import("B+_Model_v4.stl", convexity=3);
}
 
shell = 1.5;
width = 86;
length = 56;
height = 10;
bottom = 2;
round = 1.5;
boardheight = 4;
pinsafe = 3;

$fn = 50;

module case_1(){
   difference(){
	 translate([-shell,-shell,-shell]) cube([width+shell*2, length+shell*2, height+shell*2]);
 	 translate([0,0,0]) cube([width, length, height]);
  };

}

module case(){
  difference(){
	 minkowski(){
	   translate([0,0,-bottom]) cube([width, length, height]);
      cylinder(r=shell/2,h=height);
	 }
    translate([0,0,0]) cube([width, length, height]);
  }
}


module av(){
  translate([ 85-53.5, 56, 4.5]) rotate([90,0,0])  cylinder(r=2*round, h=boardheight, center=true);

}

module hdmi(){
  translate([ 85-32, 56, 5]) 
  union(){
     hull(){
     translate([0, 0, 1.5]) cube([16, 10, 4], center=true);
     translate([0, 0, -1.5]) cube([12, 10, 3], center=true);
    }
  }

}

module power(){
  translate([ 85-10.6, 56, 3.5]) 
  union(){
     hull(){
     cube([9, 10, 1.5], center=true);
     translate([0, 0, -2]) cube([7, 10, 1], center=true);
    }
  }

}

module ethernet(){
  translate([ 10, 56-10.25, 8]) cube([25, 16, 16], center=true);
  translate([ 9, 56-10.25, 0]) union(){
	 translate([0, 5, 0]) cylinder(r=2, h=5, center=true);
	 translate([0, -5, 0]) cylinder(r=2, h=5, center=true);
}

}

module usbs(){
  translate([ 10, 56-29, 9.5]) cube([25, 16, 16], center=true);
  translate([ 10, 56-47, 9.5]) cube([25, 16, 16], center=true);


}

module gpio(){
  translate([ 85-29-3.5, 4, 4 ]) cube([54, 6, 12], center=true);
}

module sd(){
  ##translate([ 78, 56-28.5, -1 ]) cube([17, 14.5, 2], center=true);

}

module pi(){
  minkowski(){
	translate([2*round, 2*round, ]) cube([width-4*round, length-4*round, boardheight]);
   cylinder(r=2*round, h=boardheight);
  }
  av();
  hdmi();
  power();
  ethernet();
  usbs();
  gpio();
  sd();
}

//#translate([5, 0, 0])
#pi();
import("B+_Model_v4_centred.stl", convexity=3);
