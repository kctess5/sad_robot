module head(back_depth, file, z_scale, scale_factor, hold_factor, t) {
	// back part
	color([1,.7,1]) 
		hull() {
			translate([0,0,-0.5*back_depth]) cube([1.2,1.03,back_depth], center=true);
			translate([0,0,-0.6*back_depth]) cube([.8,.7, back_depth], center=true);
		}

	// this bit of math scales the 0->1 value of t to 0->1->1->0 with a hold at 1 in the center
	x = 2*hold_factor+2;
	tp = 1 - max(0, abs(x*(t-0.5)) - hold_factor);

	// face
	color([.2,.6,.95]) 
		union() {
			cube([1.15,1,.01], center=true);
			translate([0,0, (scale_factor-1)*back_depth * (1-tp)]) 
				scale([1, 1, 1]) resize([1,1,z_scale*(tp*scale_factor+1-scale_factor)]) 
					surface(file = file, center=true);
		}
}

module hand() {
	union() {
		// palm
		resize([1.5,4,3]) sphere([1,1,1], $fn=100);
		// fingers
		rotate([-10,0,0]) translate([0,1.5,2]) resize([1,1,4]) sphere([1,1,1], $fn=100);
		rotate([-3,0,0]) translate([0,.5,2]) resize([1,1,4.5]) sphere([1,1,1], $fn=100);
		rotate([3,0,0]) translate([0,-.5,2]) resize([1,1,4.5]) sphere([1,1,1], $fn=100);
		rotate([10,0,0]) translate([0,-1.5,2]) resize([1,1,4]) sphere([1,1,1], $fn=100);

		rotate([50,0,0]) translate([0,-1.5,2]) resize([1,1,4]) sphere([1,1,1], $fn=100);

	}
}


module copy_mirror(vec=[0,1,0])
{
    children();
    mirror(vec) children();
}

module body() {
	body_length = .65;

	upperarm_length = .7;
	forearm_length = .63;

	shoulder_angle = 150;
	elbow_angle = 15;
	wrist_angle = -60;

	hand_size = .07;


	thigh_length = .7;
	shin_length = .55;
	foot_length = .25;

	thigh_angle = 60;
	shin_angle = 80;
	foot_angle = -50;

	butt_size = .3;
	knee_size = .15;
	ankle_size = 0.11;

	// back
	hull() {
		// shoulder part of back
		translate([0, 0, body_length/2]) scale([.4,.3,.5]) sphere(1, $fn=100);
		// butt
		translate([0, 0, -body_length/2]) scale([.6,.35,.5]) sphere(1, $fn=100);
	}

	// arms
	copy_mirror([1,0,0]) {
		translate([.3,0,body_length / 1.3]) {
			hull() {
				translate([0, 0, 0]) scale(.2) sphere(1, $fn=100);
				rotate([10,shoulder_angle,0]) translate([0,0,upperarm_length]) scale(.12) sphere(1, $fn=100);
			}

			rotate([10,shoulder_angle,0]) translate([0,0,upperarm_length]) 
			union(){
				hull() {
					scale(.12) sphere(1, $fn=100);
					rotate([10,elbow_angle,0]) translate([0,0,forearm_length]) {
						scale(.08) sphere(1, $fn=100);
					}
				}
				rotate([10,elbow_angle,0]) translate([-0.05,0,forearm_length*1.1]) 
					rotate([-10,wrist_angle,30])  scale(hand_size) hand();
			}
		}
	}

	// legs
	copy_mirror([1,0,0]) {
		translate([.2,-0.05,-1 * body_length * .7]) 
			union() {
				hull() {
					scale(butt_size) sphere(1, $fn=100);
					rotate([thigh_angle,0,10]) translate([0,0,thigh_length]) 
						scale(knee_size) sphere(1, $fn=100);
					
				}

				rotate([thigh_angle,0,10]) translate([0,0,thigh_length]) union() {
					hull() {
						scale(knee_size) sphere(1, $fn=100);
						rotate([shin_angle,0,0]) translate([0,0,shin_length]) 
							scale(ankle_size) sphere(1, $fn=100);
					}

					rotate([shin_angle,0,0]) translate([0,0,shin_length*1.1]) rotate([foot_angle,0,0]) 
					hull() {
						scale([ankle_size * .6, ankle_size, ankle_size * 1.2]) sphere(1, $fn=100);
						translate([0,0,foot_length]) 
							scale([ankle_size, ankle_size * .7, ankle_size * 1.5]) sphere(1, $fn=100);
					}
				}
			}
	}
}

module sad_robot(face, sadness, head_size, total_size) {
	scale(total_size) rotate([10,0,0]) union() {
		// head
		translate([0,.5+.15*head_size,-.2+.02*head_size])
			scale(head_size)
				rotate([90 + 40*sadness,10,0]) 
					translate([0,.5,.5])
						head(.55, face, 0.5, .4, .2, $t);
		// body
		color([.2,.6,.95])  
			translate([0,.5,-.8 * 1-.2]) 
				scale(1) body();
	}
}

sad_robot("./output/face2.png", .85, 1.2, 1);
