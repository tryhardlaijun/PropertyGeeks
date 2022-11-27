import React, { useEffect } from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import BookmarkIcon from "@mui/icons-material/Bookmark";
import BusinessOutlinedIcon from "@mui/icons-material/BusinessOutlined";
import AccountCircleIcon from "@mui/icons-material/AccountCircle";

function Navbar() {
	return (
		<nav className="navbar navbar-expand-lg navbar-light bg-light">
			<div className="container-fluid">
					<BusinessOutlinedIcon color="success" />
				<button
					className="navbar-toggler"
					type="button"
					data-bs-toggle="collapse"
					data-bs-target="#navbarSupportedContent"
				>
					<span className="navbar-toggler-icon"></span>
				</button>
				<div
					className="collapse navbar-collapse"
					id="navbarSupportedContent"
				>
					<ul className="navbar-nav me-auto mb-2 mb-lg-0">
						<li className="nav-item">
							<Link to={"/HDB"} className="nav-link">
								HDB
							</Link>
						</li>
						<li className="nav-item">
							<Link to={"/PMI"} className="nav-link">
								Private Properties
							</Link>
						</li>
					</ul>
					<ul className="nav navbar-nav ms-auto justify-content-end">
						<li className="nav-item">
							<Link to={"/bookmarks"} className="nav-link">
								<BookmarkIcon />
							</Link>
						</li>
						<li className="nav-item">
							<Link to={"/login"} className="nav-link">
								<AccountCircleIcon />
							</Link>
						</li>
					</ul>
				</div>
			</div>
		</nav>
	);
}
export default Navbar;
