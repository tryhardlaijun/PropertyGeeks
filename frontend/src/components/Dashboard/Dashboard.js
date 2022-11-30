import React from "react";
import { Link } from "react-router-dom";

function Dashboard() {
	const tokenString = localStorage.getItem("token");
	const userToken = JSON.parse(tokenString);

	return (
		<div className="container mt-4">
			<div class="card text-center">
				<div class="card-header">
					<h4 className="text-center headingFont">
						Welcome to Property Geeks
					</h4>
				</div>
				<div class="card-body">
					<h5 class="card-title">Project Done Group_1</h5>
					<p class="card-text">
						👤 Benny Lim Yi Jie - 2101955 <br />
						👤 Chen JiaJun - 2101351 <br />
						👤 Lai Wen Jun - 2102989 <br />
						👤 Lee Yan Rong - 2102608 <br />
						👤 Naomi Cole Lam Ying Tong - 2102102 <br />
						👤 Norman Chia - 2100686
					</p>
					<button type="button" className="updatebutton me-1">
						<Link
							to={userToken ? `/logout` : `/login`}
							style={{ textDecoration: "none", color: "black" }}
						>
							{userToken ? "Logout" : "Login"}
						</Link>
					</button>{userToken?(""):(
					<button type="button" className="updatebutton me-1">
						<Link
							to={`/signup`}
							style={{ textDecoration: "none", color: "black" }}
						>
							Sign Up
						</Link>
					</button>)}
					<button type="button" className="updatebutton me-1">
						<Link
							to={``}
							style={{ textDecoration: "none", color: "black" }}
						>
							Video
						</Link>
					</button>
				</div>
			</div>
		</div>
	);
}

export default Dashboard;
