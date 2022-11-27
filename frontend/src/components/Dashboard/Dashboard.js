import React, { useEffect, useState } from "react";

function Dashboard() {
	return (
		<div className="container mt-4">
			<div class="card text-center">
				<div class="card-header">
					<ul class="nav nav-tabs card-header-tabs">
						<li class="nav-item">
							<a
								class="nav-link active"
								aria-current="true"
								href="#"
							>
								Active
							</a>
						</li>
						<li class="nav-item">
							<a class="nav-link" href="#">
								Link
							</a>
						</li>
						<li class="nav-item">
							<a
								class="nav-link disabled"
								href="#"
								tabindex="-1"
								aria-disabled="true"
							>
								Disabled
							</a>
						</li>
					</ul>
				</div>
				<div class="card-body">
					<h5 class="card-title">Special title treatment</h5>
					<p class="card-text">
						With supporting text below as a natural lead-in to
						additional content.
					</p>
					<a href="#" class="btn btn-primary">
						Go somewhere
					</a>
				</div>
			</div>
		</div>
	);
}

export default Dashboard;